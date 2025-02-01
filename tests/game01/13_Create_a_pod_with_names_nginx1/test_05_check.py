import logging
import pytest
import json
import subprocess
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_pod_label_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx1"
        pod_namespace = "default"
        pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
        
        assert pod.metadata.labels.get("app") == "v1", "Pod label 'app' is not 'v1'"
        assert pod.metadata.name == "nginx1", "Pod name is not 'nginx1'"

    def test_002_pod_label_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["$client_certificate"],
            json_input["$client_key"],
            json_input["$endpoint"],
        )
        command = "kubectl get pod nginx1 -n default -o json"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            logging.error(f"Command failed with error: {result.stderr}")
        else:
            json_output = result.stdout.strip()
            logging.info(json_output)
        
            pod_data = json.loads(json_output)
            
            assert pod_data["metadata"]["labels"].get("app") == "v1", "Pod label 'app' is not 'v1'"
            assert pod_data["metadata"]["name"] == "nginx1", "Pod name is not 'nginx1'"