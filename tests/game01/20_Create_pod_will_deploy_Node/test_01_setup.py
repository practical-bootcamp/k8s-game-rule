# test_01_setup.py
import pytest
import logging
from tests.helper.k8s_client_helper import configure_k8s_client

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
