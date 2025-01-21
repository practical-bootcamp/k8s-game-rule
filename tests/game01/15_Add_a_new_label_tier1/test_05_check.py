# test_05_check.py
import logging
import pytest
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(5)
class TestCheck:
    def test_001_add_new_label(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]
        
        pod_names = ["nginx1", "nginx2", "nginx3"]
        new_label = {"tier": "web"}

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            if pod.metadata.labels["app"] in ["v1", "v2"]:
                k8s_client.patch_namespaced_pod(name=pod_name, namespace=pod_namespace, body={"metadata": {"labels": new_label}})
                logging.info(f"Updated Labels for Pod: {pod_name}")

    def test_002_verify_new_label(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        pod_namespace = json_input["namespace"]

        pod_names = ["nginx1", "nginx2", "nginx3"]

        for pod_name in pod_names:
            pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
            if pod.metadata.labels["app"] in ["v1", "v2"]:
                assert pod.metadata.labels["tier"] == "web", f"Pod '{pod_name}' does not have label 'tier=web'"
