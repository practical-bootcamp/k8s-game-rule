# test_01_setup.py
import pytest
import logging
from tests.helper.k8s_client_helper import configure_k8s_client

def create_pod_manifest(pod_name, label, namespace):
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name,
            "labels": {
                "app": label
            },
            "namespace": namespace
        },
        "spec": {
            "containers": [{
                "name": "nginx",
                "image": "nginx:latest"
            }]
        }
    }

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)
    pod_namespace = json_input["namespace"]

    pod_manifests = [
        create_pod_manifest("nginx1", "v1", pod_namespace),
        create_pod_manifest("nginx2", "v2", pod_namespace),
        create_pod_manifest("nginx3", "v1", pod_namespace)
    ]

    for pod_manifest in pod_manifests:
        response = k8s_client.create_namespaced_pod(namespace=pod_namespace, body=pod_manifest)
        logging.info(f"Created Pod: {pod_manifest['metadata']['name']} response: {response}")
