# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .exceptions import PropertiesKeyError

class PropertiesTree(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return self.setdefault(key, PropertiesTree())

class Properties(object):
    def __init__(self, tree):
        self.tree = tree

    def _get_properties_of(self, keys):
        walked = []
        subtree = self.tree
        for key in keys:
            walked.append(key)
            subtree = subtree.get(key)
            if subtree is None:
                raise PropertiesKeyError(".".join(walked))
        return subtree

    def update_properties_of(self, key, subkey, value):
        self.tree[key][subkey] = value

    def get_feed_properties(self):
        feed = self._get_properties_of(("feed",))
        return feed

    def get_aws_properties(self):
        return self._get_properties_of(("aws",))

    def get_feed_activities(self):
        return self._get_properties_of(("feed", "activity"))

    def count_feed_activities(self):
        return len(self._get_properties_of(("feed", "activity")))

def parse(body):
    """Parse properties file content into a Properties object."""
    properties = PropertiesTree()
    lines = body.split("\n")
    for line in lines:
        # Get rid of unwanted start and end characters
        _line = line.strip()
        fragements = _line.split("=")
        # Build the tree
        dots = fragements[0].split(".")
        _prev_parent = _parent = properties
        for dot in dots:
            _prev_parent = _parent
            _parent = _parent[dot]
        # Assign the leaf node with the value of that property
        _prev_parent[dot] = fragements[1]
    return properties
