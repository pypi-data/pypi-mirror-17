# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems


class JsonWatchEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Swagger model

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'object': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'object': 'object'
        }

        self._type = None
        self._object = None

    @property
    def type(self):
        """
        Gets the type of this JsonWatchEvent.
        the type of watch event; may be ADDED, MODIFIED, DELETED, or ERROR

        :return: The type of this JsonWatchEvent.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this JsonWatchEvent.
        the type of watch event; may be ADDED, MODIFIED, DELETED, or ERROR

        :param type: The type of this JsonWatchEvent.
        :type: str
        """
        self._type = type

    @property
    def object(self):
        """
        Gets the object of this JsonWatchEvent.
        the object being watched; will match the type of the resource endpoint or be a Status object if the type is ERROR

        :return: The object of this JsonWatchEvent.
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """
        Sets the object of this JsonWatchEvent.
        the object being watched; will match the type of the resource endpoint or be a Status object if the type is ERROR

        :param object: The object of this JsonWatchEvent.
        :type: str
        """
        self._object = object

    def to_dict(self):
        """
        Return model properties dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Return model properties str
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()
