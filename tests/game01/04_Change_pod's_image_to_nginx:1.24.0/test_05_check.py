import logging
import pytest
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

