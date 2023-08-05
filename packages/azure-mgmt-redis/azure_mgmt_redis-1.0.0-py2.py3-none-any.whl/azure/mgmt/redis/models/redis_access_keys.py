# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RedisAccessKeys(Model):
    """Redis cache access keys.

    :param primary_key: The current primary key that clients can use to
     authenticate with redis cache.
    :type primary_key: str
    :param secondary_key: The current secondary key that clients can use to
     authenticate with redis cache.
    :type secondary_key: str
    """ 

    _attribute_map = {
        'primary_key': {'key': 'primaryKey', 'type': 'str'},
        'secondary_key': {'key': 'secondaryKey', 'type': 'str'},
    }

    def __init__(self, primary_key=None, secondary_key=None):
        self.primary_key = primary_key
        self.secondary_key = secondary_key
