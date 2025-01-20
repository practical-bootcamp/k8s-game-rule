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
        
        # 删除 Pod 的命令 
        command = f"kubectl delete pod {pod_name} -n {pod_namespace}"
        
        # 运行命令并记录结果
        result = run_kubectl_command(kube_config, command)
        
        logging.info(result)
        assert "deleted" in result.lower(), f"Failed to delete Pod '{pod_name}' in namespace '{pod_namespace}'"
