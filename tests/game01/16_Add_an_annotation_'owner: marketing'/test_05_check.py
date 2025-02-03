# test_05_check.py
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_annotation_with_library(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            if pod.metadata.labels.get("app") == "v2":
                assert pod.metadata.annotations.get("owner") == "marketing", f"Pod '{pod_name}' does not have the annotation 'owner=marketing'"
                logging.info(f"Pod '{pod_name}' has the annotation 'owner=marketing'")

    def test_002_verify_new_annotation(self, json_input):
        logging.debug("Starting test_002_verify_new_annotation")
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            logging.debug(f"Running command: read_namespaced_pod for {pod_name}")
            logging.debug(f"Command result: {pod}")
            
            if pod:
                logging.debug(f"Current annotations for {pod_name}: {pod.metadata.annotations}")
                
                if pod.metadata.labels.get("app") == "v2":
                    assert pod.metadata.annotations.get("owner") == "marketing", f"Pod '{pod_name}' does not have the annotation 'owner=marketing'"
                    logging.info(f"Pod '{pod_name}' has the annotation 'owner=marketing'")
