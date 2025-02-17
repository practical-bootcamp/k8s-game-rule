import logging

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    def test_cleanup(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        namespace = "ilovestudy"
        secret_name = "ilovek8s"

        # 删除 Secret 的命令
        command_secret = f"kubectl delete secret {secret_name} -n {namespace}"
        result_secret = run_kubectl_command(kube_config, command_secret)
        logging.info(result_secret)

        # 删除 Namespace 的命令
        command_namespace = f"kubectl delete namespace {namespace}"
        result_namespace = run_kubectl_command(kube_config, command_namespace)
        logging.info(result_namespace)


# 运行测试
if __name__ == "__main__":
    pytest.main()
