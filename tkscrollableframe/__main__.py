"""Simple demonstration of the ScrolledFrame widget."""

from tkinter import Tk, Frame, Label

# Import the widget in a number of ways to support different use cases
try:
    from widget import ScrolledFrame
    from scrollbar_type_enum import ScrollbarsType
except ImportError:
    from .widget import ScrolledFrame
    from .scrollbar_type_enum import ScrollbarsType


def demo() -> None:
    """
    Simple as possible demonstration of the ScrolledFrame widget.

    :return: None
    """

    root = Tk()

    # Create a ScrolledFrame widget
    scrolled_frame = ScrolledFrame(root, scrollbars=ScrollbarsType.BOTH,
                                   width=640, height=480)  # Default width and height

    scrolled_frame.pack(side="top", expand=1, fill="both")  # Fill the entire root window

    # Create a frame within the ScrolledFrame
    inner_frame = scrolled_frame.display_widget(Frame)

    # Add a bunch of widgets to fill some space
    num_rows = 10
    num_cols = 10
    for row in range(num_rows):
        for column in range(num_cols):
            # Offset the palette each row to create a diagonal pattern

            # Create a label widget
            box = Label(inner_frame,
                        width=15,
                        height=5,
                        background="#AAAAAA",
                        borderwidth=2,
                        text=str(row * num_cols + column))

            box.grid(row=row,  # and assign it to a grid cell
                     column=column,
                     padx=4,
                     pady=4)

    root.mainloop()


if __name__ == "__main__":
    demo()
