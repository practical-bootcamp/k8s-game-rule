# test_05_check.py
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


@pytest.mark.order(5)
class TestCheck:
    def test_001_check_label(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            if pod.metadata.labels["app"] in ["v1", "v2"]:
                assert "tier" in pod.metadata.labels and pod.metadata.labels["tier"] == "web", f"Pod '{pod_name}' does not have the label 'tier=web'"
                logging.info(f"Pod '{pod_name}' has the label 'tier=web'")


    def test_002_verify_new_label(self, json_input):
        logging.debug("Starting test_002_verify_new_label")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        pod_namespace = json_input["namespace"]
        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod_name in pod_names:
            command = f"kubectl get pod {pod_name} -n {pod_namespace} -o json"
            logging.debug(f"Running command: {command}")
            result = run_kubectl_command(kube_config, command)
            logging.debug(f"Command result: {result}")
            
            if "error" in result.lower():
                logging.error(f"Command failed with error: {result}")
            else:
                json_output = result.strip()
                logging.debug(f"Command output: {json_output}")
                logging.info(json_output)
            
                pod_data = json.loads(json_output)
                
                assert pod_data["metadata"]["labels"].get("tier") == "web", f"Pod '{pod_name}' does not have the label 'tier=web'"
                logging.info(f"Pod '{pod_name}' has the label 'tier=web'")


