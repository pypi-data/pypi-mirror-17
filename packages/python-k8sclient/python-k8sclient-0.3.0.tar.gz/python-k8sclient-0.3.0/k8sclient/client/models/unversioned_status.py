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


class UnversionedStatus(object):
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
            'kind': 'str',
            'api_version': 'str',
            'metadata': 'UnversionedListMeta',
            'status': 'str',
            'message': 'str',
            'reason': 'str',
            'details': 'UnversionedStatusDetails',
            'code': 'int'
        }

        self.attribute_map = {
            'kind': 'kind',
            'api_version': 'apiVersion',
            'metadata': 'metadata',
            'status': 'status',
            'message': 'message',
            'reason': 'reason',
            'details': 'details',
            'code': 'code'
        }

        self._kind = None
        self._api_version = None
        self._metadata = None
        self._status = None
        self._message = None
        self._reason = None
        self._details = None
        self._code = None

    @property
    def kind(self):
        """
        Gets the kind of this UnversionedStatus.
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :return: The kind of this UnversionedStatus.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this UnversionedStatus.
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :param kind: The kind of this UnversionedStatus.
        :type: str
        """
        self._kind = kind

    @property
    def api_version(self):
        """
        Gets the api_version of this UnversionedStatus.
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#resources

        :return: The api_version of this UnversionedStatus.
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """
        Sets the api_version of this UnversionedStatus.
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#resources

        :param api_version: The api_version of this UnversionedStatus.
        :type: str
        """
        self._api_version = api_version

    @property
    def metadata(self):
        """
        Gets the metadata of this UnversionedStatus.
        Standard list metadata. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :return: The metadata of this UnversionedStatus.
        :rtype: UnversionedListMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this UnversionedStatus.
        Standard list metadata. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :param metadata: The metadata of this UnversionedStatus.
        :type: UnversionedListMeta
        """
        self._metadata = metadata

    @property
    def status(self):
        """
        Gets the status of this UnversionedStatus.
        Status of the operation. One of: \"Success\" or \"Failure\". More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#spec-and-status

        :return: The status of this UnversionedStatus.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this UnversionedStatus.
        Status of the operation. One of: \"Success\" or \"Failure\". More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#spec-and-status

        :param status: The status of this UnversionedStatus.
        :type: str
        """
        self._status = status

    @property
    def message(self):
        """
        Gets the message of this UnversionedStatus.
        A human-readable description of the status of this operation.

        :return: The message of this UnversionedStatus.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this UnversionedStatus.
        A human-readable description of the status of this operation.

        :param message: The message of this UnversionedStatus.
        :type: str
        """
        self._message = message

    @property
    def reason(self):
        """
        Gets the reason of this UnversionedStatus.
        A machine-readable description of why this operation is in the \"Failure\" status. If this value is empty there is no information available. A Reason clarifies an HTTP status code but does not override it.

        :return: The reason of this UnversionedStatus.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this UnversionedStatus.
        A machine-readable description of why this operation is in the \"Failure\" status. If this value is empty there is no information available. A Reason clarifies an HTTP status code but does not override it.

        :param reason: The reason of this UnversionedStatus.
        :type: str
        """
        self._reason = reason

    @property
    def details(self):
        """
        Gets the details of this UnversionedStatus.
        Extended data associated with the reason.  Each reason may define its own extended details. This field is optional and the data returned is not guaranteed to conform to any schema except that defined by the reason type.

        :return: The details of this UnversionedStatus.
        :rtype: UnversionedStatusDetails
        """
        return self._details

    @details.setter
    def details(self, details):
        """
        Sets the details of this UnversionedStatus.
        Extended data associated with the reason.  Each reason may define its own extended details. This field is optional and the data returned is not guaranteed to conform to any schema except that defined by the reason type.

        :param details: The details of this UnversionedStatus.
        :type: UnversionedStatusDetails
        """
        self._details = details

    @property
    def code(self):
        """
        Gets the code of this UnversionedStatus.
        Suggested HTTP return code for this status, 0 if not set.

        :return: The code of this UnversionedStatus.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this UnversionedStatus.
        Suggested HTTP return code for this status, 0 if not set.

        :param code: The code of this UnversionedStatus.
        :type: int
        """
        self._code = code

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
