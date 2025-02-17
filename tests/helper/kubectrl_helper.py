import logging
import os
import subprocess
import tempfile

from jinja2 import Environment


def build_kube_config(client_certificate, client_key, endpoint):
    cert_data = client_certificate
    key_data = client_key

    template = """
apiVersion: v1
kind: Config
clusters:
  - name: k8s-cluster
    cluster:
      server: {{endpoint}}
contexts:
  - name: k8s-context
    context:
      cluster: k8s-cluster
      user: k8s-user
current-context: k8s-context
users:
  - name: k8s-user
    user:
      client-certificate: {{cert_data}}
      client-key: {{key_data}}
    """
    env = Environment()
    jinja_template = env.from_string(template)
    return jinja_template.render(
        endpoint=endpoint, cert_data=cert_data, key_data=key_data
    ).encode("utf-8")


def run_kubectl_command(kube_config, command):
    with tempfile.NamedTemporaryFile(delete=False) as temp_config:
        temp_config.write(kube_config)
        temp_config.flush()
        os.environ["KUBECONFIG"] = temp_config.name
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=True
            )
        except subprocess.CalledProcessError as e:
            logging.info(e.stderr)
            return e.stderr
    return result.stdout


def delete_namespace(json_input):
    kube_config = build_kube_config(
        json_input["cert_file"], json_input["key_file"], json_input["host"]
    )

    pod_namespace = json_input["namespace"]
    command = f"kubectl delete namespace  {pod_namespace}"
    result = run_kubectl_command(kube_config, command)
    logging.info(result)
