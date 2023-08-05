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


class V1SELinuxOptions(object):
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
            'user': 'str',
            'role': 'str',
            'type': 'str',
            'level': 'str'
        }

        self.attribute_map = {
            'user': 'user',
            'role': 'role',
            'type': 'type',
            'level': 'level'
        }

        self._user = None
        self._role = None
        self._type = None
        self._level = None

    @property
    def user(self):
        """
        Gets the user of this V1SELinuxOptions.
        User is a SELinux user label that applies to the container.

        :return: The user of this V1SELinuxOptions.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this V1SELinuxOptions.
        User is a SELinux user label that applies to the container.

        :param user: The user of this V1SELinuxOptions.
        :type: str
        """
        self._user = user

    @property
    def role(self):
        """
        Gets the role of this V1SELinuxOptions.
        Role is a SELinux role label that applies to the container.

        :return: The role of this V1SELinuxOptions.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this V1SELinuxOptions.
        Role is a SELinux role label that applies to the container.

        :param role: The role of this V1SELinuxOptions.
        :type: str
        """
        self._role = role

    @property
    def type(self):
        """
        Gets the type of this V1SELinuxOptions.
        Type is a SELinux type label that applies to the container.

        :return: The type of this V1SELinuxOptions.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this V1SELinuxOptions.
        Type is a SELinux type label that applies to the container.

        :param type: The type of this V1SELinuxOptions.
        :type: str
        """
        self._type = type

    @property
    def level(self):
        """
        Gets the level of this V1SELinuxOptions.
        Level is SELinux level label that applies to the container.

        :return: The level of this V1SELinuxOptions.
        :rtype: str
        """
        return self._level

    @level.setter
    def level(self, level):
        """
        Sets the level of this V1SELinuxOptions.
        Level is SELinux level label that applies to the container.

        :param level: The level of this V1SELinuxOptions.
        :type: str
        """
        self._level = level

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
