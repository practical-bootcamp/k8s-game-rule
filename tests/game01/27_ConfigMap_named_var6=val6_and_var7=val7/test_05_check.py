import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_check_configmap(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        configmap_name = "anotherone"
        namespace = json_input["namespace"]

        try:
            configmap = k8s_client.read_namespaced_config_map(name=configmap_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get ConfigMap '{configmap_name}': {str(e)}"

        # 验证ConfigMap的内容
        assert configmap.api_version == "v1", "Incorrect apiVersion."
        assert configmap.kind == "ConfigMap", "Incorrect kind."
        assert configmap.metadata.name == configmap_name, "Incorrect metadata.name."
        assert "var6" in configmap.data, "Missing key 'var6' in data."
        assert configmap.data["var6"] == "val6", "Incorrect value for 'var6'."
        assert "var7" in configmap.data, "Missing key 'var7' in data."
        assert configmap.data["var7"] == "val7", "Incorrect value for 'var7'."
        logging.info(f"ConfigMap '{configmap_name}' has the correct content.")

    def test_002_check_pod(self, json_input):
        logging.debug("Starting test_002_check_pod")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod nginx -n {json_input['namespace']} -o json"
        result = run_kubectl_command(kube_config, command)
        pod = json.loads(result)

        # 验证Pod的内容
        assert pod["apiVersion"] == "v1", "Incorrect apiVersion."
        assert pod["kind"] == "Pod", "Incorrect kind."
        assert pod["metadata"]["name"] == "nginx", "Incorrect metadata.name."

        # 检查Pod的环境变量
        env_vars = pod["spec"]["containers"][0]["env"]
        env_var_dict = {env["name"]: env["valueFrom"]["configMapKeyRef"]["name"] for env in env_vars if "valueFrom" in env and "configMapKeyRef" in env["valueFrom"]}
        assert "var6" in env_var_dict, "Missing environment variable 'var6' in Pod."
        assert env_var_dict["var6"] == "anotherone", "Incorrect ConfigMap reference for environment variable 'var6'."
        assert "var7" in env_var_dict, "Missing environment variable 'var7' in Pod."
        assert env_var_dict["var7"] == "anotherone", "Incorrect ConfigMap reference for environment variable 'var7'."
        logging.info(f"Pod 'nginx' has the correct environment variables 'var6' and 'var7'.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
