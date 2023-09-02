import sys
import yaml
from kubernetes import client, config

def delete_ingress(credentials, ingress_file):

    config.load_kube_config(config_file=credentials)
    current_context = config.list_kube_config_contexts()[1]
    cluster_name = current_context['context']['cluster']
    api_instance = client.NetworkingV1Api()

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
            api_instance.delete_namespaced_ingress( name = name, namespace = namespace)
            print(cluster_name + "/" + namespace + "/" + apiversion + "/" + name + " deleted")
        else:
            print(cluster_name + "/" + namespace + "/" + apiversion + "/" + name + " not existed")

    except Exception as e:
        print(f"Error: {str(e)}")


def delete_gw_template(credentials, conf_file):
    print(credentials, conf_file)

def delete_conf(credentials, conf_file):
    print(credentials, conf_file)

def delete(credentials, type, conf_file):

    if type == "ingress":
        delete_ingress(credentials, conf_file)
    elif type == "gw":
        delete_gw_template(credentials, conf_file)
    else:
        delete_conf(credentials, conf_file)

