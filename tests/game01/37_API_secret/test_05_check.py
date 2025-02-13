import json
import logging
from base64 import b64decode

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:
    def test_001_check_namespace(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace_name = "ilovestudy"

        try:
            namespace = k8s_client.read_namespace(name=namespace_name)
        except Exception as e:
            assert False, f"Failed to get Namespace '{namespace_name}': {str(e)}"

        assert namespace.metadata.name == namespace_name, "Incorrect metadata.name."
        logging.info(f"Namespace '{namespace_name}' exists.")

    def test_002_check_secret_via_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        secret_name = "ilovek8s"
        namespace = "ilovestudy"

        try:
            secret = k8s_client.read_namespaced_secret(
                name=secret_name, namespace=namespace
            )
        except Exception as e:
            assert False, f"Failed to get Secret '{secret_name}': {str(e)}"

        # 验证Secret的内容
        assert secret.api_version == "v1", "Incorrect apiVersion."
        assert secret.kind == "Secret", "Incorrect kind."
        assert secret.metadata.name == secret_name, "Incorrect metadata.name."
        assert secret.metadata.namespace == namespace, "Incorrect metadata.namespace."
        assert "API_KEY" in secret.data, "Missing key 'API_KEY' in Secret data."
        assert (
            b64decode(secret.data["API_KEY"]).decode("utf-8") == "ilovek8s"
        ), "Incorrect value for 'API_KEY' in Secret data."

        logging.info(
            f"Secret '{secret_name}' in Namespace '{namespace}' has the correct value for 'API_KEY'."
        )

    def test_003_check_secret_via_kubectl(self, json_input):
        logging.debug("Starting test_003_check_secret_via_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get secret ilovek8s -n ilovestudy -o json"
        result = run_kubectl_command(kube_config, command)
        secret = json.loads(result)

        # 验证Secret的内容
        assert secret["apiVersion"] == "v1", "Incorrect apiVersion."
        assert secret["kind"] == "Secret", "Incorrect kind."
        assert secret["metadata"]["name"] == "ilovek8s", "Incorrect metadata.name."
        assert (
            secret["metadata"]["namespace"] == "ilovestudy"
        ), "Incorrect metadata.namespace."
        assert "API_KEY" in secret["data"], "Missing key 'API_KEY' in Secret data."
        assert (
            b64decode(secret["data"]["API_KEY"]).decode("utf-8") == "ilovek8s"
        ), "Incorrect value for 'API_KEY' in Secret data."

        logging.info(
            f"Secret 'ilovek8s' in Namespace 'ilovestudy' has the correct value for 'API_KEY'."
        )


# 运行测试
if __name__ == "__main__":
    pytest.main()
