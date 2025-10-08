import figpack.views as fpv
import figpack_slides.views as fps
import os
from figpack_helpers import parse_slides, embed_images_as_base64, create_slide


ccm_color = "#F0751C"

header = fps.SlideHeader(height=10, background_color=ccm_color)
footer = fps.SlideFooter(height=10, background_color=ccm_color)
background_color = "white"


def create_content(name: str):
    if name == "plot-1":
        return plot_1()
    elif name == "example-1":
        return example_1()
    return fpv.Markdown(f"Content '{name}' not found.", font_size=24)


def plot_1():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Sine Wave")
    return fpv.MatplotlibFigure(fig)


def example_1():
    path = "spurious-discovery-tests/examples/temporal_autocorrelation_01/tests/claude-sonnet-4/working/report.md"
    base_dir = os.path.dirname(path)

    with open(path, "r") as f:
        report_content = f.read()

    # Embed images as base64
    report_content_with_images = embed_images_as_base64(report_content, base_dir)

    return fpv.Markdown(report_content_with_images, font_size=12)


def create_slides_from_markdown(md_content: str):
    slide_data_list = parse_slides(md_content)
    slides = [
        create_slide(
            slide_data,
            background_color=background_color,
            title_slide_background_color=ccm_color,
            header=header,
            footer=footer,
            create_content=create_content,
            base_dir=".",
        )
        for slide_data in slide_data_list
    ]
    return fps.Slides(slides=slides)


def main():
    # Read index.md
    with open("index.md", "r") as f:
        md_content = f.read()

    # Create slides
    slides = create_slides_from_markdown(md_content)

    slides.save("build", title="AI Agents for Data Science")


if __name__ == "__main__":
    main()
