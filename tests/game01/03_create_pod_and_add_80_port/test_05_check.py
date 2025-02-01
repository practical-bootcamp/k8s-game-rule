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
        pod_names = [pod.metadata.name for pod in pods.items]
        assert pod_name in pod_names, f"Pod '{pod_name}' does not exist in namespace '{pod_namespace}'"

    def test_002_pod_attributes_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"],
            json_input["key_file"],
            json_input["host"]
        )
        pod_name = "nginx"
        pod_namespace = "default"
        command = f"kubectl get pod {pod_name} -n {pod_namespace} -o json"
        try:
            result = run_kubectl_command(kube_config, command)
            logging.info(result)
            pod_data = json.loads(result)
            assert pod_data["spec"]["containers"][0]["image"] == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
            assert pod_data["spec"]["containers"][0]["ports"][0]["containerPort"] == 80, "Pod containerPort is not 80"
            assert pod_data["metadata"]["namespace"] == "default", "Pod namespace is not default"
            assert pod_data["metadata"]["name"] == "nginx", "Pod name is not nginx"
        except Exception as e:
            logging.error(f"Failed to execute command '{command}': {e}")
