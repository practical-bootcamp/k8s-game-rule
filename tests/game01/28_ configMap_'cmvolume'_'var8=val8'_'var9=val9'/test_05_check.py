import json
import logging

from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


class TestCheck:
    def test_001_check_configmap(self, json_input):
        k8s_client = configure_k8s_client(json_input)
        configmap_name = "cmvolume"
        namespace = json_input["namespace"]

        try:
            configmap = k8s_client.read_namespaced_config_map(
                name=configmap_name, namespace=namespace
            )
        except Exception as e:
            assert False, f"Failed to get ConfigMap '{configmap_name}': {str(e)}"

        # 验证ConfigMap的内容
        assert configmap.api_version == "v1", "Incorrect apiVersion."
        assert configmap.kind == "ConfigMap", "Incorrect kind."
        assert configmap.metadata.name == configmap_name, "Incorrect metadata.name."
        assert "var8" in configmap.data, "Missing key 'var8' in data."
        assert configmap.data["var8"] == "val8", "Incorrect value for 'var8'."
        assert "var9" in configmap.data, "Missing key 'var9' in data."
        assert configmap.data["var9"] == "val9", "Incorrect value for 'var9'."
        logging.info(f"ConfigMap '{configmap_name}' has the correct content.")

    def test_002_check_pod(self, json_input):
        logging.debug("Starting test_002_check_pod")
        kube_config = build_kube_config(
            json_input["cert_file"], json_input["key_file"], json_input["host"]
        )

        command = f"kubectl get pod nginx-pod -n {json_input['namespace']} -o json"
        result = run_kubectl_command(kube_config, command)
        pod = json.loads(result)

        # 验证Pod的内容
        assert pod["apiVersion"] == "v1", "Incorrect apiVersion."
        assert pod["kind"] == "Pod", "Incorrect kind."
        assert pod["metadata"]["name"] == "nginx-pod", "Incorrect metadata.name."

        # 检查Pod的卷挂载
        volumes = pod["spec"]["volumes"]
        volume_dict = {
            vol["name"]: vol["configMap"]["name"]
            for vol in volumes
            if "configMap" in vol
        }
        assert "config-volume" in volume_dict, "Missing volume 'config-volume' in Pod."
        assert (
            volume_dict["config-volume"] == "cmvolume"
        ), "Incorrect ConfigMap reference for volume 'config-volume'."

        # 检查挂载路径
        volume_mounts = pod["spec"]["containers"][0]["volumeMounts"]
        mount_paths = {mnt["name"]: mnt["mountPath"] for mnt in volume_mounts}
        assert (
            "config-volume" in mount_paths
        ), "Missing volume mount 'config-volume' in Pod."
        assert (
            mount_paths["config-volume"] == "/etc/lala"
        ), "Incorrect mountPath for volume 'config-volume'."

        logging.info(f"Pod 'nginx-pod' has the correct volume mounts.")


# 运行测试
if __name__ == "__main__":
    pytest.main()
