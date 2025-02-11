import logging
import pytest
import json
from base64 import b64decode
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_secret_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        secret_name = "mysecret"
        namespace = "default" # 请确保命名空间与 Secret 配置中的一致

        try:
            secret = k8s_client.read_namespaced_secret(name=secret_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get Secret '{secret_name}': {str(e)}"

        # 验证Secret的内容
        assert secret.api_version == "v1", "Incorrect apiVersion."
        assert secret.kind == "Secret", "Incorrect kind."
        assert secret.metadata.name == secret_name, "Incorrect metadata.name."
        assert secret.metadata.namespace == namespace, "Incorrect metadata.namespace."
        assert "password" in secret.data, "Missing key 'password' in Secret data."
        assert b64decode(secret.data["password"]).decode('utf-8') == "mypass", "Incorrect value for 'password' in Secret data."

        logging.info(f"Secret '{secret_name}' in Namespace '{namespace}' has the correct value for 'password'.")

    def test_002_check_secret_via_kubectl(self, json_input):
        logging.debug("Starting test_002_check_secret_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get secret mysecret -n default -o json"
        result = run_kubectl_command(kube_config, command)
        secret = json.loads(result)

        # 验证Secret的内容
        assert secret["apiVersion"] == "v1", "Incorrect apiVersion."
        assert secret["kind"] == "Secret", "Incorrect kind."
        assert secret["metadata"]["name"] == "mysecret", "Incorrect metadata.name."
        assert secret["metadata"]["namespace"] == "default", "Incorrect metadata.namespace."
        assert "password" in secret["data"], "Missing key 'password' in Secret data."
        assert b64decode(secret["data"]["password"]).decode('utf-8') == "mypass", "Incorrect value for 'password' in Secret data."

        logging.info(f"Secret 'mysecret' in Namespace 'default' has the correct value for 'password'.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
