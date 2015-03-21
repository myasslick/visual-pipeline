# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class PropertiesError(Exception):
    """Base class for exceptions in this module."""
    pass

class PropertiesKeyError(PropertiesError):
    CUSTOM_MESSAGE = "No '{key}' defined in properties."
    def __init__(self, key):
        self.msg = self.CUSTOM_MESSAGE.format(key=key)
        self.key = key
        super(PropertiesError, self).__init__(self.msg)
