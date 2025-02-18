import json
import logging
import base64

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

class TestCheck:
    def test_001_check_secret_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        namespace = json_input["namespace"]
        secret_name = "mysecret"

        logging.info(f"Using namespace: {namespace}")
        logging.info(f"Checking Secret '{secret_name}' in namespace '{namespace}' using client")

        # 验证 Secret
        try:
            secret = k8s_client.read_namespaced_secret(name=secret_name, namespace=namespace)
        except Exception as e:
            logging.error(f"Failed to get Secret '{secret_name}': {str(e)}")
            assert False, f"Failed to get Secret '{secret_name}': {str(e)}"

        # 验证 Secret 中的密码值
        password_value = base64.b64decode(secret.data["password"]).decode()
        assert password_value == "mypass", f"Expected password to be 'mypass', but got '{password_value}'."
        logging.info(f"Secret '{secret_name}' has the correct password value.")

    def test_002_check_secret_kubectl(self, json_input):
        logging.debug("Starting test_002_check_secret_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        namespace = json_input["namespace"]
        secret_name = "mysecret"

        logging.info(f"Using namespace: {namespace}")
        logging.info(f"Checking Secret '{secret_name}' in namespace '{namespace}' using kubectl")

        # 使用 kubectl 获取 Secret
        command = f"kubectl get secret {secret_name} -n {namespace} -o json"
        result = run_kubectl_command(kube_config, command)

        # 解析 kubectl 输出的 JSON 内容
        secret = json.loads(result)

        # 验证 Secret 的内容
        assert secret["apiVersion"] == "v1", "Incorrect apiVersion."
        assert secret["kind"] == "Secret", "Incorrect kind."
        assert secret["metadata"]["name"] == secret_name, "Incorrect metadata.name."

        # 验证 Secret 中的密码值
        password_value = base64.b64decode(secret["data"]["password"]).decode()
        assert password_value == "mypass", f"Expected password to be 'mypass', but got '{password_value}'."
        logging.info(f"Secret '{secret_name}' has the correct password value.")
