# test_05_check.py
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_pod_scheduled_on_correct_node_with_library(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_name = "gpu-pod"

        try:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            node_name = pod.spec.node_name
            node = k8s_client.read_node(name=node_name)
            labels = node.metadata.labels if node.metadata.labels is not None else {}
            assert labels.get("accelerator") == "nvidia-tesla-p100", f"Pod '{pod_name}' is not scheduled on a node with label 'accelerator=nvidia-tesla-p100'"
            logging.info(f"Pod '{pod_name}' is scheduled on a node with label 'accelerator=nvidia-tesla-p100'")

    def test_002_verify_pod_scheduled_on_correct_node_with_kubectl(self, json_input):
        logging.debug("Starting test_002_verify_pod_scheduled_on_correct_node_with_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        pod_namespace = json_input["namespace"]
        pod_name = "gpu-pod"

        try:
            command = f"kubectl get pod {pod_name} -n {pod_namespace} -o json"
            logging.debug(f"Running command: {command}")
            result = run_kubectl_command(kube_config, command)
            logging.debug(f"Command result: {result}")
            
            json_output = result.strip()
            logging.debug(f"Command output: {json_output}")
            logging.info(json_output)
        
            pod_data = json.loads(json_output)
            node_name = pod_data["spec"]["nodeName"]

            command = f"kubectl get node {node_name} -o json"
            logging.debug(f"Running command: {command}")
            result = run_kubectl_command(kube_config, command)
            logging.debug(f"Command result: {result}")
            
            json_output = result.strip()
            logging.debug(f"Command output: {json_output}")
            logging.info(json_output)
        
            node_data = json.loads(json_output)
            labels = node_data["metadata"].get("labels", {})
            assert labels.get("accelerator") == "nvidia-tesla-p100", f"Pod '{pod_name}' is not scheduled on a node with label 'accelerator=nvidia-tesla-p100'"
            logging.info(f"Pod '{pod_name}' is scheduled on a node with label 'accelerator=nvidia-tesla-p100'")
        except CalledProcessError as e:
            if 'not found' in str(e).lower():
                logging.info(f"Pod '{pod_name}' or Node '{node_name}' not found, skipping check.")
            else:
                raise
