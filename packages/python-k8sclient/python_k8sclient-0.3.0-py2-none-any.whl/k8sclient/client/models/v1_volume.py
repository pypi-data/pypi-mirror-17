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


class V1Volume(object):
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
            'name': 'str',
            'host_path': 'V1HostPathVolumeSource',
            'empty_dir': 'V1EmptyDirVolumeSource',
            'gce_persistent_disk': 'V1GCEPersistentDiskVolumeSource',
            'aws_elastic_block_store': 'V1AWSElasticBlockStoreVolumeSource',
            'git_repo': 'V1GitRepoVolumeSource',
            'secret': 'V1SecretVolumeSource',
            'nfs': 'V1NFSVolumeSource',
            'iscsi': 'V1ISCSIVolumeSource',
            'glusterfs': 'V1GlusterfsVolumeSource',
            'persistent_volume_claim': 'V1PersistentVolumeClaimVolumeSource',
            'rbd': 'V1RBDVolumeSource',
            'flex_volume': 'V1FlexVolumeSource',
            'cinder': 'V1CinderVolumeSource',
            'cephfs': 'V1CephFSVolumeSource',
            'flocker': 'V1FlockerVolumeSource',
            'downward_api': 'V1DownwardAPIVolumeSource',
            'fc': 'V1FCVolumeSource',
            'azure_file': 'V1AzureFileVolumeSource',
            'config_map': 'V1ConfigMapVolumeSource'
        }

        self.attribute_map = {
            'name': 'name',
            'host_path': 'hostPath',
            'empty_dir': 'emptyDir',
            'gce_persistent_disk': 'gcePersistentDisk',
            'aws_elastic_block_store': 'awsElasticBlockStore',
            'git_repo': 'gitRepo',
            'secret': 'secret',
            'nfs': 'nfs',
            'iscsi': 'iscsi',
            'glusterfs': 'glusterfs',
            'persistent_volume_claim': 'persistentVolumeClaim',
            'rbd': 'rbd',
            'flex_volume': 'flexVolume',
            'cinder': 'cinder',
            'cephfs': 'cephfs',
            'flocker': 'flocker',
            'downward_api': 'downwardAPI',
            'fc': 'fc',
            'azure_file': 'azureFile',
            'config_map': 'configMap'
        }

        self._name = None
        self._host_path = None
        self._empty_dir = None
        self._gce_persistent_disk = None
        self._aws_elastic_block_store = None
        self._git_repo = None
        self._secret = None
        self._nfs = None
        self._iscsi = None
        self._glusterfs = None
        self._persistent_volume_claim = None
        self._rbd = None
        self._flex_volume = None
        self._cinder = None
        self._cephfs = None
        self._flocker = None
        self._downward_api = None
        self._fc = None
        self._azure_file = None
        self._config_map = None

    @property
    def name(self):
        """
        Gets the name of this V1Volume.
        Volume's name. Must be a DNS_LABEL and unique within the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/identifiers.md#names

        :return: The name of this V1Volume.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this V1Volume.
        Volume's name. Must be a DNS_LABEL and unique within the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/identifiers.md#names

        :param name: The name of this V1Volume.
        :type: str
        """
        self._name = name

    @property
    def host_path(self):
        """
        Gets the host_path of this V1Volume.
        HostPath represents a pre-existing file or directory on the host machine that is directly exposed to the container. This is generally used for system agents or other privileged things that are allowed to see the host machine. Most containers will NOT need this. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#hostpath

        :return: The host_path of this V1Volume.
        :rtype: V1HostPathVolumeSource
        """
        return self._host_path

    @host_path.setter
    def host_path(self, host_path):
        """
        Sets the host_path of this V1Volume.
        HostPath represents a pre-existing file or directory on the host machine that is directly exposed to the container. This is generally used for system agents or other privileged things that are allowed to see the host machine. Most containers will NOT need this. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#hostpath

        :param host_path: The host_path of this V1Volume.
        :type: V1HostPathVolumeSource
        """
        self._host_path = host_path

    @property
    def empty_dir(self):
        """
        Gets the empty_dir of this V1Volume.
        EmptyDir represents a temporary directory that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#emptydir

        :return: The empty_dir of this V1Volume.
        :rtype: V1EmptyDirVolumeSource
        """
        return self._empty_dir

    @empty_dir.setter
    def empty_dir(self, empty_dir):
        """
        Sets the empty_dir of this V1Volume.
        EmptyDir represents a temporary directory that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#emptydir

        :param empty_dir: The empty_dir of this V1Volume.
        :type: V1EmptyDirVolumeSource
        """
        self._empty_dir = empty_dir

    @property
    def gce_persistent_disk(self):
        """
        Gets the gce_persistent_disk of this V1Volume.
        GCEPersistentDisk represents a GCE Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#gcepersistentdisk

        :return: The gce_persistent_disk of this V1Volume.
        :rtype: V1GCEPersistentDiskVolumeSource
        """
        return self._gce_persistent_disk

    @gce_persistent_disk.setter
    def gce_persistent_disk(self, gce_persistent_disk):
        """
        Sets the gce_persistent_disk of this V1Volume.
        GCEPersistentDisk represents a GCE Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#gcepersistentdisk

        :param gce_persistent_disk: The gce_persistent_disk of this V1Volume.
        :type: V1GCEPersistentDiskVolumeSource
        """
        self._gce_persistent_disk = gce_persistent_disk

    @property
    def aws_elastic_block_store(self):
        """
        Gets the aws_elastic_block_store of this V1Volume.
        AWSElasticBlockStore represents an AWS Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#awselasticblockstore

        :return: The aws_elastic_block_store of this V1Volume.
        :rtype: V1AWSElasticBlockStoreVolumeSource
        """
        return self._aws_elastic_block_store

    @aws_elastic_block_store.setter
    def aws_elastic_block_store(self, aws_elastic_block_store):
        """
        Sets the aws_elastic_block_store of this V1Volume.
        AWSElasticBlockStore represents an AWS Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#awselasticblockstore

        :param aws_elastic_block_store: The aws_elastic_block_store of this V1Volume.
        :type: V1AWSElasticBlockStoreVolumeSource
        """
        self._aws_elastic_block_store = aws_elastic_block_store

    @property
    def git_repo(self):
        """
        Gets the git_repo of this V1Volume.
        GitRepo represents a git repository at a particular revision.

        :return: The git_repo of this V1Volume.
        :rtype: V1GitRepoVolumeSource
        """
        return self._git_repo

    @git_repo.setter
    def git_repo(self, git_repo):
        """
        Sets the git_repo of this V1Volume.
        GitRepo represents a git repository at a particular revision.

        :param git_repo: The git_repo of this V1Volume.
        :type: V1GitRepoVolumeSource
        """
        self._git_repo = git_repo

    @property
    def secret(self):
        """
        Gets the secret of this V1Volume.
        Secret represents a secret that should populate this volume. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#secrets

        :return: The secret of this V1Volume.
        :rtype: V1SecretVolumeSource
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """
        Sets the secret of this V1Volume.
        Secret represents a secret that should populate this volume. More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#secrets

        :param secret: The secret of this V1Volume.
        :type: V1SecretVolumeSource
        """
        self._secret = secret

    @property
    def nfs(self):
        """
        Gets the nfs of this V1Volume.
        NFS represents an NFS mount on the host that shares a pod's lifetime More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#nfs

        :return: The nfs of this V1Volume.
        :rtype: V1NFSVolumeSource
        """
        return self._nfs

    @nfs.setter
    def nfs(self, nfs):
        """
        Sets the nfs of this V1Volume.
        NFS represents an NFS mount on the host that shares a pod's lifetime More info: http://releases.k8s.io/release-1.2/docs/user-guide/volumes.md#nfs

        :param nfs: The nfs of this V1Volume.
        :type: V1NFSVolumeSource
        """
        self._nfs = nfs

    @property
    def iscsi(self):
        """
        Gets the iscsi of this V1Volume.
        ISCSI represents an ISCSI Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/examples/iscsi/README.md

        :return: The iscsi of this V1Volume.
        :rtype: V1ISCSIVolumeSource
        """
        return self._iscsi

    @iscsi.setter
    def iscsi(self, iscsi):
        """
        Sets the iscsi of this V1Volume.
        ISCSI represents an ISCSI Disk resource that is attached to a kubelet's host machine and then exposed to the pod. More info: http://releases.k8s.io/release-1.2/examples/iscsi/README.md

        :param iscsi: The iscsi of this V1Volume.
        :type: V1ISCSIVolumeSource
        """
        self._iscsi = iscsi

    @property
    def glusterfs(self):
        """
        Gets the glusterfs of this V1Volume.
        Glusterfs represents a Glusterfs mount on the host that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/examples/glusterfs/README.md

        :return: The glusterfs of this V1Volume.
        :rtype: V1GlusterfsVolumeSource
        """
        return self._glusterfs

    @glusterfs.setter
    def glusterfs(self, glusterfs):
        """
        Sets the glusterfs of this V1Volume.
        Glusterfs represents a Glusterfs mount on the host that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/examples/glusterfs/README.md

        :param glusterfs: The glusterfs of this V1Volume.
        :type: V1GlusterfsVolumeSource
        """
        self._glusterfs = glusterfs

    @property
    def persistent_volume_claim(self):
        """
        Gets the persistent_volume_claim of this V1Volume.
        PersistentVolumeClaimVolumeSource represents a reference to a PersistentVolumeClaim in the same namespace. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistentvolumeclaims

        :return: The persistent_volume_claim of this V1Volume.
        :rtype: V1PersistentVolumeClaimVolumeSource
        """
        return self._persistent_volume_claim

    @persistent_volume_claim.setter
    def persistent_volume_claim(self, persistent_volume_claim):
        """
        Sets the persistent_volume_claim of this V1Volume.
        PersistentVolumeClaimVolumeSource represents a reference to a PersistentVolumeClaim in the same namespace. More info: http://releases.k8s.io/release-1.2/docs/user-guide/persistent-volumes.md#persistentvolumeclaims

        :param persistent_volume_claim: The persistent_volume_claim of this V1Volume.
        :type: V1PersistentVolumeClaimVolumeSource
        """
        self._persistent_volume_claim = persistent_volume_claim

    @property
    def rbd(self):
        """
        Gets the rbd of this V1Volume.
        RBD represents a Rados Block Device mount on the host that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/examples/rbd/README.md

        :return: The rbd of this V1Volume.
        :rtype: V1RBDVolumeSource
        """
        return self._rbd

    @rbd.setter
    def rbd(self, rbd):
        """
        Sets the rbd of this V1Volume.
        RBD represents a Rados Block Device mount on the host that shares a pod's lifetime. More info: http://releases.k8s.io/release-1.2/examples/rbd/README.md

        :param rbd: The rbd of this V1Volume.
        :type: V1RBDVolumeSource
        """
        self._rbd = rbd

    @property
    def flex_volume(self):
        """
        Gets the flex_volume of this V1Volume.
        FlexVolume represents a generic volume resource that is provisioned/attached using a exec based plugin. This is an alpha feature and may change in future.

        :return: The flex_volume of this V1Volume.
        :rtype: V1FlexVolumeSource
        """
        return self._flex_volume

    @flex_volume.setter
    def flex_volume(self, flex_volume):
        """
        Sets the flex_volume of this V1Volume.
        FlexVolume represents a generic volume resource that is provisioned/attached using a exec based plugin. This is an alpha feature and may change in future.

        :param flex_volume: The flex_volume of this V1Volume.
        :type: V1FlexVolumeSource
        """
        self._flex_volume = flex_volume

    @property
    def cinder(self):
        """
        Gets the cinder of this V1Volume.
        Cinder represents a cinder volume attached and mounted on kubelets host machine More info: http://releases.k8s.io/release-1.2/examples/mysql-cinder-pd/README.md

        :return: The cinder of this V1Volume.
        :rtype: V1CinderVolumeSource
        """
        return self._cinder

    @cinder.setter
    def cinder(self, cinder):
        """
        Sets the cinder of this V1Volume.
        Cinder represents a cinder volume attached and mounted on kubelets host machine More info: http://releases.k8s.io/release-1.2/examples/mysql-cinder-pd/README.md

        :param cinder: The cinder of this V1Volume.
        :type: V1CinderVolumeSource
        """
        self._cinder = cinder

    @property
    def cephfs(self):
        """
        Gets the cephfs of this V1Volume.
        CephFS represents a Ceph FS mount on the host that shares a pod's lifetime

        :return: The cephfs of this V1Volume.
        :rtype: V1CephFSVolumeSource
        """
        return self._cephfs

    @cephfs.setter
    def cephfs(self, cephfs):
        """
        Sets the cephfs of this V1Volume.
        CephFS represents a Ceph FS mount on the host that shares a pod's lifetime

        :param cephfs: The cephfs of this V1Volume.
        :type: V1CephFSVolumeSource
        """
        self._cephfs = cephfs

    @property
    def flocker(self):
        """
        Gets the flocker of this V1Volume.
        Flocker represents a Flocker volume attached to a kubelet's host machine. This depends on the Flocker control service being running

        :return: The flocker of this V1Volume.
        :rtype: V1FlockerVolumeSource
        """
        return self._flocker

    @flocker.setter
    def flocker(self, flocker):
        """
        Sets the flocker of this V1Volume.
        Flocker represents a Flocker volume attached to a kubelet's host machine. This depends on the Flocker control service being running

        :param flocker: The flocker of this V1Volume.
        :type: V1FlockerVolumeSource
        """
        self._flocker = flocker

    @property
    def downward_api(self):
        """
        Gets the downward_api of this V1Volume.
        DownwardAPI represents downward API about the pod that should populate this volume

        :return: The downward_api of this V1Volume.
        :rtype: V1DownwardAPIVolumeSource
        """
        return self._downward_api

    @downward_api.setter
    def downward_api(self, downward_api):
        """
        Sets the downward_api of this V1Volume.
        DownwardAPI represents downward API about the pod that should populate this volume

        :param downward_api: The downward_api of this V1Volume.
        :type: V1DownwardAPIVolumeSource
        """
        self._downward_api = downward_api

    @property
    def fc(self):
        """
        Gets the fc of this V1Volume.
        FC represents a Fibre Channel resource that is attached to a kubelet's host machine and then exposed to the pod.

        :return: The fc of this V1Volume.
        :rtype: V1FCVolumeSource
        """
        return self._fc

    @fc.setter
    def fc(self, fc):
        """
        Sets the fc of this V1Volume.
        FC represents a Fibre Channel resource that is attached to a kubelet's host machine and then exposed to the pod.

        :param fc: The fc of this V1Volume.
        :type: V1FCVolumeSource
        """
        self._fc = fc

    @property
    def azure_file(self):
        """
        Gets the azure_file of this V1Volume.
        AzureFile represents an Azure File Service mount on the host and bind mount to the pod.

        :return: The azure_file of this V1Volume.
        :rtype: V1AzureFileVolumeSource
        """
        return self._azure_file

    @azure_file.setter
    def azure_file(self, azure_file):
        """
        Sets the azure_file of this V1Volume.
        AzureFile represents an Azure File Service mount on the host and bind mount to the pod.

        :param azure_file: The azure_file of this V1Volume.
        :type: V1AzureFileVolumeSource
        """
        self._azure_file = azure_file

    @property
    def config_map(self):
        """
        Gets the config_map of this V1Volume.
        ConfigMap represents a configMap that should populate this volume

        :return: The config_map of this V1Volume.
        :rtype: V1ConfigMapVolumeSource
        """
        return self._config_map

    @config_map.setter
    def config_map(self, config_map):
        """
        Sets the config_map of this V1Volume.
        ConfigMap represents a configMap that should populate this volume

        :param config_map: The config_map of this V1Volume.
        :type: V1ConfigMapVolumeSource
        """
        self._config_map = config_map

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
