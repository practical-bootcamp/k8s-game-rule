# test_01_setup.py
import pytest
import logging
from kubernetes import client, config
from tests.helper.k8s_client_helper import configure_k8s_client

def create_serviceaccount_manifest():
    return {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {
            "name": "myuser",
            "namespace": "default"
        }
    }

def create_pod_manifest():
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "nginx-pod",
            "namespace": "default"
        },
        "spec": {
            "serviceAccountName": "myuser",
            "containers": [{
                "name": "nginx",
                "image": "nginx",
                "livenessProbe": {
                    "exec": {
                        "command": ["ls"]
                    },
                    "initialDelaySeconds": 5,
                    "periodSeconds": 5
                }
            }]
        }
    }

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)

    # 创建 ServiceAccount
    sa_manifest = create_serviceaccount_manifest()
    try:
        k8s_client.create_namespaced_service_account(namespace="default", body=sa_manifest)
        logging.info(f"ServiceAccount 'myuser' created successfully in namespace 'default'.")
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logging.info("ServiceAccount 'myuser' already exists in namespace 'default'.")
        else:
            raise e

    # 创建 Pod
    pod_manifest = create_pod_manifest()
    try:
        k8s_client.create_namespaced_pod(namespace="default", body=pod_manifest)
        logging.info(f"Pod 'nginx-pod' created successfully in namespace 'default'.")
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logging.info("Pod 'nginx-pod' already exists in namespace 'default'.")
        else:
            raise e

# 运行测试
if __name__ == "__main__":
    pytest.main()
