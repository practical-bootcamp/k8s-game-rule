# test_03_answer.py
import logging
import os
import pytest
from tests.helper.kubectrl_helper import build_kube_config, run_kubectl_command


@pytest.mark.order(3)
def test_answer(json_input):
    kube_config = build_kube_config(
        json_input["cert_file"], json_input["key_file"], json_input["host"]
    )

    current_folder = os.path.dirname(__file__)
    template_path = os.path.join(current_folder, "answer.template.yaml")
    yaml_path = os.path.join(current_folder, "answer.gen.yaml")

    # 读取并替换模板文件中的占位符
    with open(template_path, "r", encoding="utf-8") as file:
        yaml_content = file.read()
        yaml_content = yaml_content.replace("{namespace}", json_input["namespace"])
        with open(yaml_path, "w", encoding="utf-8") as file:
            file.write(yaml_content)

    # 应用生成的 yaml 文件以创建 Pods
    command = f"kubectl apply -f {yaml_path}"
    result = run_kubectl_command(kube_config, command)
    logging.info(result)

    # 验证 Pods 是否创建成功
    pod_names = ["nginx1", "nginx2", "nginx3"]
    for pod_name in pod_names:
        command = f"kubectl get pod {pod_name} -n {json_input['namespace']} -o json"
        result = run_kubectl_command(kube_config, command)
        logging.info(result)
        assert pod_name in result, f"Pod '{pod_name}' does not exist in namespace '{json_input['namespace']}'"

