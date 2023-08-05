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


class V1beta1IngressStatus(object):
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
            'load_balancer': 'V1LoadBalancerStatus'
        }

        self.attribute_map = {
            'load_balancer': 'loadBalancer'
        }

        self._load_balancer = None

    @property
    def load_balancer(self):
        """
        Gets the load_balancer of this V1beta1IngressStatus.
        LoadBalancer contains the current status of the load-balancer.

        :return: The load_balancer of this V1beta1IngressStatus.
        :rtype: V1LoadBalancerStatus
        """
        return self._load_balancer

    @load_balancer.setter
    def load_balancer(self, load_balancer):
        """
        Sets the load_balancer of this V1beta1IngressStatus.
        LoadBalancer contains the current status of the load-balancer.

        :param load_balancer: The load_balancer of this V1beta1IngressStatus.
        :type: V1LoadBalancerStatus
        """
        self._load_balancer = load_balancer

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
