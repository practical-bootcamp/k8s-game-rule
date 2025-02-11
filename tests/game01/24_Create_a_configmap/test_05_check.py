# test_05_check_configmap.py
import logging
import pytest
import json
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheckConfigMap:
    def test_001_check_configmap_client(self, json_input):
        k8s_client = configure_k8s_client(json_input)

        # 获取ConfigMap
        configmap_name = "config"
        namespace = json_input["namespace"]
        
        try:
            configmap = k8s_client.read_namespaced_config_map(name=configmap_name, namespace=namespace)
        except Exception as e:
            assert False, f"Failed to get ConfigMap '{configmap_name}': {str(e)}"

        # 验证ConfigMap的内容
        assert configmap.api_version == "v1", "Incorrect apiVersion."
        assert configmap.kind == "ConfigMap", "Incorrect kind."
        assert configmap.metadata.name == configmap_name, "Incorrect metadata.name."
        assert "foo" in configmap.data, "Missing key 'foo' in data."
        assert configmap.data["foo"] == "lala", "Incorrect value for 'foo'."
        assert "foo2" in configmap.data, "Missing key 'foo2' in data."
        assert configmap.data["foo2"] == "lolo", "Incorrect value for 'foo2'."
        logging.info(f"ConfigMap '{configmap_name}' has the correct content.")

    def test_002_check_configmap_kubectl(self, json_input):
        logging.debug("Starting test_002_check_configmap_kubectl")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        # 使用kubectl获取ConfigMap
        command = f"kubectl get configmap config -n {json_input['namespace']} -o json"
        result = run_kubectl_command(kube_config, command)
        
        # 解析kubectl输出的JSON内容
        configmap = json.loads(result)
        
        # 验证ConfigMap的内容
        assert configmap["apiVersion"] == "v1", "Incorrect apiVersion."
        assert configmap["kind"] == "ConfigMap", "Incorrect kind."
        assert configmap["metadata"]["name"] == "config", "Incorrect metadata.name."
        assert "foo" in configmap["data"], "Missing key 'foo' in data."
        assert configmap["data"]["foo"] == "lala", "Incorrect value for 'foo'."
        assert "foo2" in configmap["data"], "Missing key 'foo2' in data."
        assert configmap["data"]["foo2"] == "lolo", "Incorrect value for 'foo2'."
        logging.info(f"ConfigMap 'config' has the correct content.")

# 运行测试
if __name__ == "__main__":
    pytest.main()
