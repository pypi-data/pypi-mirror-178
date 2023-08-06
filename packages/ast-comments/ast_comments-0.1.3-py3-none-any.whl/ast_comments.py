import ast
import tokenize
from ast import *  # noqa: F401,F403
from typing import List, Protocol, Tuple, Union


class stmt(ast.stmt):
    comments: Tuple[str, ...]


class AstNode(Protocol):
    body: List[stmt]


def format_comment(comment_string: str):
    return comment_string.lstrip("# ")


def parse(source: Union[str, bytes, ast.AST], *args, **kwargs) -> AstNode:
    tree = ast.parse(source, *args, **kwargs)
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt) and not hasattr(node, "comments"):
            node._fields += ("comments",)
            node.comments = ()
    if isinstance(source, (str, bytes)):
        _enrich(source, tree)
    return tree


def _enrich(source: Union[str, bytes], tree: AstNode) -> None:
    if isinstance(source, bytes):
        source = source.decode()
    lines_iter = iter(source.splitlines(keepends=True))
    tokens = tokenize.generate_tokens(lambda: next(lines_iter))

    comment_tokens = sorted(
        (x.start[0], x) for x in tokens if x.type == tokenize.COMMENT
    )

    if not comment_tokens:
        return

    nodes = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        if node.lineno not in nodes:
            nodes[node.lineno] = [node]
        else:
            nodes[node.lineno].append(node)

    node_lines = sorted(nodes)

    i = j = 0
    while i < len(comment_tokens) and j < len(node_lines):
        t_lineno, token = comment_tokens[i]
        n_lineno = node_lines[j]
        if t_lineno <= n_lineno:
            for node in nodes[n_lineno]:
                node.comments += (format_comment(token.string),)
            i += 1
        else:
            j += 1
