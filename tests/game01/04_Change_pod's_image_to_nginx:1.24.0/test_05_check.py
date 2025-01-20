import logging

import pytest
import json  # 确保导入库
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:

    def test_001_pod_attributes_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx"
        pod_namespace = "default"
        pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
        
        assert pod.spec.containers[0].image == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
        assert pod.spec.containers[0].ports[0].container_port == 80, "Pod containerPort is not 80"
        assert pod.metadata.namespace == "default", "Pod namespace is not default"
        assert pod.metadata.name == "nginx", "Pod name is not nginx"

    def test_002_pod_attributes_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        # Single command to fetch all necessary information in JSON format
        command = "kubectl get pod nginx -n default -o=json"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        
        pod_info = json.loads(result)
        pod_namespace_result = pod_info["metadata"]["namespace"]
        pod_name_result = pod_info["metadata"]["name"]
        pod_image_result = pod_info["spec"]["containers"][0]["image"]
        pod_port_result = pod_info["spec"]["containers"][0]["ports"][0]["containerPort"]
        
        assert pod_namespace_result == "default", "Pod namespace is not default"
        assert pod_name_result == "nginx", "Pod name is not nginx"
        assert pod_image_result == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
        assert pod_port_result == 80, "Pod containerPort is not 80"
