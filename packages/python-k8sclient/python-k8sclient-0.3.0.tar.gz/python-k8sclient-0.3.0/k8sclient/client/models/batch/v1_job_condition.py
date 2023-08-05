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


class V1JobCondition(object):
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
            'status': 'str',
            'last_probe_time': 'str',
            'last_transition_time': 'str',
            'reason': 'str',
            'message': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'status': 'status',
            'last_probe_time': 'lastProbeTime',
            'last_transition_time': 'lastTransitionTime',
            'reason': 'reason',
            'message': 'message'
        }

        self._type = None
        self._status = None
        self._last_probe_time = None
        self._last_transition_time = None
        self._reason = None
        self._message = None

    @property
    def type(self):
        """
        Gets the type of this V1JobCondition.
        Type of job condition, Complete or Failed.

        :return: The type of this V1JobCondition.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this V1JobCondition.
        Type of job condition, Complete or Failed.

        :param type: The type of this V1JobCondition.
        :type: str
        """
        self._type = type

    @property
    def status(self):
        """
        Gets the status of this V1JobCondition.
        Status of the condition, one of True, False, Unknown.

        :return: The status of this V1JobCondition.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this V1JobCondition.
        Status of the condition, one of True, False, Unknown.

        :param status: The status of this V1JobCondition.
        :type: str
        """
        self._status = status

    @property
    def last_probe_time(self):
        """
        Gets the last_probe_time of this V1JobCondition.
        Last time the condition was checked.

        :return: The last_probe_time of this V1JobCondition.
        :rtype: str
        """
        return self._last_probe_time

    @last_probe_time.setter
    def last_probe_time(self, last_probe_time):
        """
        Sets the last_probe_time of this V1JobCondition.
        Last time the condition was checked.

        :param last_probe_time: The last_probe_time of this V1JobCondition.
        :type: str
        """
        self._last_probe_time = last_probe_time

    @property
    def last_transition_time(self):
        """
        Gets the last_transition_time of this V1JobCondition.
        Last time the condition transit from one status to another.

        :return: The last_transition_time of this V1JobCondition.
        :rtype: str
        """
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, last_transition_time):
        """
        Sets the last_transition_time of this V1JobCondition.
        Last time the condition transit from one status to another.

        :param last_transition_time: The last_transition_time of this V1JobCondition.
        :type: str
        """
        self._last_transition_time = last_transition_time

    @property
    def reason(self):
        """
        Gets the reason of this V1JobCondition.
        (brief) reason for the condition's last transition.

        :return: The reason of this V1JobCondition.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this V1JobCondition.
        (brief) reason for the condition's last transition.

        :param reason: The reason of this V1JobCondition.
        :type: str
        """
        self._reason = reason

    @property
    def message(self):
        """
        Gets the message of this V1JobCondition.
        Human readable message indicating details about last transition.

        :return: The message of this V1JobCondition.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this V1JobCondition.
        Human readable message indicating details about last transition.

        :param message: The message of this V1JobCondition.
        :type: str
        """
        self._message = message

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
