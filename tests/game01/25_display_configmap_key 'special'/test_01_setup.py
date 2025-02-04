import pytest
import logging
from tests.helper.k8s_client_helper import configure_k8s_client
from tests.helper.kubectrl_helper import run_kubectl_command

@pytest.mark.order(1)
def test_setup(json_input):
    k8s_client = configure_k8s_client(json_input)

    # 创建文件并加载内容
    command_create_file = "echo -e 'var3=val3\nvar4=val4' > config4.txt"
    result_create_file = run_kubectl_command(json_input, command_create_file)
    logging.info(f"Created file 'config4.txt' with content. Result: {result_create_file}")

# 运行测试
if __name__ == "__main__":
    pytest.main()
