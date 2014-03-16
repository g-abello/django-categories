from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

try:
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest

from django.db.models import Q


def assertQsEqual(q, other_q):
    """Returns True if q and other_q are logically equivalent.
    """
    nodes = izip_longest(
        yield_nodes(q),
        yield_nodes(other_q),
        fillvalue=None
    )
    
    for node, other_node in nodes:
        if node is None or other_node is None:
            return False

        if node.connector != other_node.connector:
            return False

        if node.negated != other_node.negated:
            return False

        children =[_ for _ in node.children if not isinstance(_, Q)]
        other_children = [_ for _ in other_node.children 
                                  if not isinstance(_, Q)]
        if children != other_children:
            return False

    return True

def assertQsNotEqual(q, other_q):
    """Returns True if q and other_q are not logically equivalent.
    """
    return not assertQsEqual(q, other_q)

def yield_nodes(tree):
    """Generator that traverses tree breadth-first and yields tree nodes."""
    queue = [tree]
    while queue:
        node = queue.pop(0) 
        yield node
        children = [_ for _ in node.children if isinstance(_, Q)]
        queue.extend(children)