import figpack_slides as fps
from create_slide import create_slide


def main():
    with open("index.md", "r") as f:
        md_content = f.read()

    slides = fps.parse_markdown_to_slides(md_content, create_slide=create_slide)

    slides.save("build", title=slides.slides[0].title.text)


if __name__ == "__main__":
    main()
