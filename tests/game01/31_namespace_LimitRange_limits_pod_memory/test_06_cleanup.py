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

        namespace = "limitrange"

        # 删除 LimitRange 的命令
        limitrange_name = "mem-limit-range"
        command_limitrange = f"kubectl delete limitrange {limitrange_name} -n {namespace}"
        
        # 运行命令并记录结果
        result_limitrange = run_kubectl_command(kube_config, command_limitrange)
        logging.info(result_limitrange)
        assert "deleted" in result_limitrange.lower(), f"Failed to delete LimitRange '{limitrange_name}' in namespace '{namespace}'"

        # 删除 Namespace 的命令
        command_namespace = f"kubectl delete namespace {namespace}"
        
        # 运行命令并记录结果
        result_namespace = run_kubectl_command(kube_config, command_namespace)
        logging.info(result_namespace)
        assert "deleted" in result_namespace.lower(), f"Failed to delete Namespace '{namespace}'"

# 运行测试
if __name__ == "__main__":
    pytest.main()
