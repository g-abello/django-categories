from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from textwrap import dedent

import unittest

from django import template
from django.test import TestCase
from django.utils.html import strip_spaces_between_tags

from categories.models import Category
from .helpers import assert_equal_without_whitespace


class CategoryTagsTest(TestCase):

    # maxDiff controls the length of diff messages from failed assertEquals.
    # None will show all diffs regardless of length.
    #
    maxDiff = None

    fixtures = ['musicgenres.json']

    def render_template(self, template_string, context={}):
        """
        Return the rendered string or raise an exception.
        """
        tpl = template.Template(template_string)
        ctxt = template.Context(context)
        return tpl.render(ctxt)

    def testTooFewArguments(self):
        """
        Ensure that get_category raises an exception if there aren't enough arguments.
        """
        self.assertRaises(template.TemplateSyntaxError, self.render_template, '{% load category_tags %}{% get_category %}')

    def test_basic_usage(self):
        """
        Test that we can properly retrieve a category.
        """
        # display_path_as_ul
        rock_resp = """<ul><li><a href="/categories/">Top</a></li></ul>"""
        resp = self.render_template(
            """{% load category_tags %}{% display_path_as_ul "/Rock" %}"""
        )
        self.assertEqual(resp, rock_resp)

        # display_drilldown_as_ul
        expected_resp = """\
            <ul>
                <li>
                    <a href="/categories/">Top</a>
                    <ul>
                        <li>
                            <a href="/categories/world/">World</a>
                            <ul>
                                <li>
                                    <strong>Worldbeat</strong>
                                    <ul>
                                        <li>
                                            <a href="/categories/world/worldbeat/afrobeat/">Afrobeat</a>
                                        </li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
            """
        resp = self.render_template(
            """\
            {% load category_tags %}
            {% display_drilldown_as_ul "/World/Worldbeat" "categories.category" %}
            """
        )
        assert_equal_without_whitespace(expected_resp, resp)

        # breadcrumbs
        expected_resp = """\
            <a href="/categories/world/">World</a> &gt; Worldbeat
            """

        resp = self.render_template(
            """\
            {% load category_tags %}
            {% breadcrumbs "/World/Worldbeat" " &gt; " "categories.category" %}
            """
        )
        assert_equal_without_whitespace(expected_resp, resp)

        # get_top_level_categories
        tags = [
            "Avant-garde",
            "Blues",
            "Country",
            "Easy listening",
            "Electronic",
            "Hip hop/Rap music",
            "Jazz",
            "Latin",
            "Modern folk",
            "Pop",
            "Reggae",
            "Rhythm and blues",
            "Rock",
            "World",
        ]
        expected_resp = "|".join(tags) + "|"
        resp = self.render_template(
            """\
            {% load category_tags %}
            {% get_top_level_categories using "categories.category" as varname %}
            {% for item in varname %}{{ item }}|{% endfor %}
            """
        )
        assert_equal_without_whitespace(expected_resp, resp)

        # get_category_drilldown
        expected_resp = "World|World &gt; Worldbeat|"
        resp = self.render_template(
            """\
            {% load category_tags %}
            {% get_category_drilldown "/World" using "categories.category" as var %}
            {% for item in var %}{{ item }}|{% endfor %}
            """
        )
        assert_equal_without_whitespace(expected_resp, resp)

        # recursetree
        expected_resp = """\
            <ul>
                <li>
                    Country
                    <ul>
                        <li>
                            Country pop
                            <ul>
                                <li>
                                    Urban Cowboy
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li>
                    World
                    <ul>
                        <li>
                            Worldbeat
                            <ul></ul>
                        </li>
                    </ul>
                </li>
            </ul>
            """
        ctxt = {
            'nodes': Category.objects.filter(
                name__in=("Worldbeat", "Urban Cowboy")
            ),
        }
        resp = self.render_template(
            """\
            {% load category_tags %}
            {% spaceless %}
                <ul>
                    {% recursetree nodes|tree_queryset %}
                        <li>
                            {{ node.name }}
                            {% if not node.is_leaf_node %}
                                <ul>
                                    {{ children }}
                                </ul>
                            {% endif %}
                        </li>
                    {% endrecursetree %}
                </ul>
            {% endspaceless %}
            """,
            ctxt
        )
        assert_equal_without_whitespace(expected_resp, resp)
