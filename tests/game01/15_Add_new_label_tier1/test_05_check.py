# test_05_check.py
import logging
import pytest
import json
from kubernetes.client.rest import ApiException
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_label_tier_web_added_with_library(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        try:
            pods = k8s_client.list_namespaced_pod(namespace=pod_namespace)
            for pod in pods.items:
                labels = pod.metadata.labels if pod.metadata.labels is not None else {}
                if labels.get("app") in ["v2", "v1"]:
                    assert labels.get("tier") == "web", f"Pod '{pod.metadata.name}' with label 'app={labels.get('app')}' does not have the label 'tier=web'"
                    logging.info(f"Pod '{pod.metadata.name}' with label 'app={labels.get('app')}' has the label 'tier=web'")
        except ApiException as e:
            if e.status == 404:
                logging.info(f"No pods found in namespace '{pod_namespace}', skipping check.")
            else:
                raise

    def test_002_verify_label_tier_web_added_with_kubectl(self, json_input):
        logging.debug("Starting test_002_verify_label_tier_web_added_with_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        pod_namespace = json_input["namespace"]

        try:
            command = f"kubectl get pods -n {pod_namespace} -o json"
            logging.debug(f"Running command: {command}")
            result = run_kubectl_command(kube_config, command)
            logging.debug(f"Command result: {result}")
            
            json_output = result.strip()
            logging.debug(f"Command output: {json_output}")
            logging.info(json_output)
        
            pods_data = json.loads(json_output)
            for pod in pods_data["items"]:
                labels = pod["metadata"].get("labels", {})
                if labels.get("app") in ["v2", "v1"]:
                    assert labels.get("tier") == "web", f"Pod '{pod['metadata']['name']}' with label 'app={labels.get('app')}' does not have the label 'tier=web'"
                    logging.info(f"Pod '{pod['metadata']['name']}' with label 'app={labels.get('app')}' has the label 'tier=web'")
        except CalledProcessError as e:
            if 'not found' in str(e).lower():
                logging.info(f"No pods found in namespace '{pod_namespace}', skipping check.")
            else:
                raise
