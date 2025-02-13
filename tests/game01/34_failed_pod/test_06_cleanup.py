import logging

from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCleanup:

    def test_cleanup(self, json_input):
        # 配置 Kubernetes
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        namespace = "one"

        # 删除 Pod 的命令
        pod_name = "fail-pod"
        command_pod = f"kubectl delete pod {pod_name} -n {namespace}"

        # 运行命令并记录结果，如果Pod不存在，命令会失败，但这是预期行为
        result_pod = run_kubectl_command(kube_config, command_pod)
        logging.info(result_pod)


# 运行测试
if __name__ == "__main__":
    pytest.main()
