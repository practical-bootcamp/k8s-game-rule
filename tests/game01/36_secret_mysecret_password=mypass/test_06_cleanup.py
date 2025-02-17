import logging

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    def test_cleanup(self, json_input):
        # 配置 Kubernetes
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        namespace = "default"  # 请确保命名空间与 Secret 配置中的一致

        # 删除 Secret 的命令
        secret_name = "mysecret"
        command_secret = f"kubectl delete secret {secret_name} -n {namespace}"

        # 运行命令并记录结果
        result_secret = run_kubectl_command(kube_config, command_secret)
        logging.info(result_secret)
        assert (
            "deleted" in result_secret.lower()
        ), f"Failed to delete Secret '{secret_name}' in namespace '{namespace}'"


# 运行测试
if __name__ == "__main__":
    pytest.main()
