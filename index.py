import os
import figpack_slides as fps

def main():
    with open("index.md", "r") as f:
        md_content = f.read()

    ccm_color = "#F0751C"
    theme = fps.create_theme_default_1(
        title_bg_color=ccm_color,
        header_bg_color=ccm_color,
        footer_bg_color=ccm_color
    )

    slides = fps.create_presentation(
        md_content, 
        theme=theme
    )

    slides.save("build", title=slides.title)

    if os.environ.get("UPLOAD_FIGURE") == "1":
        slides.show(upload=True, title=slides.title, open_in_browser=True)

if __name__ == "__main__":
    main()
