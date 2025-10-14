import os
import figpack_slides as fps
from create_slide import create_slide


def main():
    with open("index.md", "r") as f:
        md_content = f.read()

    slides = fps.parse_markdown_to_slides(md_content, create_slide=create_slide)

    slides.save("build", title=slides.slides[0].title.text)

    if os.environ.get("UPLOAD_FIGURE") == "1":
        slides.show(upload=True, title=slides.slides[0].title.text, open_in_browser=True)


if __name__ == "__main__":
    main()
