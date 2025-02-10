import logging
import pytest
from kubernetes import client, config

@pytest.mark.order(1)
def test_setup(json_input):
    # 加载 Kubernetes 配置
    config.load_kube_config(config_file=json_input["kube_config"])

    # 创建 Kubernetes API 客户端
    v1 = client.CoreV1Api()
    rbac_v1 = client.RbacAuthorizationV1Api()

    namespace_name = "one"

    # 检查命名空间是否存在
    try:
        v1.read_namespace(name=namespace_name)
        logging.info(f"Namespace '{namespace_name}' already exists.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            # 创建命名空间
            namespace = client.V1Namespace(
                api_version="v1",
                kind="Namespace",
                metadata=client.V1ObjectMeta(name=namespace_name)
            )
            v1.create_namespace(body=namespace)
            logging.info(f"Namespace '{namespace_name}' created successfully.")
        else:
            raise e

    # 创建 ResourceQuota 对象
    resource_quota = client.V1ResourceQuota(
        api_version="v1",
        kind="ResourceQuota",
        metadata=client.V1ObjectMeta(name="resource-quota", namespace=namespace_name),
        spec=client.V1ResourceQuotaSpec(
            hard={
                "requests.cpu": "1",
                "requests.memory": "1Gi",
                "limits.cpu": "2",
                "limits.memory": "2Gi"
            }
        )
    )

    # 应用 ResourceQuota
    try:
        v1.create_namespaced_resource_quota(namespace=namespace_name, body=resource_quota)
        logging.info(f"ResourceQuota 'resource-quota' created successfully in namespace '{namespace_name}'.")
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logging.info(f"ResourceQuota 'resource-quota' already exists in namespace '{namespace_name}'.")
        else:
            raise e

# 运行测试
if __name__ == "__main__":
    pytest.main()
