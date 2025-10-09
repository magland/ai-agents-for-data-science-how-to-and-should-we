import figpack.views as fpv
import figpack_slides.views as fps
import os
from figpack_helpers import create_slides_from_markdown


ccm_color = "#F0751C"
header = fps.SlideHeader(height=10, background_color=ccm_color)
footer = fps.SlideFooter(height=10, background_color=ccm_color)
background_color = "white"


def main():
    # Read index.md
    with open("index.md", "r") as f:
        md_content = f.read()

    # Create slides
    slides = create_slides_from_markdown(
        md_content,
        title_slide_background_color=ccm_color,
        standard_slide_background_color="white",
        header=header,
        footer=footer,
    )

    slides.save("build", title="AI Agents for Data Science")


if __name__ == "__main__":
    main()
