from typing import List
import os
import figpack_slides.views as fpsv
import figpack.views as fpv
import figpack_slides as fps

ccm_color = "#F0751C"
title_slide_text_color = "#FFFFFF"
title_slide_background_color = ccm_color
title_slide_title_font_size = 80
title_slide_subtitle_font_size = 40
title_slide_author_font_size = 30
standard_slide_background_color = "#FFFFFF"
standard_slide_text_color = "#000000"
standard_slide_title_font_size = 50
standard_slide_external_markdown_font_size = 16
header = fpsv.SlideHeader(height=10, background_color=ccm_color)
footer = fpsv.SlideFooter(height=10, background_color=ccm_color)

def get_standard_slide_content_font_size(metadata: dict) -> int:
    font = metadata.get("font", "normal")
    default_font_size = 28
    if font == "small":
        font_size = 16
    elif font == "medium-small":
        font_size = 20
    elif font == "large":
        font_size = 40
    else:
        font_size = default_font_size
    return font_size


def create_slide(
    parsed_slide: fps.ParsedSlide
):
    title = parsed_slide.title
    slide_type = parsed_slide.slide_type
    sections = parsed_slide.sections
    print(
        f"Creating slide: title='{title}', type='{slide_type}', Number of sections={len(sections)}"
    )
    if slide_type == "title":
        return create_title_slide(parsed_slide)
    elif slide_type == "tabs-on-right":
        return create_tabs_on_right_slide(parsed_slide)
    else:
        return create_standard_slide(parsed_slide)
        

def create_standard_slide(
    parsed_slide: fps.ParsedSlide
):
    title = parsed_slide.title
    sections = parsed_slide.sections
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
    return fpsv.Slide(
        title=fpsv.SlideText(text=title or "", font_size=standard_slide_title_font_size, font_family="SANS-SERIF", color=standard_slide_text_color),
        content=content,
        header=header,
        footer=footer,
        background_color=standard_slide_background_color,
    )

def create_tabs_on_right_slide(
    parsed_slide: fps.ParsedSlide
):
    title = parsed_slide.title
    sections = parsed_slide.sections
    if len(sections) < 2:
        raise ValueError("Tabs-on-right slide must have at least two sections.")
    
    # First section goes on the left
    left_content = process_section(sections[0])
    
    # Remaining sections become tabs on the right
    tabs: List[fpv.TabLayoutItem] = []
    for i, section in enumerate(sections[1:], start=1):
        tab_label = section.metadata.get("tab-label", f"Tab {i}")
        tabs.append(
            fpv.TabLayoutItem(
                label=tab_label,
                view=process_section(section),
            )
        )
    
    # Create horizontal layout with left content and tabs on right
    content = fpv.Box(
        direction="horizontal",
        items=[
            fpv.LayoutItem(view=left_content, stretch=1),
            fpv.LayoutItem(view=fpv.TabLayout(items=tabs), stretch=1),
        ]
    )
    
    return fpsv.Slide(
        title=fpsv.SlideText(text=title or "", font_size=standard_slide_title_font_size, font_family="SANS-SERIF", color=standard_slide_text_color),
        content=content,
        header=header,
        footer=footer,
        background_color=standard_slide_background_color,
    )


def create_title_slide(
    parsed_slide: fps.ParsedSlide
):
    title = parsed_slide.title
    if len(parsed_slide.sections) != 1:
        raise ValueError("Title slide must have exactly one section.")
    section = parsed_slide.sections[0]
    metadata = section.metadata
    subtitle = metadata.get("subtitle", "")
    author = metadata.get("author", "")

    return fpsv.TitleSlide(
        title=fpsv.SlideText(
            text=title,
            font_size=title_slide_title_font_size,
            font_family="SANS-SERIF",
            color=title_slide_text_color,
        ),
        subtitle=(
            fpsv.SlideText(
                text=subtitle,
                font_size=title_slide_subtitle_font_size,
                font_family="SANS-SERIF",
                color=title_slide_text_color,
            )
            if subtitle
            else None
        ),
        author=(
            fpsv.SlideText(
                text=author,
                font_size=title_slide_author_font_size,
                font_family="SANS-SERIF",
                color=title_slide_text_color,
            )
            if author
            else None
        ),
        background_color=title_slide_background_color,
    )

def process_section(section: fps.ParsedSlideSection):
    content = section.content.strip()
    metadata = section.metadata

    if metadata.get("figpack-view-example") == "example-1":
        return figpack_view_example_1()

    if content.startswith("<iframe") and content.endswith("</iframe>"):
        # This is an iframe tag - extract the URL and create an Iframe view
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
            
            if metadata.get('markdown-as-text') == 'true':
                md_content = f"````\n{md_content}\n````"  # Using 4 backticks to allow including triple backticks in content

            # Embed images as base64
            md_content_with_images = fps.embed_images_as_base64(md_content, base_dir)

            return fpv.Markdown(md_content_with_images, font_size=standard_slide_external_markdown_font_size)
        except FileNotFoundError:
            return fpv.Markdown(f"Error: File not found: {md_file_path}", font_size=28)
        except Exception as e:
            return fpv.Markdown(f"Error loading markdown file: {str(e)}", font_size=28)

    if content.startswith("![") and "](./" in content and content.endswith(")"):
        # This is an image path - extract the path and create an Image view
        path = content[content.find("](./") + 2 : -1]
        return fpv.Image(path)

    # Regular markdown content - check if it contains images and embed them
    content_with_images = fps.embed_images_as_base64(content, base_dir="./")
    font_size = get_standard_slide_content_font_size(metadata)
    return fpv.Markdown(content_with_images, font_size=font_size)


def figpack_view_example_1():
    import numpy as np
    import figpack.views as vv

    # Create a simple timeseries
    graph = vv.TimeseriesGraph(y_label="Amplitude")

    # Generate data
    t = np.linspace(0, 10, 500)
    y = np.sin(2 * np.pi * t) * np.exp(-t / 5)

    # Add line series
    graph.add_line_series(
        name="Damped Sine",
        t=t.astype(np.float32),
        y=y.astype(np.float32),
        color="blue"
    )

    return graph