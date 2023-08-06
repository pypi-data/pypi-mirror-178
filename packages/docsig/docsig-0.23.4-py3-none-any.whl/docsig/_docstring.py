"""
docsig._docstring
=================
"""
from __future__ import annotations

import re as _re
import textwrap as _textwrap

import astroid as _ast

from ._utils import get_index as _get_index
from ._utils import gettabno as _gettabno
from ._utils import lstrip_quant as _lstrip_quant


class _BaseDocStyle:
    PARAM_KEYS: tuple[str, ...] = tuple()

    def __init__(self) -> None:
        self._returns = False
        self._args: list[tuple[str, str | None]] = []

    @property
    def args(self) -> tuple[tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._returns


class _DocStyle(_BaseDocStyle):
    def __init__(self, string: str) -> None:
        super().__init__()
        # the first line has variable indentation
        # remove for uniform dedenting
        self._string = _textwrap.dedent("\n".join(string.splitlines()[1:]))

    @property
    def isstyle(self) -> bool:
        """Boolean result for whether string matches this style."""
        return any(i in self._string for i in self.PARAM_KEYS)


class _SphinxStyle(_DocStyle):

    PARAM_KEYS = ("param", "key", "keyword", "return")

    def __init__(self, string: str) -> None:
        super().__init__(string)
        keys = 0
        for line in string.splitlines():
            line = _lstrip_quant(line, 4)
            match = _re.match(":(.*?): ", line)
            if (
                match is not None
                and line.startswith(match.group(0))
                and any(
                    match.group(1).startswith(inc) for inc in self.PARAM_KEYS
                )
            ):
                string_list = match.group(1).split()
                key, value = string_list[0], _get_index(1, string_list)
                if key == "return":
                    self._returns = True
                    continue

                if key in ("key", "keyword"):
                    if keys == 1:
                        continue

                    keys = 1
                    value = "(**)"

                self._args.append((key, value))


class _NumpyStyle(_DocStyle):
    TAB = "    "
    PARAM_KEYS = ("Parameters", "Returns")
    PARAM_UL = tuple(len(i) * "-" for i in PARAM_KEYS)

    def __init__(self, string: str) -> None:
        super().__init__(string)
        self._in_params = 0
        self._returns = (
            f"{self.PARAM_KEYS[1]}\n{self.PARAM_UL[1]}" in self._string
        )
        self._match_indent: int | None = None
        for line in string.splitlines():
            self._populate_args(line)

    def _populate_args(self, line: str) -> None:
        if self.PARAM_KEYS[0] in line:
            self._in_params = 1

        elif self._in_params == 1 and self.PARAM_UL[0] in line:
            self._in_params = 2

        elif self._in_params == 2:
            if line == "":
                self._in_params = 0
            else:
                if self._match_indent is None:
                    self._match_indent = _gettabno(line)

                if _gettabno(line) == self._match_indent:
                    value = line.split(":")[0].strip()
                    if value:
                        key = "param"
                        if value.startswith("**"):
                            key, value = "keyword", "(**)"

                        elif value.startswith("*"):
                            value = value[1:]

                        self._args.append((key, value))

    @property
    def isstyle(self) -> bool:
        """Boolean result for whether string matches this style."""
        return super().isstyle and any(
            i in self._string for i in self.PARAM_UL
        )


class Docstring:
    """Represents docstring.

    :param node: Docstring's abstract syntax tree.
    """

    def __init__(self, node: _ast.Const | None = None) -> None:
        self._string = None
        self._returns = False
        self._args: list[tuple[str, str | None]] = []
        self._style = _BaseDocStyle()
        if node is not None:
            self._string = node.value
            self._get_style(node.value)

    def _get_style(self, string: str) -> None:
        sphinx_style = _SphinxStyle(string)
        numpy_style = _NumpyStyle(string)
        if numpy_style.isstyle:
            self._style = numpy_style

        elif sphinx_style.isstyle:
            self._style = sphinx_style

    @property
    def string(self) -> str | None:
        """The raw documentation string, if it exists, else None."""
        return self._string

    @property
    def args(self) -> tuple[tuple[str, str | None], ...]:
        """Docstring args."""
        return tuple(self._style.args)

    @property
    def returns(self) -> bool:
        """Check that docstring return is documented."""
        return self._style.returns
