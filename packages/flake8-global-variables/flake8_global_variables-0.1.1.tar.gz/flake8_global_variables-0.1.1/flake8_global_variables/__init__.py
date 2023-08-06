import sys
import ast
from typing import Any, Type, Tuple, Generator


if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


_GV400 = 'GV400: Found global variable'


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Global(self, node):
        for name in node.names:
            if not name.isupper():
                self.errors.append((node.lineno, node.col_offset, _GV400))
                self.generic_visit(node)

    def visit_Assign(self, node):
        if node.col_offset == 0:
            for target in node.targets:
                if hasattr(target, 'id') and not target.id.isupper():
                    self.errors.append((node.lineno, node.col_offset, _GV400))
                    self.generic_visit(node)


class GlobalVariablesChecker:
    name = 'flake8-global-variables'
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
