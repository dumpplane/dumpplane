import sys
import yaml
from kubernetes import client, config

def apply_ingress(credentials, ingress_file):

    config.load_kube_config(config_file=credentials)
    current_context = config.list_kube_config_contexts()[1]
    cluster_name = current_context['context']['cluster']
    api_instance = client.NetworkingV1Api()
    namespace = "default"
    try:
        with open(ingress_file, "r") as yaml_file:
            ingress_manifest = yaml.safe_load(yaml_file)
        yaml_file.close
        if "namespace" in ingress_manifest['metadata']:
            namespace = ingress_manifest['metadata']['namespace']
        name = ingress_manifest['metadata']['name']
        apiversion = ingress_manifest['apiVersion'][:ingress_manifest['apiVersion'].rfind("/")]

        ingressExist = False
        for item in api_instance.list_namespaced_ingress(namespace=namespace).items:
            if item.metadata.name == name:
                ingressExist = True
                break
        if ingressExist:
            api_instance.patch_namespaced_ingress( name = name, namespace = namespace, body = ingress_manifest)
            print(cluster_name + "/" + namespace + "/" + apiversion + "/" + name + " updated")
        else:
            api_instance.create_namespaced_ingress( namespace = namespace, body = ingress_manifest)
            print(cluster_name + "/" + namespace + "/" + apiversion + "/" + name + " created")

    except Exception as e:
        print(f"Error: {str(e)}")
  


def apply_gw_template(credentials, conf_file):
    print(credentials, conf_file)

def apply_conf(credentials, conf_file):
    print(credentials, conf_file)

def apply(credentials, type, conf_file):

    if type == "ingress":
        apply_ingress(credentials, conf_file)
    elif type == "gw":
        apply_gw_template(credentials, conf_file)
    else:
        apply_conf(credentials, conf_file)

