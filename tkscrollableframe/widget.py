"""
Implementation of the scrollable frame widget.
"""

# pylint: disable=R0902
import sys

import tkinter as tk
from tkinter import ttk

__all__ = ["ScrolledFrame"]

from typing import Any, Union

# Import the scrollbar type enum in a number of ways to support different use cases
try:
    from scrollbar_type_enum import ScrollbarsType
except ImportError:
    from .scrollbar_type_enum import ScrollbarsType

# Scrollbar-related configuration
_DEFAULT_SCROLLBARS = "both"
_VALID_SCROLLBARS = "vertical", "horizontal", "both", "neither"


class ScrolledFrame(tk.Frame):
    """Scrollable Frame widget.

    Use display_widget() to set the interior widget. For example,
    to display a Label with the text "Hello, world!", you can say:

        sf = ScrolledFrame(self)
        sf.pack()
        sf.display_widget(Label, text="Hello, world!")
    You may probably want to put an inner frame inside the ScrolledFrame

    The constructor accepts the usual Tkinter keyword arguments, plus
    a handful of its own:

      scrollbars (str; default: "both")
        Which scrollbars to provide.
        Must be one of "vertical", "horizontal," "both", or "neither".

      use_ttk (bool; default: False)
        Whether to use ttk widgets if available.
        The default is to use standard Tk widgets. This setting has
        no effect if ttk is not available on your system.
    """

    def __init__(self, master: tk.Tk, scrollbars: ScrollbarsType = ScrollbarsType.BOTH,
                 **kwargs) -> None:
        """
        Initialize the ScrolledFrame.

        :param master: The parent widget.
        :param self.__scrollbars: Which scrollbars to provide.
        :param kwargs: Keyword arguments for the usual tk widget settings.
        """

        # bind the arrow keys and scroll wheel
        self.bind_arrow_keys(master)
        self.bind_scroll_wheel(master)

        tk.Frame.__init__(self, master)

        # Hold these names for the interior widget
        self._interior = None
        self._interior_id = None

        # Whether to fit the interior widget's width to the canvas
        self._fit_width = False

        # Which scrollbars to provide
        self.__scrollbars = scrollbars.value

        # Whether to use ttk widgets if available
        if "use_ttk" in kwargs:
            if ttk and kwargs["use_ttk"]:
                scrollbar = ttk.Scrollbar
            else:
                scrollbar = tk.Scrollbar
            del kwargs["use_ttk"]
        else:
            scrollbar = tk.Scrollbar

        # Default to a 1px sunken border
        if "borderwidth" not in kwargs:
            kwargs["borderwidth"] = 1
        if "relief" not in kwargs:
            kwargs["relief"] = "sunken"

        # Set up the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Canvas to hold the interior widget
        canvas = self._canvas = tk.Canvas(self,
                                          borderwidth=0,
                                          highlightthickness=0,
                                          takefocus=0)

        # Enable scrolling when the canvas has the focus
        self.bind_arrow_keys(canvas)
        self.bind_scroll_wheel(canvas)

        # Call _resize_interior() when the canvas widget is updated
        canvas.bind("<Configure>", self._resize_interior)

        # Scrollbars
        xscroll = self._x_scrollbar = scrollbar(self,
                                                orient="horizontal",
                                                command=canvas.xview)
        yscroll = self._y_scrollbar = scrollbar(self,
                                                orient="vertical",
                                                command=canvas.yview)
        canvas.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        # Lay out our widgets
        canvas.grid(row=0, column=0, sticky="nsew")
        if self.__scrollbars in ["vertical", "both"]:
            yscroll.grid(row=0, column=1, sticky="ns")
        if self.__scrollbars in ["horizontal", "both"]:
            xscroll.grid(row=1, column=0, sticky="we")

        # Forward these to the canvas widget
        self.bind = canvas.bind
        self.focus_set = canvas.focus_set
        self.unbind = canvas.unbind
        self.xview = canvas.xview
        self.xview_moveto = canvas.xview_moveto
        self.yview = canvas.yview
        self.yview_moveto = canvas.yview_moveto

        # Process our remaining configuration options
        self.configure(**kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value of a widget option.

        :param key: Key of the dictionary option
        :param value: Value of the dictionary option
        """

        if key in ["width", "height", "takefocus"]:
            # Forward these to the canvas widget
            self._canvas.configure(**{key: value})

        else:
            # Handle everything else normally
            tk.Frame.configure(self, **{key: value})

    def bind_arrow_keys(self, widget: Union[tk.Widget, tk.Tk]) -> None:
        """
        Bind the specified widget's arrow key events to the canvas.

        :param widget: the specified widget to bind
        """

        widget.bind("<Up>",
                    lambda event: self._canvas.yview_scroll(-1, "units"))

        widget.bind("<Down>",
                    lambda event: self._canvas.yview_scroll(1, "units"))

        widget.bind("<Left>",
                    lambda event: self._canvas.xview_scroll(-1, "units"))

        widget.bind("<Right>",
                    lambda event: self._canvas.xview_scroll(1, "units"))

    def bind_scroll_wheel(self, widget: Union[tk.Widget, tk.Tk]) -> None:
        """
        Bind the specified widget's mouse scroll events to the canvas.

        :param widget: the specified widget to bind
        """

        widget.bind("<MouseWheel>", self._scroll_canvas)
        widget.bind("<Button-4>", self._scroll_canvas)
        widget.bind("<Button-5>", self._scroll_canvas)

    def cget(self, key: str) -> Any:
        """
        Get the value of a widget option.

        :param key: The key of the item to get
        :return: The value of the item
        """

        if key in ["width", "height", "takefocus"]:
            return self._canvas.cget(key)

        return tk.Frame.cget(self, key)

    # Also override this alias for cget()
    __getitem__ = cget

    def configure(self, cnf: Any = None, **kw) -> None:
        """
        Configure resources of a widget.

        :param cnf: Dict of options
        :param kw: Keyword arguments
        :return:
        """

        # This is overridden so we can use our custom __setitem__()
        # to pass certain options directly to the canvas.
        if cnf:
            for key in cnf:
                self[key] = cnf[key]

        for key, val in kw.items():
            self[key] = val

    # Also override this alias for configure()
    config = configure

    def display_widget(self, widget_class, fit_width=False, **kw) -> tk.Widget:
        """
        Create and display a new widget.

        :param widget_class:
        :param fit_width: If True, the interior widget will be stretched as
        needed to fit the width of the frame.
        :param kw: Keyword arguments are passed to the widget_class constructor.
        :return: Returns the new widget.
        """

        # Blank the canvas
        self.erase()

        # Set width fitting
        self._fit_width = fit_width

        # Set the new interior widget
        self._interior = widget_class(self._canvas, **kw)

        # Add the interior widget to the canvas, and save its widget ID
        # for use in _resize_interior()
        self._interior_id = self._canvas.create_window(0, 0,
                                                       anchor="nw",
                                                       window=self._interior)

        # Call _update_scroll_region() when the interior widget is resized
        self._interior.bind("<Configure>", self._update_scroll_region)

        # Fit the interior widget to the canvas if requested
        # We don't need to check fit_width here since _resize_interior()
        # already does.
        self._resize_interior()

        # Scroll to the top-left corner of the canvas
        self.scroll_to_top()

        return self._interior

    def erase(self) -> None:
        """
        Erase the displayed widget.
        """

        # Clear the canvas
        self._canvas.delete("all")

        # Delete the interior widget
        del self._interior
        del self._interior_id

        # Save these names
        self._interior = None
        self._interior_id = None

        # Reset width fitting
        self._fit_width = False

    def scroll_to_top(self) -> None:
        """
        Scroll to the top-left corner of the canvas.
        """

        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

    def _resize_interior(self, event: tk.Event = None) -> None:
        """
        Resize the interior widget to fit the canvas.

        :param event: event to resize
        """

        # compare event to keep pylint happy
        if event == 1:
            pass

        if self._fit_width and self._interior_id:
            # The current width of the canvas
            canvas_width = self._canvas.winfo_width()

            # The interior widget's requested width
            requested_width = self._interior.winfo_reqwidth()

            if requested_width != canvas_width:
                # Resize the interior widget
                new_width = max(canvas_width, requested_width)
                self._canvas.itemconfigure(self._interior_id, width=new_width)

    def _scroll_canvas(self, event: tk.Event) -> None:
        """
        Scroll the canvas when event triggered

        :param event: event to scroll
        """

        canvas = self._canvas
        print(self.__scrollbars)
        # If we are able to vertically scroll
        if self.__scrollbars in [ScrollbarsType.BOTH.value, ScrollbarsType.VERTICAL.value]:

            if sys.platform.startswith("darwin"):
                if event.state == 0:  # In macOS event state is 0 for scrolling up and down
                    canvas.yview_scroll(-1 * event.delta, "units")

            # Unix oddly handles each direction separately
            elif event.num == 4:  # Unix - scroll up
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Unix - scroll down
                canvas.yview_scroll(1, "units")

            elif event.state == 8:  # windows scroll y direction
                canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # if we are able to horizontally scroll
        if self.__scrollbars in [ScrollbarsType.BOTH.value, ScrollbarsType.HORIZONTAL.value]:

            if sys.platform.startswith("darwin"):
                if event.state == 1:  # and event state 1 for scrolling left and right
                    canvas.xview_scroll(-1 * event.delta, "units")

            if event.num == 6:  # Unix - scroll left
                canvas.yview_scroll(-1, "units")
            elif event.num == 7:  # Unix - scroll right
                canvas.yview_scroll(1, "units")

            elif event.state == 9:  # windows scroll x direction
                canvas.xview_scroll(-1 * (event.delta // 120), "units")


    def _update_scroll_region(self, event: tk.Event) -> None:
        """
        Update the scroll region when the interior widget is resized.

        :param event: event to resize scrollbar
        """

        # compare event to keep pylint happy
        if event == 1:
            pass

        # The interior widget's requested width and height
        req_width = self._interior.winfo_reqwidth()
        req_height = self._interior.winfo_reqheight()

        # Set the scroll region to fit the interior widget
        self._canvas.configure(scrollregion=(0, 0, req_width, req_height))
