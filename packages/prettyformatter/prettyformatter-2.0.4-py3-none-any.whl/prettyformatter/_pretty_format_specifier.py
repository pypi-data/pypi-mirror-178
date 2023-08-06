"""
Implements:
    Format
"""

try:
    from typing import final
except:
    class Format:
        _formatter: str

        __slots__ = ("_formatter")

        def __init__(self, formatter: str) -> None:
            self._formatter = formatter

        def format(self, s: str) -> str:
            return self._formatter.format(s)
else:
    @final
    class Format:
        _formatter: str

        __slots__ = ("_formatter")

        def __init__(self, formatter: str) -> None:
            self._formatter = formatter

        def format(self, s: str) -> str:
            return self._formatter.format(s)
