from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import six
import unittest

from django.db.models import Q

from .helpers import assertQsEqual, assertQsNotEqual, yield_nodes


class HelpersTestCase(unittest.TestCase):

    # Q objects are sublcasses of Django's utils.tree.Node. yeild_nodes
    # traverses the Q tree breadth-first and yields each Q object.
    #
    def test_yield_nodes(self):
        Qs = [
            Q(name="Q zero"),
            Q(name="Q one"),
            Q(name="Q two"),
        ]
        combined_Q = Qs[2] | (Qs[0] & Qs[1])

        nodes = yield_nodes(combined_Q)
        
        def assertInNextNode(vals, nodes):
            n = six.next(nodes)
            for val in vals:
                self.assertTrue(
                    val in n,
                    "Expected to find {} in {}".format(val, n)
                )
        
        assertInNextNode([("name", "Q two",)], nodes)
        assertInNextNode(
            [
                ("name", "Q zero"),
                ("name", "Q one"),
            ],
            nodes
        )
        with self.assertRaises(StopIteration):
            six.next(nodes)

    # assertQsEqual and assertQsNotEqual determine if two Q trees are logically
    # equivalent.
    #
    def test_assertQsEqual(self):
        Qs = [
            Q(name="Q zero"),
            Q(name="Q one"),
            Q(name="Q two"),
        ]
        combined_Q = Qs[2] | (Qs[0] & Qs[1])
        self.assertTrue(assertQsEqual(combined_Q, combined_Q))

    def test_assertQsNotEqual(self):
        q = Q(name="Q test")
        combined_Q = q | q
        self.assertTrue(assertQsNotEqual(q, combined_Q))
