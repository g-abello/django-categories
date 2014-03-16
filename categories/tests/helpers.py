from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import re

from six.moves import zip_longest

from django.db.models import Q


class QComparer(object):

    @classmethod
    def equal_Q_nodes(cls, node, other_node):
        """Returns True if both nodes (ignoring child Q nodes) are equal. False
        otherwise.
        """
        if node is None or other_node is None:
            return False

        if node.connector != other_node.connector:
            return False

        if node.negated != other_node.negated:
            return False

        # OR nodes only have other Qs as children. AND nodes have both their
        # key value pairs for filtering as well as potential Q children.
        #
        if node.connector == Q.AND:
            value = node.children[0]
            other_value = other_node.children[0]
            if value != other_value:
                return False

        return True

    @classmethod
    def equal_Q_trees(cls, tree, other_tree):
        """Returns True if tree and other_three are logically equivalent.
        """
        nodes = zip_longest(
            yield_nodes(tree),
            yield_nodes(other_tree),
            fillvalue=None
        )
        for node, other_node in nodes:
            if not cls.equal_Q_nodes(node, other_node):
                return False
        return True

    @classmethod
    def equal_Qs(cls, q, other_q):
        """Returns True if q and other_q are logically equivalent. Since Q
        objects are structured as trees, equal_Q just calls equal_Q_tree.
        """
        return cls.equal_Q_trees(q, other_q)


def drop_whitespace(string):
    """Returns a string stripped of all whitespace."""
    s, _ = re.subn(r'\s', '', string)
    return s

def assert_equal_without_whitespace(string, other_string):
    s = drop_whitespace(string)
    other_s = drop_whitespace(other_string)
    if s != other_s:
        raise AssertionError("Expected {} to equal {}".format(s, other_s))

def assert_not_equal_without_whitespace(string, other_string):
    s = drop_whitespace(string)
    other_s = drop_whitespace(other_string)
    if s == other_s:
        raise AssertionError("Expected {} to NOT equal {}".format(s, other_s))

def assert_equal_Qs(q, other_q):
    """Rasies AssertionError if q and other_q are not equal.
    """
    if not QComparer.equal_Qs(q, other_q):
        raise AssertionError("Expected {} to equal {}".format(q, other_q))

def assert_not_equal_Qs(q, other_q):
    """Rasies AssertionError if q and other_q are equal.
    """
    if QComparer.equal_Qs(q, other_q):
        raise AssertionError("Expected {} to NOT equal {}".format(q, other_q))

def yield_nodes(tree):
    """Generator that traverses tree breadth-first and yields tree nodes."""
    queue = [tree]
    while queue:
        node = queue.pop(0) 
        yield node
        children = [_ for _ in node.children if isinstance(_, Q)]
        queue.extend(children)
