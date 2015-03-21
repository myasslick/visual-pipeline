# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from visualize_pipeline import properties
from visualize_pipeline import exceptions as vs_exceptions

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
    def assertPropertiesKeyError(self, ppi, key, subkey):
        self.assertRaises(vs_exceptions.PropertiesKeyError,
            ppi.get_properties_of, key, subkey)

    def test_empty_properties_tree_lookup_raised_error(self):
        tree = properties.PropertiesTree()
        pp = properties.Properties(tree)
        self.assertPropertiesKeyError(pp, "pieline", "name")
        self.assertPropertiesKeyError(pp, "pipeline", "id")

    def test_add_pipeline_name_to_empty_properties_tree(self):
        tree = properties.PropertiesTree()
        pp = properties.Properties(tree)
        pp.update_properties_of("pipeline", "name", "Test")
        self.assertEqual(
            pp.get_properties_of("pipeline", "name"), "Test")

    def test_get_a_properties_from_non_empty_properties_tree(self):
        tree = properties.parse("pipeline.name=Test")
        pp = properties.Properties(tree)
        self.assertEqual(
            pp.get_properties_of("pipeline", "name"), "Test")

if __name__ == "__main__":
    unittest.main()
