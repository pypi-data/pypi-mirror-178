import ast
from typing import Generator


def walk_disregarding_root(node: ast.AST) -> Generator[ast.AST, None, None]:
    """
    Recursively yield all descendant nodes in the tree starting at *node*
    (EXCLUDING *node* itself), in no specified order.  This is useful if you
    only want to modify nodes in place and don't care about the context.
    """
    from collections import deque
    todo = deque([node])
    node = todo.popleft()
    todo.extend(ast.iter_child_nodes(node))
    while todo:
        node = todo.popleft()
        todo.extend(ast.iter_child_nodes(node))
        yield node


# todo: only use this logic for python 3.7
def fix_missing_locations(node: ast.AST):
    """
    When you compile a node tree with compile(), the compiler expects lineno and
    col_offset attributes for every node that supports them.  This is rather
    tedious to fill in for generated nodes, so this helper adds these attributes
    recursively where not already set, by setting them to the values of the
    parent node.  It works recursively starting at *node*.
    """
    node_types_with_end_lineno_and_end_col_offset = (
        ast.stmt, ast.arg, ast.expr, ast.excepthandler
    )

    def _fix(node: ast.AST, lineno: int, col_offset: int, end_lineno: int, end_col_offset: int):
        if 'lineno' in node._attributes:
            if not hasattr(node, 'lineno'):
                node.lineno = lineno
            else:
                lineno = node.lineno
        if any([isinstance(node, node_type) for node_type in node_types_with_end_lineno_and_end_col_offset]):
            if not hasattr(node, 'end_lineno'):
                node.end_lineno = end_lineno
            else:
                end_lineno = node.end_lineno
        if 'col_offset' in node._attributes:
            if not hasattr(node, 'col_offset'):
                node.col_offset = col_offset
            else:
                col_offset = node.col_offset
        if any([isinstance(node, node_type) for node_type in node_types_with_end_lineno_and_end_col_offset]):
            if not hasattr(node, 'end_col_offset'):
                node.end_col_offset = end_col_offset
            else:
                end_col_offset = node.end_col_offset
        for child in ast.iter_child_nodes(node):
            _fix(child, lineno, col_offset, end_lineno, end_col_offset)
    _fix(node, 1, 0, 1, 0)
    return node
