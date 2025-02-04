# test_06_cleanup.py
import logging
import pytest
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command
from tests.helper.k8s_client_helper import configure_k8s_client

class TestCleanup:

    @pytest.mark.order(6)
    def test_cleanup(self, json_input):
        # 配置 Kubernetes
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )
        
        pod_namespace = json_input["namespace"]
        pod_names = ["nginx1", "nginx2", "nginx3", "gpu-pod"]
        
        for pod_name in pod_names:
            # 删除 Pod 的命令 
            command = f"kubectl delete pod {pod_name} -n {pod_namespace}"
            
            # 运行命令并记录结果
            result = run_kubectl_command(kube_config, command)
            
            logging.info(result)
            assert "deleted" in result.lower(), f"Failed to delete Pod '{pod_name}' in namespace '{pod_namespace}'"
        
        # 删除节点标签
        k8s_client = configure_k8s_client(json_input)
        node_name = "minikube"
        
        body = {
            "metadata": {
                "labels": {
                    "accelerator": None
                }
            }
        }
        response = k8s_client.patch_node(node_name, body)
        logging.info(f"Removed label 'accelerator' from Node '{node_name}', response: {response}")
