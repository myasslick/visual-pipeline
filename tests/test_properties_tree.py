# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from visualize_pipeline import properties

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

if __name__ == "__main__":
    unittest.main()
