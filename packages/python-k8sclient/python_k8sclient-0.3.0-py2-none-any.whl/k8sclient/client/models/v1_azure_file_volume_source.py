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


class V1AzureFileVolumeSource(object):
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
            'secret_name': 'str',
            'share_name': 'str',
            'read_only': 'bool'
        }

        self.attribute_map = {
            'secret_name': 'secretName',
            'share_name': 'shareName',
            'read_only': 'readOnly'
        }

        self._secret_name = None
        self._share_name = None
        self._read_only = None

    @property
    def secret_name(self):
        """
        Gets the secret_name of this V1AzureFileVolumeSource.
        the name of secret that contains Azure Storage Account Name and Key

        :return: The secret_name of this V1AzureFileVolumeSource.
        :rtype: str
        """
        return self._secret_name

    @secret_name.setter
    def secret_name(self, secret_name):
        """
        Sets the secret_name of this V1AzureFileVolumeSource.
        the name of secret that contains Azure Storage Account Name and Key

        :param secret_name: The secret_name of this V1AzureFileVolumeSource.
        :type: str
        """
        self._secret_name = secret_name

    @property
    def share_name(self):
        """
        Gets the share_name of this V1AzureFileVolumeSource.
        Share Name

        :return: The share_name of this V1AzureFileVolumeSource.
        :rtype: str
        """
        return self._share_name

    @share_name.setter
    def share_name(self, share_name):
        """
        Sets the share_name of this V1AzureFileVolumeSource.
        Share Name

        :param share_name: The share_name of this V1AzureFileVolumeSource.
        :type: str
        """
        self._share_name = share_name

    @property
    def read_only(self):
        """
        Gets the read_only of this V1AzureFileVolumeSource.
        Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts.

        :return: The read_only of this V1AzureFileVolumeSource.
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """
        Sets the read_only of this V1AzureFileVolumeSource.
        Defaults to false (read/write). ReadOnly here will force the ReadOnly setting in VolumeMounts.

        :param read_only: The read_only of this V1AzureFileVolumeSource.
        :type: bool
        """
        self._read_only = read_only

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
