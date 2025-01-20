import pytest
import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command

@pytest.mark.order(5)
class TestCheck:
    def test_001_pod_attributes_with_library(self, json_input):
        logging.debug(json_input)
        k8s_client = configure_k8s_client(json_input)
        pod_name = "nginx"
        pod_namespace = "default"
        pod = k8s_client.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
        
        assert pod.spec.containers[0].image == "nginx:1.24.0", "Pod image version is not nginx:1.24.0"
        assert pod.spec.containers[0].ports[0].container_port == 80, "Pod containerPort is not 80"
        assert pod.metadata.namespace == "default", "Pod namespace is not default"
        assert pod.metadata.name == "nginx", "Pod name is not nginx"

    def test_002_pod_attributes_with_kubectl(self, json_input):
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        # 获取 Pod 的命名空间
        command_namespace = "kubectl get pod nginx -n default -o=jsonpath='{.metadata.namespace}'"
        namespace_result = subprocess.run(command_namespace, shell=True, capture_output=True, text=True)
        namespace = namespace_result.stdout.strip()
        logging.info(f"Namespace: {namespace}")
        
        # 获取 Pod 的名称
        command_name = "kubectl get pod nginx -n default -o=jsonpath='{.metadata.name}'"
        name_result = subprocess.run(command_name, shell=True, capture_output=True, text=True)
        name = name_result.stdout.strip()
        logging.info(f"Pod Name: {name}")
        
        # 获取 Pod 的镜像
        command_image = "kubectl get pod nginx -n default -o=jsonpath='{.spec.containers[0].image}'"
        image_result = subprocess.run(command_image, shell=True, capture_output=True, text=True)
        image = image_result.stdout.strip()
        logging.info(f"Pod Image: {image}")
        
        # 获取 Pod 的端口
        command_port = "kubectl get pod nginx -n default -o=jsonpath='{.spec.containers[0].ports[0].containerPort}'"
        port_result = subprocess.run(command_port, shell=True, capture_output=True, text=True)
        port = port_result.stdout.strip()
        logging.info(f"Pod Port: {port}")

        # 验证命名空间、名称、镜像和端口
        assert namespace == "default", "Pod namespace is not 'default'"
        assert name == "nginx", "Pod name is not 'nginx'"
        assert image == "nginx:1.24.0", f"Pod image is not 'nginx:1.24.0', it is '{image}'"
        assert port == "80", f"Pod port is not '80', it is '{port}'"

