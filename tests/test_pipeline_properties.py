# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from visualize_pipeline import (
    properties,
    exceptions as vs_exceptions
)

class TestPropertiesTree(unittest.TestCase):
    def test_empty_dict_returns_on_declartion(self):
        tree = properties.PropertiesTree()
        self.assertEqual([], tree.keys())
        self.assertEqual({}, tree)

    def test_multilevel_dict_declared_and_mutable(self):
        tree = properties.PropertiesTree()
        tree[1][2]
        self.assertEqual([1], tree.keys())
        self.assertEqual([2], tree[1].keys())
        tree[1][2] = "value2"
        self.assertEqual("value2", tree[1][2])

class TestPropertiesParser(unittest.TestCase):
    def test_feed_id_parsed(self):
        pp = properties.parse("feed.Id=ExampleFeed")
        self.assertEqual(pp["feed"]["Id"], "ExampleFeed")

class TestPropertiesClass(unittest.TestCase):
    def setUp(self):
        self.empty_tree = properties.PropertiesTree()
        self.feed_id = "Test"
        self.activities = {1: {"activity": "EmrScript",
                               "name": "test_feed_download"
                              },
                           2: {"activity": "PigScript",
                               "name": "test_feed_process"
                              }
        }
        self.non_empty_tree = {"feed": {"id": self.feed_id,
                                        "activity": self.activities
        }}

    def assertPropertiesKeyError(self, pp_method):
        self.assertRaises(vs_exceptions.PropertiesKeyError,
            pp_method)

    def test_keyerror_on_empty_tree(self):
        pp = properties.Properties(self.empty_tree)
        self.assertPropertiesKeyError(pp.get_feed_properties)

    def test_keyerror_on_non_existent_key(self):
        pp = properties.Properties(self.non_empty_tree)
        # error message check + exception check
        error_msg = vs_exceptions.PropertiesKeyError.MESSAGE.format(
                key="feed.name")
        self.assertRaisesRegexp(
                vs_exceptions.PropertiesKeyError,
                error_msg,
                pp._get_properties_of,
                ["feed", "name"]
        )

    def test_update_empty_properties_tree(self):
        pp = properties.Properties(self.empty_tree)
        pp.update_properties_of("feed", "id", self.feed_id)
        self.assertEqual(
            pp.get_feed_properties()["id"], self.feed_id)

    def test_get_a_properties_from_non_empty_properties_tree(self):
        pp = properties.Properties(self.non_empty_tree)
        self.assertEqual(
            pp.get_feed_properties()["id"], self.feed_id)

    def test_get_feed_activities(self):
        pp = properties.Properties(self.non_empty_tree)
        self.assertEqual(
            pp.get_feed_activities(),
            self.activities)

    def test_count_feed_activities(self):
        pp = properties.Properties(self.non_empty_tree)
        expected_count = len(self.activities)
        self.assertEqual(pp.count_feed_activities(), expected_count)

if __name__ == "__main__":
    unittest.main()
