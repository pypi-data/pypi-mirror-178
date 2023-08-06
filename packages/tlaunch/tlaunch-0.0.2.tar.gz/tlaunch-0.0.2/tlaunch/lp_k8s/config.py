from typing import Dict, List, Optional, Tuple

from kubernetes import client

from tlaunch.lp_k8s.resource import Resource
from tlaunch.lp_k8s.volume_mount import VolumeMount
from tlaunch.lp_k8s.persistent_volume_claim_volume_source import PersistentVolumeClaimVolumeSource
from tlaunch.lp_k8s.util import map_opt

DEFAULT_PORTS = [('launchpad', 8001)]
DEFAULT_NAME = 'launchpad'
REVERB_IMAGE = 'docker.4pd.io/tlaunch/reverb:base'
DEFAULT_VOLUME_NAME = 'tdata'
DEFAULT_MNT_PATH = '/TData'
DEFAULT_COMMAND = ['bash', '-c', '/TData/code/setup.sh && python3 -u -mtlaunch.lp_k8s.process_entry']
DEBUG_COMMAND = ['bash', '-c', 'sleep 3600']
DEFAULT_PVC_NAME = 'jfsdemo'
DEFAULT_IMAGE_PULL_POLICY = 'IfNotPresent'


class Container:
    def __init__(self,
                 namespace: str,
                 image: Optional[str] = None,
                 command: Optional[List[str]] = None,
                 flags: List[str] = [],
                 resources: Optional[Resource] = None,
                 volume_mounts: Optional[List[VolumeMount]] = None,
                 env: Optional[Dict[str, int]] = None,
                 image_pull_policy: str = None,
                 ports: Optional[List[Tuple[str, int]]] = None):
        self.job_name = DEFAULT_NAME
        self.image = image or REVERB_IMAGE
        self.command = (command or DEFAULT_COMMAND) + flags
        self.resources = resources
        self.volume_mounts = volume_mounts or [
            VolumeMount(name=DEFAULT_VOLUME_NAME, mount_path=DEFAULT_MNT_PATH, sub_path='./' + namespace)]
        self.env = env
        self.image_pull_policy = image_pull_policy or DEFAULT_IMAGE_PULL_POLICY
        self.ports = DEFAULT_PORTS.extend(ports) if ports else DEFAULT_PORTS

    def build(self) -> client.V1Container:
        return client.V1Container(
            name=self.job_name,
            image=self.image,
            image_pull_policy=self.image_pull_policy,
            command=self.command,
            ports=map_opt(
                self.ports,
                lambda x: [client.V1ContainerPort(name=v[0],
                                                  container_port=v[1]) for v in x]
            ),
            resources=map_opt(
                self.resources,
                lambda x: client.V1ResourceRequirements(limits=x.limits,
                                                        requests=x.requests)) \
                if self.resources else None,
            volume_mounts=map_opt(
                self.volume_mounts,
                lambda t: [client.V1VolumeMount(mount_path=v.mount_path,
                                                mount_propagation=v.mount_propagation,
                                                name=v.name,
                                                read_only=v.read_only,
                                                sub_path=v.sub_path,
                                                sub_path_expr=v.sub_path_expr) for v in t]) \
                if self.volume_mounts else None,
            env=map_opt(
                self.env,
                lambda e: [client.V1EnvVar(name=k, value=v)
                           for k, v in e.items()]))

    def set_job_name(self, job_name: str) -> 'Container':
        self.job_name = job_name
        return self


class Volumer:
    def __init__(self,
                 namespace: str,
                 persistent_volume_claim: Optional[PersistentVolumeClaimVolumeSource] = None,
                 name: Optional[str] = None):
        claim_name = namespace + '-' + DEFAULT_PVC_NAME
        self.persistent_volume_claim = persistent_volume_claim or PersistentVolumeClaimVolumeSource(
            claim_name=claim_name)
        self.name = name or DEFAULT_VOLUME_NAME

    def build(self) -> client.V1Volume:
        return client.V1Volume(
            persistent_volume_claim=map_opt(
                self.persistent_volume_claim,
                lambda p: client.V1PersistentVolumeClaimVolumeSource(claim_name=p.claim_name,
                                                                     read_only=p.read_only)) \
                if self.persistent_volume_claim else None,
            name=self.name)


class Config:
    def __init__(self, namespace: str,
                 container: Optional[Container] = None,
                 volumer: Optional[Volumer] = None,
                 **kwargs):
        self.container = container or Container(namespace=namespace)
        self.volumer = volumer or Volumer(namespace=namespace)
        self.kwargs = kwargs

    def build(self) -> client.V1PodSpec:
        return client.V1PodSpec(**self.kwargs, containers=[self.container.build()],
                                volumes=[self.volumer.build()] if self.volumer else None)

    def set_job_name(self, job_name: str) -> 'Config':
        self.container.set_job_name(job_name)
        return self


class DefaultReverbConfig(Config):
    def __init__(self) -> None:
        self.container = Container(image=REVERB_IMAGE)
