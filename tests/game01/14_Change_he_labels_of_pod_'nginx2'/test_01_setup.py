# test_01_setup.py
import pytest
import logging
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)
    pod_names = ["nginx1", "nginx2", "nginx3"]
    pod_namespace = json_input["namespace"]

    for pod_name in pod_names:
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": pod_name,
                "labels": {
                    "app": "v1"
                },
                "namespace": pod_namespace
            },
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx:latest"
                }]
            }
        }
        response = k8s_client.create_namespaced_pod(namespace=pod_namespace, body=pod_manifest)
        logging.info(f"Created Pod: {pod_name} response: {response}")
