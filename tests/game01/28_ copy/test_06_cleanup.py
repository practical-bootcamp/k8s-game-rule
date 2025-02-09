import logging
import pytest
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

class TestCleanup:

    @pytest.mark.order(6)
    def test_cleanup(self, json_input):
        # 配置 Kubernetes
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        namespace = json_input["namespace"]

        # 删除 ConfigMap 的命令
        configmap_name = "cmvolume"
        command_configmap = f"kubectl delete configmap {configmap_name} -n {namespace}"
        
        # 运行命令并记录结果
        result_configmap = run_kubectl_command(kube_config, command_configmap)
        logging.info(result_configmap)
        assert "deleted" in result_configmap.lower(), f"Failed to delete ConfigMap '{configmap_name}' in namespace '{namespace}'"

        # 删除 Pod 的命令
        pod_name = "nginx-pod"
        command_pod = f"kubectl delete pod {pod_name} -n {namespace}"
        
        # 运行命令并记录结果
        result_pod = run_kubectl_command(kube_config, command_pod)
        logging.info(result_pod)
        assert "deleted" in result_pod.lower(), f"Failed to delete Pod '{pod_name}' in namespace '{namespace}'"

# 运行测试
if __name__ == "__main__":
    pytest.main()
