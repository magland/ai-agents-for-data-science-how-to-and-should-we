import base64
import os
import figpack_slides.views as fps
import figpack.views as fpv


def embed_images_as_base64(markdown_content: str, base_dir: str) -> str:
    """
    Convert image references in markdown to base64 data URIs.

    Args:
        markdown_content: The markdown text containing image references
        base_dir: Directory path where image files are located

    Returns:
        Modified markdown with images embedded as base64 data URIs
    """
    import re

    # Pattern to match markdown images: ![alt text](image.png)
    image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def replace_image(match):
        """Replace function to convert image reference to base64 data URI."""
        alt_text = match.group(1)
        image_filename = match.group(2)

        # Skip if it's already a data URI or absolute URL
        if image_filename.startswith("data:") or image_filename.startswith("http"):
            return match.group(0)  # Return original match unchanged

        # Build full path to the image file
        image_path = os.path.join(base_dir, image_filename)

        # Read and encode the image
        try:
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()
                base64_data = base64.b64encode(image_data).decode("utf-8")

                # Determine image type from extension
                ext = os.path.splitext(image_filename)[1].lower()
                mime_type = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".svg": "image/svg+xml",
                }.get(ext, "image/png")

                # Create data URI
                data_uri = f"data:{mime_type};base64,{base64_data}"

                # Return the replacement with base64 data
                return f"![{alt_text}]({data_uri})"
        except (FileNotFoundError, PermissionError, IOError, OSError):
            # If any error occurs, return the original match unchanged
            return match.group(0)

    # Use re.sub to replace all image references
    return image_pattern.sub(replace_image, markdown_content)


def parse_key_value_assignment(line: str):
    ind = line.find(" <- ")
    if ind == -1:
        return None, None
    key = line[:ind].strip()
    if " " in key:
        return None, None
    value = line[ind + 4 :].strip()
    return key, value


def is_key_value_assignment(line: str):
    key, value = parse_key_value_assignment(line)
    return key is not None and value is not None


def parse_slides(md_content):
    """Parse markdown content into slide data structures."""
    # Split by --- to get individual slides
    raw_slides = md_content.split("\n---\n")

    slides = []
    for raw_slide in raw_slides:
        lines = raw_slide.strip().split("\n")
        if not lines:
            continue

        slide_data = {"title": None, "slide-type": None, "sections": []}

        slide_data["sections"].append(
            {
                "metadata": {},
                "content": "",
            }
        )
        for line in lines:
            if line.startswith("# ") and slide_data["title"] is None:
                slide_data["title"] = line.lstrip("# ").strip()
            elif line == "section-break":
                slide_data["sections"].append({"metadata": {}, "content": ""})
            elif is_key_value_assignment(line):
                key, value = parse_key_value_assignment(line)
                if key and value:
                    if key == "slide-type":
                        slide_data["slide-type"] = value
                    else:
                        slide_data["sections"][-1]["metadata"][key] = value
            else:
                if slide_data["sections"][-1]["content"]:
                    slide_data["sections"][-1]["content"] += "\n" + line
                else:
                    slide_data["sections"][-1]["content"] = line
        slides.append(slide_data)

    return slides


def create_title_slide(title: str, section: dict, *, background_color: str):
    metadata = section.get("metadata", {})
    subtitle = metadata.get("subtitle", "")
    author = metadata.get("author", "")

    return fps.TitleSlide(
        title=fps.SlideText(
            text=title,
            font_size=80,
            font_family="SANS-SERIF",
            color="white",
        ),
        subtitle=(
            fps.SlideText(
                text=subtitle,
                font_size=40,
                font_family="SANS-SERIF",
                color="white",
            )
            if subtitle
            else None
        ),
        author=(
            fps.SlideText(
                text=author,
                font_size=30,
                font_family="SANS-SERIF",
                color="white",
            )
            if author
            else None
        ),
        background_color=background_color,
    )


def process_section(section: dict):
    content = section.get("content", "")
    metadata = section.get("metadata", {})
    font = metadata.get("font", "normal")
    if content.startswith("<iframe") and content.endswith("</iframe>"):
        # Extract the URL from the src attribute
        import re

        match = re.search(r'src="([^"]+)"', content)
        if match:
            url = match.group(1)
            return fpv.Iframe(url=url)
        else:
            return fpv.Markdown(
                "Error: Invalid iframe tag - no src attribute found", font_size=28
            )

    if content.startswith("./") and content.endswith(".md"):
        # This is a markdown file path - read and embed it
        md_file_path = content
        base_dir = os.path.dirname(md_file_path)

        try:
            with open(md_file_path, "r") as f:
                md_content = f.read()

            # Embed images as base64
            md_content_with_images = embed_images_as_base64(md_content, base_dir)

            return fpv.Markdown(md_content_with_images, font_size=16)
        except FileNotFoundError:
            return fpv.Markdown(f"Error: File not found: {md_file_path}", font_size=28)
        except Exception as e:
            return fpv.Markdown(f"Error loading markdown file: {str(e)}", font_size=28)

    if content.startswith("![") and "](./" in content and content.endswith(")"):
        path = content[content.find("](./") + 2 : -1]
        return fpv.Image(path)

    # Regular markdown content - check if it contains images and embed them
    content_with_images = embed_images_as_base64(content, base_dir="./")
    font_size = 28
    if font == "small":
        font_size = 16
    return fpv.Markdown(content_with_images, font_size=font_size)


def create_standard_slide(
    title: str, sections: list, *, background_color: str, header, footer
):
    if len(sections) == 0:
        raise ValueError("Standard slide must have at least one section.")
    if len(sections) == 1:
        # Single column - process the passage
        content = process_section(sections[0])
    elif len(sections) == 2:
        # Multiple columns - use Box with horizontal layout
        items = []
        for section in sections:
            items.append(
                fpv.LayoutItem(
                    view=process_section(section),
                    stretch=1,
                )
            )
        content = fpv.Box(direction="horizontal", items=items)
    else:
        raise ValueError("Slides with more than two sections are not supported.")
    return fps.Slide(
        title=fps.SlideText(text=title or "", font_size=50, font_family="SANS-SERIF"),
        content=content,
        header=header,
        footer=footer,
        background_color=background_color,
    )


def create_slide(
    slide_data,
    *,
    title_slide_background_color,
    standard_slide_background_color,
    header,
    footer,
):
    title = slide_data.get("title", "")
    slide_type = slide_data.get("slide-type", "standard")
    sections = slide_data.get("sections", [])
    print(
        f"Creating slide: title='{title}', type='{slide_type}', Number of sections={len(sections)}"
    )
    if slide_type == "title":
        if len(sections) != 1:
            raise ValueError("Title slide must have exactly one section.")
        return create_title_slide(
            title=title,
            section=sections[0],
            background_color=title_slide_background_color,
        )
    else:
        return create_standard_slide(
            title=title,
            sections=sections,
            background_color=standard_slide_background_color,
            header=header,
            footer=footer,
        )


def create_slides_from_markdown(
    md_content: str,
    *,
    title_slide_background_color,
    standard_slide_background_color,
    header,
    footer,
):
    slide_data_list = parse_slides(md_content)
    slides = [
        create_slide(
            slide_data,
            title_slide_background_color=title_slide_background_color,
            standard_slide_background_color=standard_slide_background_color,
            header=header,
            footer=footer,
        )
        for slide_data in slide_data_list
    ]
    print(f"Created {len(slides)} slides.")
    return fps.Slides(slides=slides)
