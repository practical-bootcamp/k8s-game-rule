import logging

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    def test_cleanup(self, json_input):
        # 配置 Kubernetes
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        namespace = "one"

        # 删除 ResourceQuota 的命令
        quota_name = "resource-quota"
        command_quota = f"kubectl delete resourcequota {quota_name} -n {namespace}"

        # 运行命令并记录结果
        result_quota = run_kubectl_command(kube_config, command_quota)
        logging.info(result_quota)
        assert (
            "deleted" in result_quota.lower()
        ), f"Failed to delete ResourceQuota '{quota_name}' in namespace '{namespace}'"


# 运行测试
if __name__ == "__main__":
    pytest.main()
