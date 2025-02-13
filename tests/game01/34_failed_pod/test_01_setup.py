# test_01_setup.py
import logging

from kubernetes import client, config

from tests.helper.k8s_client_helper import configure_k8s_client


def create_resource_quota_manifest(namespace):
    return {
        "apiVersion": "v1",
        "kind": "ResourceQuota",
        "metadata": {"name": "resource-quota", "namespace": namespace},
        "spec": {
            "hard": {
                "requests.cpu": "1",
                "requests.memory": "1Gi",
                "limits.cpu": "2",
                "limits.memory": "2Gi",
            }
        },
    }


def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)
    namespace_name = "one"

    # 检查命名空间是否存在
    try:
        k8s_client.read_namespace(name=namespace_name)
        logging.info(f"Namespace '{namespace_name}' already exists.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            # 创建命名空间
            namespace_manifest = client.V1Namespace(
                api_version="v1",
                kind="Namespace",
                metadata=client.V1ObjectMeta(name=namespace_name),
            )
            k8s_client.create_namespace(body=namespace_manifest)
            logging.info(f"Namespace '{namespace_name}' created successfully.")
        else:
            raise e

    # 创建 ResourceQuota 对象
    resource_quota_manifest = create_resource_quota_manifest(namespace_name)

    # 应用 ResourceQuota
    try:
        k8s_client.create_namespaced_resource_quota(
            namespace=namespace_name, body=resource_quota_manifest
        )
        logging.info(
            f"ResourceQuota 'resource-quota' created successfully in namespace '{namespace_name}'."
        )
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logging.info(
                f"ResourceQuota 'resource-quota' already exists in namespace '{namespace_name}'."
            )
        else:
            raise e


# 运行测试
if __name__ == "__main__":
    pytest.main()
