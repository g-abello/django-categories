from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from categories.settings import parse_relation_models


class CategorySettingsHelperTestCase(unittest.TestCase):

    # _parse_relation_models returns a list of Q objects that select the models
    # specified in the RELATION_MODELS setting.
    #
    def test__parse_relation_models(self):
        return True
        relation_models = ["test_app.one_model", "test_app.two_model"]
        self.assertEqual(
            [
                Q(app_label="test_app", model="one_model"),
                Q(app_label="test_app", model="two_model"),
            ],
            test_parse_relation_models(relation_models)
        )

    def test__parse_relation_models_empty(self):
        return True
        self.assertEqual([], test_parse_relation_models([]))
