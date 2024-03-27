"""
This module holds an enum class that defines the types of scrollbars
that can be used in the ScrollableFrame class.
"""

from enum import Enum


class ScrollbarsType(Enum):
    """
    An enum class that defines the types of scrollbars that can be used
    """
    VERTICAL = "vertical"  # If you only want a vertical scrollbar
    HORIZONTAL = "horizontal"  # If you only want a horizontal scrollbar
    BOTH = "both"  # If you want both a vertical and horizontal scrollbar
    NONE = "neither"  # If you don't want any scrollbars
