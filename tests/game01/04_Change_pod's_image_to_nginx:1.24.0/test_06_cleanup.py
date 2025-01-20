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
        
        pod_namespace = "default"
        pod_name = "nginx"
        
        # 恢复 Pod 的图像为默认版本，在这里假设默认版本是 nginx:1.23.0
        command = f"kubectl set image pod/{pod_name} nginx=nginx:1.23.0 -n {pod_namespace}"
        result = run_kubectl_command(kube_config, command)
        
        logging.info(result)
        assert "pod/nginx image updated" in result.lower(), f"Failed to reset image of Pod '{pod_name}' in namespace '{pod_namespace}'"
        
        # 检查并记录结果
        command = f"kubectl get pod {pod_name} -n {pod_namespace} -o json"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        assert "nginx:1.23.0" in result, f"Pod '{pod_name}' image not reset to default in namespace '{pod_namespace}'"
