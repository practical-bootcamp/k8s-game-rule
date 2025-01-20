import logging

import json
import pytest
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:

    def test_001_pod_exists_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx"
        pod_namespace = "default"
        pods = k8s_client.list_namespaced_pod(namespace=pod_namespace)
        pod_names = {pod.metadata.name: pod.spec.containers[0].image for pod in pods.items}
        assert pod_name in pod_names, f"Pod '{pod_name}' does not exist in namespace '{pod_namespace}'"
        assert pod_names[pod_name] == "nginx:1.24.0", f"Pod '{pod_name}' does not have image 'nginx:1.24.0'"

    def test_002_pod_exists_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        command = "kubectl get pod nginx -n default -o=json"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        pod_info = json.loads(result)
        
        pod_name_result = pod_info["metadata"]["name"]
        pod_image_result = pod_info["spec"]["containers"][0]["image"]
        
        assert pod_name_result == "nginx", f"Pod '{pod_name}' does not exist in namespace 'default'"
        assert pod_image_result == "nginx:1.24.0", f"Pod '{pod_name}' does not have image 'nginx:1.24.0'"
