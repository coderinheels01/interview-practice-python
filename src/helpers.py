from pathlib import Path


def show_diagram(filename: str, caller_file: str = __file__, figsize: tuple = (12, 8)):
    """
    Render a diagram image inline.

    Args:
        filename:    Image filename (e.g. "circle-diagram.png") located in an
                     'assets/' folder next to the calling file.
        caller_file: Pass __file__ from the calling script so the assets folder
                     is resolved relative to that file, not this helper.
        figsize:     Matplotlib figure size (width, height) in inches.
                     Only used when IPython is not available.
    """
    img_path = Path(caller_file).parent / "assets" / filename
    if not img_path.exists():
        print(f"[show_diagram] Image not found: {img_path}")
        return

    try:
        from IPython.display import Image, display

        display(Image(filename=str(img_path)))
    except ImportError:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        img = mpimg.imread(str(img_path))
        plt.figure(figsize=figsize)
        plt.imshow(img)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
