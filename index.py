import figpack_slides.views as fps
from figpack_slides_helpers import create_slides_from_markdown, create_title_slide, create_standard_slide


ccm_color = "#F0751C"
header = fps.SlideHeader(height=10, background_color=ccm_color)
footer = fps.SlideFooter(height=10, background_color=ccm_color)


def create_slide(
    *,
    title: str,
    slide_type: str,
    sections: list
):
    print(
        f"Creating slide: title='{title}', type='{slide_type}', Number of sections={len(sections)}"
    )
    if slide_type == "title":
        if len(sections) != 1:
            raise ValueError("Title slide must have exactly one section.")
        return create_title_slide(
            title=title,
            section=sections[0],
            background_color=ccm_color,
            color="white",
        )
    else:
        return create_standard_slide(
            title=title,
            sections=sections,
            background_color="white",
            color="black",
            header=header,
            footer=footer,
        )


def main():
    with open("index.md", "r") as f:
        md_content = f.read()

    slides = create_slides_from_markdown(
        md_content,
        create_slide=create_slide
    )

    slides.save("build", title="AI Agents for Data Science")


if __name__ == "__main__":
    main()
