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


class V1PersistentVolume(object):
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
            'metadata': 'V1ObjectMeta',
            'spec': 'V1PersistentVolumeSpec',
            'status': 'V1PersistentVolumeStatus'
        }

        self.attribute_map = {
            'kind': 'kind',
            'api_version': 'apiVersion',
            'metadata': 'metadata',
            'spec': 'spec',
            'status': 'status'
        }

        self._kind = None
        self._api_version = None
        self._metadata = None
        self._spec = None
        self._status = None

    @property
    def kind(self):
        """
        Gets the kind of this V1PersistentVolume.
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :return: The kind of this V1PersistentVolume.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this V1PersistentVolume.
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#types-kinds

        :param kind: The kind of this V1PersistentVolume.
        :type: str
        """
        self._kind = kind

    @property
    def api_version(self):
        """
        Gets the api_version of this V1PersistentVolume.
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#resources

        :return: The api_version of this V1PersistentVolume.
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """
        Sets the api_version of this V1PersistentVolume.
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#resources

        :param api_version: The api_version of this V1PersistentVolume.
        :type: str
        """
        self._api_version = api_version

    @property
    def metadata(self):
        """
        Gets the metadata of this V1PersistentVolume.
        Standard object's metadata. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#metadata

        :return: The metadata of this V1PersistentVolume.
        :rtype: V1ObjectMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this V1PersistentVolume.
        Standard object's metadata. More info: http://releases.k8s.io/release-1.2/docs/devel/api-conventions.md#metadata

        :param metadata: The metadata of this V1PersistentVolume.
        :type: V1ObjectMeta
        """
        self._metadata = metadata

    @property
    def spec(self):
        """
        Gets the spec of this V1PersistentVolume.
        Spec defines a specification of a persistent volume owned by the cluster. Provisioned by an administrator. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistent-volumes

        :return: The spec of this V1PersistentVolume.
        :rtype: V1PersistentVolumeSpec
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """
        Sets the spec of this V1PersistentVolume.
        Spec defines a specification of a persistent volume owned by the cluster. Provisioned by an administrator. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistent-volumes

        :param spec: The spec of this V1PersistentVolume.
        :type: V1PersistentVolumeSpec
        """
        self._spec = spec

    @property
    def status(self):
        """
        Gets the status of this V1PersistentVolume.
        Status represents the current information/status for the persistent volume. Populated by the system. Read-only. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistent-volumes

        :return: The status of this V1PersistentVolume.
        :rtype: V1PersistentVolumeStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this V1PersistentVolume.
        Status represents the current information/status for the persistent volume. Populated by the system. Read-only. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistent-volumes

        :param status: The status of this V1PersistentVolume.
        :type: V1PersistentVolumeStatus
        """
        self._status = status

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
