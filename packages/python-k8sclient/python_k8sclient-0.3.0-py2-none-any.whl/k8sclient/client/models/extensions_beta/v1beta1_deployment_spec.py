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


class V1beta1DeploymentSpec(object):
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
            'replicas': 'int',
            'selector': 'V1beta1LabelSelector',
            'template': 'V1PodTemplateSpec',
            'strategy': 'V1beta1DeploymentStrategy',
            'min_ready_seconds': 'int',
            'revision_history_limit': 'int',
            'paused': 'bool',
            'rollback_to': 'V1beta1RollbackConfig'
        }

        self.attribute_map = {
            'replicas': 'replicas',
            'selector': 'selector',
            'template': 'template',
            'strategy': 'strategy',
            'min_ready_seconds': 'minReadySeconds',
            'revision_history_limit': 'revisionHistoryLimit',
            'paused': 'paused',
            'rollback_to': 'rollbackTo'
        }

        self._replicas = None
        self._selector = None
        self._template = None
        self._strategy = None
        self._min_ready_seconds = None
        self._revision_history_limit = None
        self._paused = None
        self._rollback_to = None

    @property
    def replicas(self):
        """
        Gets the replicas of this V1beta1DeploymentSpec.
        Number of desired pods. This is a pointer to distinguish between explicit zero and not specified. Defaults to 1.

        :return: The replicas of this V1beta1DeploymentSpec.
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """
        Sets the replicas of this V1beta1DeploymentSpec.
        Number of desired pods. This is a pointer to distinguish between explicit zero and not specified. Defaults to 1.

        :param replicas: The replicas of this V1beta1DeploymentSpec.
        :type: int
        """
        self._replicas = replicas

    @property
    def selector(self):
        """
        Gets the selector of this V1beta1DeploymentSpec.
        Label selector for pods. Existing ReplicaSets whose pods are selected by this will be the ones affected by this deployment.

        :return: The selector of this V1beta1DeploymentSpec.
        :rtype: V1beta1LabelSelector
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """
        Sets the selector of this V1beta1DeploymentSpec.
        Label selector for pods. Existing ReplicaSets whose pods are selected by this will be the ones affected by this deployment.

        :param selector: The selector of this V1beta1DeploymentSpec.
        :type: V1beta1LabelSelector
        """
        self._selector = selector

    @property
    def template(self):
        """
        Gets the template of this V1beta1DeploymentSpec.
        Template describes the pods that will be created.

        :return: The template of this V1beta1DeploymentSpec.
        :rtype: V1PodTemplateSpec
        """
        return self._template

    @template.setter
    def template(self, template):
        """
        Sets the template of this V1beta1DeploymentSpec.
        Template describes the pods that will be created.

        :param template: The template of this V1beta1DeploymentSpec.
        :type: V1PodTemplateSpec
        """
        self._template = template

    @property
    def strategy(self):
        """
        Gets the strategy of this V1beta1DeploymentSpec.
        The deployment strategy to use to replace existing pods with new ones.

        :return: The strategy of this V1beta1DeploymentSpec.
        :rtype: V1beta1DeploymentStrategy
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """
        Sets the strategy of this V1beta1DeploymentSpec.
        The deployment strategy to use to replace existing pods with new ones.

        :param strategy: The strategy of this V1beta1DeploymentSpec.
        :type: V1beta1DeploymentStrategy
        """
        self._strategy = strategy

    @property
    def min_ready_seconds(self):
        """
        Gets the min_ready_seconds of this V1beta1DeploymentSpec.
        Minimum number of seconds for which a newly created pod should be ready without object of its container crashing, for it to be considered available. Defaults to 0 (pod will be considered available as soon as it is ready)

        :return: The min_ready_seconds of this V1beta1DeploymentSpec.
        :rtype: int
        """
        return self._min_ready_seconds

    @min_ready_seconds.setter
    def min_ready_seconds(self, min_ready_seconds):
        """
        Sets the min_ready_seconds of this V1beta1DeploymentSpec.
        Minimum number of seconds for which a newly created pod should be ready without object of its container crashing, for it to be considered available. Defaults to 0 (pod will be considered available as soon as it is ready)

        :param min_ready_seconds: The min_ready_seconds of this V1beta1DeploymentSpec.
        :type: int
        """
        self._min_ready_seconds = min_ready_seconds

    @property
    def revision_history_limit(self):
        """
        Gets the revision_history_limit of this V1beta1DeploymentSpec.
        The number of old ReplicaSets to retain to allow rollback. This is a pointer to distinguish between explicit zero and not specified.

        :return: The revision_history_limit of this V1beta1DeploymentSpec.
        :rtype: int
        """
        return self._revision_history_limit

    @revision_history_limit.setter
    def revision_history_limit(self, revision_history_limit):
        """
        Sets the revision_history_limit of this V1beta1DeploymentSpec.
        The number of old ReplicaSets to retain to allow rollback. This is a pointer to distinguish between explicit zero and not specified.

        :param revision_history_limit: The revision_history_limit of this V1beta1DeploymentSpec.
        :type: int
        """
        self._revision_history_limit = revision_history_limit

    @property
    def paused(self):
        """
        Gets the paused of this V1beta1DeploymentSpec.
        Indicates that the deployment is paused and will not be processed by the deployment controller.

        :return: The paused of this V1beta1DeploymentSpec.
        :rtype: bool
        """
        return self._paused

    @paused.setter
    def paused(self, paused):
        """
        Sets the paused of this V1beta1DeploymentSpec.
        Indicates that the deployment is paused and will not be processed by the deployment controller.

        :param paused: The paused of this V1beta1DeploymentSpec.
        :type: bool
        """
        self._paused = paused

    @property
    def rollback_to(self):
        """
        Gets the rollback_to of this V1beta1DeploymentSpec.
        The config this deployment is rolling back to. Will be cleared after rollback is done.

        :return: The rollback_to of this V1beta1DeploymentSpec.
        :rtype: V1beta1RollbackConfig
        """
        return self._rollback_to

    @rollback_to.setter
    def rollback_to(self, rollback_to):
        """
        Sets the rollback_to of this V1beta1DeploymentSpec.
        The config this deployment is rolling back to. Will be cleared after rollback is done.

        :param rollback_to: The rollback_to of this V1beta1DeploymentSpec.
        :type: V1beta1RollbackConfig
        """
        self._rollback_to = rollback_to

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
