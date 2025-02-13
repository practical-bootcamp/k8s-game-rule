import json
import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:
    def test_001_check_resourcequota_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        quota_name = "resource-quota"
        namespace = "one"

        try:
            quota = k8s_client.read_namespaced_resource_quota(
                name=quota_name, namespace=namespace
            )
        except Exception as e:
            assert False, f"Failed to get ResourceQuota '{quota_name}': {str(e)}"

        # 验证ResourceQuota的内容
        assert quota.api_version == "v1", "Incorrect apiVersion."
        assert quota.kind == "ResourceQuota", "Incorrect kind."
        assert quota.metadata.name == quota_name, "Incorrect metadata.name."
        assert quota.metadata.namespace == namespace, "Incorrect metadata.namespace."

        # 检查ResourceQuota的资源请求和限制
        hard_limits = quota.spec.hard
        assert hard_limits["requests.cpu"] == "1", "Incorrect requests.cpu limit."
        assert (
            hard_limits["requests.memory"] == "1Gi"
        ), "Incorrect requests.memory limit."
        assert hard_limits["limits.cpu"] == "2", "Incorrect limits.cpu limit."
        assert hard_limits["limits.memory"] == "2Gi", "Incorrect limits.memory limit."

        logging.info(
            f"ResourceQuota '{quota_name}' in Namespace '{namespace}' has the correct resource requests and limits."
        )

    def test_002_check_resourcequota_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_resourcequota_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get resourcequota resource-quota -n one -o json"
        result = run_kubectl_command(kube_config, command)
        quota = json.loads(result)

        # 验证ResourceQuota的内容
        assert quota["apiVersion"] == "v1", "Incorrect apiVersion."
        assert quota["kind"] == "ResourceQuota", "Incorrect kind."
        assert quota["metadata"]["name"] == "resource-quota", "Incorrect metadata.name."
        assert quota["metadata"]["namespace"] == "one", "Incorrect metadata.namespace."

        # 检查ResourceQuota的资源请求和限制
        hard_limits = quota["spec"]["hard"]
        assert hard_limits["requests.cpu"] == "1", "Incorrect requests.cpu limit."
        assert (
            hard_limits["requests.memory"] == "1Gi"
        ), "Incorrect requests.memory limit."
        assert hard_limits["limits.cpu"] == "2", "Incorrect limits.cpu limit."
        assert hard_limits["limits.memory"] == "2Gi", "Incorrect limits.memory limit."

        logging.info(
            f"ResourceQuota 'resource-quota' in Namespace 'one' has the correct resource requests and limits."
        )


# 运行测试
if __name__ == "__main__":
    pytest.main()
