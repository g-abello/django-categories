from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from django.db.models import Q
import six

from .helpers import (
    QComparer,
    assert_equal_Qs,
    assert_equal_without_whitespace,
    assert_not_equal_Qs,
    assert_not_equal_without_whitespace,
    drop_whitespace,
    yield_nodes,
)


class QComparerTestCase(unittest.TestCase):

    # QComparer.equal_Qs returns True if passed Q trees are logically
    # equivalent, False otherwise.
    #
    def test_equal_Qs_returns_true(self):
        q = Q(name="Q test")
        self.assertTrue(QComparer.equal_Qs(q, q))

    def test_equal_Q_returns_false(self):
        q = Q(name="Q test")
        self.assertFalse(QComparer.equal_Qs(q, q|q))


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
                    "Expected to find {0} in {1}".format(val, n)
                )
        
        assertInNextNode([("name", "Q two",)], nodes)
        assertInNextNode(
            [
                ("name", "Q zero"),
                ("name", "Q one"),
            ],
            nodes
        )
        self.assertRaises(StopIteration, six.next, nodes)
        # with self.assertRaises(StopIteration):
        #     six.next(nodes)

    # assert_equal_Qs and assert_not_equal_Qs raise AssertionErrors if the
    # passe Q trees don't meet expectations.
    #
    def test_assertQsEqual_raises_exception(self):
        q = Q(name="Q test")
        self.assertRaises(AssertionError, assert_equal_Qs, q, q|q)
        # with self.assertRaises(AssertionError):
        #     assert_equal_Qs(q, q|q)

    def test_assertQsNotEqual_raises_exception(self):
        Qs = [
            Q(name="Q zero"),
            Q(name="Q one"),
            Q(name="Q two"),
        ]
        combined_Q = Qs[2] | (Qs[0] & Qs[1])
        self.assertRaises(
            AssertionError,
            assert_not_equal_Qs,
            combined_Q,
            combined_Q
        )
        # with self.assertRaises(AssertionError):
        #     assert_not_equal_Qs(combined_Q, combined_Q)

    # assert_equal_without_whitespace and assert_not_equal_without_whitespace
    # determine if two strings are equal after removing all whitspace from them.
    #
    def test_assert_equal_without_whitespace_raises_excpetion(self):
        a = "A test string."
        self.assertRaises(
            AssertionError,
            assert_equal_without_whitespace,
            a,
            a*2
        )
        # with self.assertRaises(AssertionError):
        #     assert_equal_without_whitespace(a, a*2)

    def test_assert_not_equal_without_whitespace_raises_exception(self):
        a = " A test\t string\n with   whitespace ."
        b = "Ateststringwithwhitespace."
        self.assertRaises(
            AssertionError,
            assert_not_equal_without_whitespace,
            a,
            b
        )
        # with self.assertRaises(AssertionError):
        #     assert_not_equal_without_whitespace(a, b)

    # drop_whitespace returns a string with all whitespace replaced with empty
    # strings.
    #
    def test_drop_whitespace(self):
        self.assertEqual(
            "<h1>VeryCondensed</h1><div><p>MuchManageable</p><p>Wow.</p></div>",
            drop_whitespace(
                """\
                <h1>Very Condensed</h1>
                <div>
                    <p>
                        Much
                        Manageable
                    </p>
                    <p>Wow.</p>
                </div>
                """
            )
        )
