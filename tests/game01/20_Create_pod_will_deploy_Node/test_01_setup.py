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

def label_node(k8s_client, node_name, labels):
    body = {
        "metadata": {
            "labels": labels
        }
    }
    return k8s_client.patch_node(node_name, body)

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)
    pod_namespace = json_input["namespace"]
    node_name = "minikube"


    # 检查节点是否存在
    node = k8s_client.read_node(name=node_name)
    logging.info(f"Node '{node_name}' exists.")
        
    # 为节点添加标签
    labels = {
        "accelerator": "nvidia-tesla-p100"
    }
    response = label_node(k8s_client, node_name, labels)
    logging.info(f"Labeled Node '{node_name}' with labels: {labels}, response: {response}")


    pod_manifests = [
        create_pod_manifest("nginx1", "v1", pod_namespace),
        create_pod_manifest("nginx2", "v2", pod_namespace),
        create_pod_manifest("nginx3", "v3", pod_namespace)
    ]

    for pod_manifest in pod_manifests:
        response = k8s_client.create_namespaced_pod(namespace=pod_namespace, body=pod_manifest)
        logging.info(f"Created Pod: {pod_manifest['metadata']['name']} response: {response}")
