import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_add_new_annotation(self, json_input):
        logging.debug("Starting test_001_add_new_annotation")
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_names = ["nginx1", "nginx2", "nginx3"]
        new_annotation = {"owner": "marketing"}

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            logging.debug(f"Current annotations for {pod_name}: {pod.metadata.annotations}")
            if pod.metadata.labels["app"] == "v2":
                updated_annotations = pod.metadata.annotations.copy() if pod.metadata.annotations else {}
                updated_annotations.update(new_annotation)
                k8s_client.patch_namespaced_pod(name=pod_name, namespace=pod_namespace, body={"metadata": {"annotations": updated_annotations}})
                logging.info(f"Updated Annotations for Pod: {pod_name}")

    def test_002_verify_new_annotation(self, json_input):
        logging.debug("Starting test_002_verify_new_annotation")
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
                logging.debug(f"Current annotations for {pod_name}: {pod_data['metadata'].get('annotations', {})}")
                
                if pod_data["metadata"]["labels"].get("app") == "v2":
                    assert pod_data["metadata"].get("annotations", {}).get("owner") == "marketing", f"Pod '{pod_name}' does not have the annotation 'owner=marketing'"
                    logging.info(f"Pod '{pod_name}' has the annotation 'owner=marketing'")
