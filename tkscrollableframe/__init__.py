"""A scrollable Frame widget for Tkinter."""

# Import the widget in a number of ways to support different use cases
try:
    from widget import ScrolledFrame
except ImportError:
    from .widget import ScrolledFrame


# The only thing we need to publicly export is the widget
__all__ = ["ScrolledFrame"]
