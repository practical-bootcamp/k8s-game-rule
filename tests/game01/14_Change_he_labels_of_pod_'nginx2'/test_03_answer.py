# test_03_answer.py
import logging
import pytest
from tests.helper.k8s_client_helper import configure_k8s_client

@pytest.mark.order(3)
def test_answer(json_input):
    k8s_client = configure_k8s_client(json_input)
    pod_name = "nginx2"
    pod_namespace = json_input["namespace"]
    
    # 修改 Pod 标签
    patch = {
        "metadata": {
            "labels": {
                "app": "v2"
            }
        }
    }
    response = k8s_client.patch_namespaced_pod(name=pod_name, namespace=pod_namespace, body=patch)
    logging.info(f"Patched Pod: {pod_name} response: {response}")
