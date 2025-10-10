import shutil
import os
import figpack_slides as fps
from create_slide import create_slide


def main():
    with open("index.md", "r") as f:
        md_content = f.read()

    slides = fps.parse_markdown_to_slides(md_content, create_slide=create_slide)

    slides.save("build", title=slides.slides[0].title.text)

    # Copy videos/ directory to build/, overwriting if it exists
    if os.path.exists("videos"):
        if os.path.exists("build/videos"):
            shutil.rmtree("build/videos")
        print("Copying videos to build directory")
        shutil.copytree("videos", "build/videos")


if __name__ == "__main__":
    main()
