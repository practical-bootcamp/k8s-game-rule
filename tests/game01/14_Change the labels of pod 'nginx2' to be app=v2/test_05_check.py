# test_05_check.py
import logging
import pytest
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(5)
class TestCheck:
    def test_001_pod_labels_with_library(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx2"
        pod_namespace = json_input["namespace"]
        
        pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
        assert pod.metadata.labels["app"] == "v2", f"Pod '{pod_name}' label is not 'app=v2'"

    def test_002_pod_labels_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"],
            json_input["key_file"],
            json_input["host"]
        )
        command = f"kubectl get pod {pod_name} -n {pod_namespace} -o json"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        
        pod_data = json.loads(result)
        assert pod_data["metadata"]["labels"]["app"] == "v2", f"Pod '{pod_data['metadata']['name']}' label is not 'app=v2'"
