import logging
from launchpad import context, Program
from kubernetes import client, config
from tlaunch.lp_k8s.client import validate_name

K8S_API_GROUP = "tartrl.cn"
K8S_API_VERSION =  "v1alpha1"
K8S_API_PLURAL = "lpjobs"


def stop(program_name: str = None, namespace: str = "default"):
    config.load_incluster_config()
    kube_api = client.CustomObjectsApi()
    if program_name is None:
        launch_config = context.get_context().launch_config
        namespace = launch_config["kube_namespace"]
        program_name = launch_config["lpjob_name"]
    kube_api.delete_namespaced_custom_object(
        K8S_API_GROUP,
        K8S_API_VERSION,
        namespace,
        K8S_API_PLURAL,
        validate_name(program_name))
    logging.info(f"An lpjob named '{program_name}' has been deleted in namespace '{namespace}'")
