import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_serviceaccount_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        sa_name = "myuser"
        namespace = "default"

        try:
            sa = k8s_client.read_namespaced_service_account(name=sa_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get ServiceAccount '{sa_name}': {str(e)}"

        # 验证ServiceAccount的内容
        assert sa.api_version == "v1", "Incorrect apiVersion."
        assert sa.kind == "ServiceAccount", "Incorrect kind."
        assert sa.metadata.name == sa_name, "Incorrect metadata.name."
        assert sa.metadata.namespace == namespace, "Incorrect metadata.namespace."

        logging.info(f"ServiceAccount '{sa_name}' in Namespace '{namespace}' exists and is correctly configured.")

    def test_002_check_serviceaccount_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_serviceaccount_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get serviceaccount myuser -n default -o json"
        result = run_kubectl_command(kube_config, command)
        sa = json.loads(result)

        # 验证ServiceAccount的内容
        assert sa["apiVersion"] == "v1", "Incorrect apiVersion."
        assert sa["kind"] == "ServiceAccount", "Incorrect kind."
        assert sa["metadata"]["name"] == "myuser", "Incorrect metadata.name."
        assert sa["metadata"]["namespace"] == "default", "Incorrect metadata.namespace."

        logging.info(f"ServiceAccount 'myuser' in Namespace 'default' exists and is correctly configured.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
