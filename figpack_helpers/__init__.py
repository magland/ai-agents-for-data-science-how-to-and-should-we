import base64

import figpack.views as fpv
import figpack_slides.views as fps
import os


def process_passage(passage, create_content, base_dir="."):
    """Process a passage, detecting :::name::: markers, markdown file paths, and iframe tags, returning appropriate content."""
    # Check if passage is an iframe tag
    stripped_passage = passage.strip()
    if stripped_passage.startswith("<iframe") and stripped_passage.endswith("</iframe>"):
        # Extract the URL from the src attribute
        import re
        match = re.search(r'src="([^"]+)"', stripped_passage)
        if match:
            url = match.group(1)
            return fpv.Iframe(url=url)
        else:
            return fpv.Markdown("Error: Invalid iframe tag - no src attribute found", font_size=28)
    
    # Check if passage is a markdown file path (starts with ./ and ends with .md)
    if stripped_passage.startswith("./") and stripped_passage.endswith(".md"):
        # This is a markdown file path - read and embed it
        md_file_path = stripped_passage
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
    
    # Check if passage contains ::: markers
    if ":::" in passage:
        # Find the start and end of the marker
        start_idx = passage.find(":::")
        if start_idx != -1:
            # Find the closing :::
            end_idx = passage.find(":::", start_idx + 3)
            if end_idx != -1:
                # Extract the name
                name = passage[start_idx + 3 : end_idx]

                # Check if this is a pure marker (only whitespace before/after)
                before = passage[:start_idx].strip()
                after = passage[end_idx + 3 :].strip()

                if before or after:
                    # Mixed content - raise exception
                    raise ValueError(
                        f"Mixed content not supported: passage contains both text and :::marker:::. Passage: {passage[:50]}..."
                    )

                # Pure marker - return the content
                return create_content(name)

    # Regular markdown content - check if it contains images and embed them
    passage_with_images = embed_images_as_base64(passage, base_dir)
    return fpv.Markdown(passage_with_images, font_size=28)


def parse_slides(md_content):
    """Parse markdown content into slide data structures."""
    # Split by --- to get individual slides
    raw_slides = md_content.split("\n---\n")

    slides = []
    for raw_slide in raw_slides:
        lines = raw_slide.strip().split("\n")
        if not lines:
            continue

        slide_data = {"title": None, "metadata": {}, "content_passages": []}

        # Extract title (first line starting with #)
        title_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                slide_data["title"] = line.strip().lstrip("#").strip()
                title_idx = i + 1
                break

        # Parse remaining lines for metadata and content
        content_lines = []
        for i in range(title_idx, len(lines)):
            line = lines[i].strip()

            # Check if it's a key-value pair (e.g., layout: title)
            # Ignore lines with ::: markers
            if line.startswith("layout: ") or line.startswith("author: ") or line.startswith("subtitle: "):
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    # Only treat as metadata if key is a simple word (no spaces)
                    if " " not in key:
                        slide_data["metadata"][key] = value
                        continue

            # Otherwise it's content
            content_lines.append(lines[i])

        # Join content and split by :column-break:
        full_content = "\n".join(content_lines).strip()
        if full_content:
            passages = full_content.split("column-break")
            slide_data["content_passages"] = [p.strip() for p in passages if p.strip()]

        slides.append(slide_data)

    return slides


def create_slide(
    slide_data,
    *,
    title_slide_background_color: str,
    background_color: str,
    header,
    footer,
    create_content,
    base_dir: str = ".",
):
    """Create a figpack slide from parsed slide data."""
    print(slide_data)
    # Check if this is a title slide
    if slide_data["metadata"].get("layout") == "title":
        return fps.TitleSlide(
            title=fps.SlideText(
                text=slide_data["title"],
                font_size=80,
                font_family="SANS-SERIF",
                color="white",
            ),
            subtitle=fps.SlideText(
                text=slide_data["metadata"].get("subtitle", ""),
                font_size=40,
                font_family="SANS-SERIF",
                color="white",
            ),
            author=fps.SlideText(
                text=slide_data["metadata"].get("author", ""),
                font_size=30,
                font_family="SANS-SERIF",
                color="white",
            ),
            background_color=title_slide_background_color,
        )

    # Regular slide with content
    if len(slide_data["content_passages"]) == 0:
        # No content
        content = fpv.Markdown("", font_size=30)
    elif len(slide_data["content_passages"]) == 1:
        # Single column - process the passage
        content = process_passage(slide_data["content_passages"][0], create_content=create_content, base_dir=base_dir)
    else:
        # Multiple columns - use Box with horizontal layout
        items = []
        for passage in slide_data["content_passages"]:
            items.append(
                fpv.LayoutItem(
                    view=process_passage(passage, create_content=create_content, base_dir=base_dir),
                    stretch=1,
                )
            )
        content = fpv.Box(direction="horizontal", items=items)

    return fps.Slide(
        title=fps.SlideText(
            text=slide_data["title"] or "", font_size=50, font_family="SANS-SERIF"
        ),
        content=content,
        header=header,
        footer=footer,
        background_color=background_color,
    )


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
    image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
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
