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


class V1EndpointSubset(object):
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
            'addresses': 'list[V1EndpointAddress]',
            'not_ready_addresses': 'list[V1EndpointAddress]',
            'ports': 'list[V1EndpointPort]'
        }

        self.attribute_map = {
            'addresses': 'addresses',
            'not_ready_addresses': 'notReadyAddresses',
            'ports': 'ports'
        }

        self._addresses = None
        self._not_ready_addresses = None
        self._ports = None

    @property
    def addresses(self):
        """
        Gets the addresses of this V1EndpointSubset.
        IP addresses which offer the related ports that are marked as ready. These endpoints should be considered safe for load balancers and clients to utilize.

        :return: The addresses of this V1EndpointSubset.
        :rtype: list[V1EndpointAddress]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """
        Sets the addresses of this V1EndpointSubset.
        IP addresses which offer the related ports that are marked as ready. These endpoints should be considered safe for load balancers and clients to utilize.

        :param addresses: The addresses of this V1EndpointSubset.
        :type: list[V1EndpointAddress]
        """
        self._addresses = addresses

    @property
    def not_ready_addresses(self):
        """
        Gets the not_ready_addresses of this V1EndpointSubset.
        IP addresses which offer the related ports but are not currently marked as ready because they have not yet finished starting, have recently failed a readiness check, or have recently failed a liveness check.

        :return: The not_ready_addresses of this V1EndpointSubset.
        :rtype: list[V1EndpointAddress]
        """
        return self._not_ready_addresses

    @not_ready_addresses.setter
    def not_ready_addresses(self, not_ready_addresses):
        """
        Sets the not_ready_addresses of this V1EndpointSubset.
        IP addresses which offer the related ports but are not currently marked as ready because they have not yet finished starting, have recently failed a readiness check, or have recently failed a liveness check.

        :param not_ready_addresses: The not_ready_addresses of this V1EndpointSubset.
        :type: list[V1EndpointAddress]
        """
        self._not_ready_addresses = not_ready_addresses

    @property
    def ports(self):
        """
        Gets the ports of this V1EndpointSubset.
        Port numbers available on the related IP addresses.

        :return: The ports of this V1EndpointSubset.
        :rtype: list[V1EndpointPort]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """
        Sets the ports of this V1EndpointSubset.
        Port numbers available on the related IP addresses.

        :param ports: The ports of this V1EndpointSubset.
        :type: list[V1EndpointPort]
        """
        self._ports = ports

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
