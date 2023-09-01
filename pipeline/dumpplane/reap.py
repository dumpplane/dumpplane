import sys
import yaml
import json
from kubernetes import client, config

def get_ingress_from_namespace(api_instance, namespace):
    try:
        api_response = api_instance.list_namespaced_ingress(namespace=namespace)
        return api_response.items
    except Exception as e:
        print(f"Error: {str(e)}")

def write_to_file(file_path, data):
    try:
        json_string = json.dumps(data, indent=4)
        with open(file_path, "w") as file:
            file.write(json_string)
        print(f"reap to {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

def reap_ingress(credentials, namespaces, outputToConsole):
    
    namespaces_raws = namespaces.split(",")
    namespaces_list = [i.strip() for i in namespaces_raws if len(i.strip()) > 0]

    config.load_kube_config(config_file=credentials)
    current_context = config.list_kube_config_contexts()[1]
    cluster_name = current_context['context']['cluster']
    api_instance = client.NetworkingV1Api()

    for ns in namespaces_list:
        items = get_ingress_from_namespace(api_instance, ns)
        for item in items:
            if outputToConsole:
                ingress_yaml = yaml.dump(item.to_dict(), default_flow_style=False)
                print(ingress_yaml)
            else:
                target_dict = item.to_dict()
                target_dict['metadata']['creation_timestamp'] = target_dict['metadata']['creation_timestamp'].isoformat()
                if target_dict['metadata']['managed_fields']:
                    for f in target_dict['metadata']['managed_fields']:
                        f['time'] = f['time'].isoformat()
                file_path = cluster_name + "_" + ns + "_" + item.metadata.name + ".json"
                write_to_file(file_path, target_dict)


def reap_gw_template(credentials, namespaces, outputToConsole):
    print(credentials, namespaces, outputToConsole)

def reap_conf(credentials, namespaces, outputToConsole):
    print(credentials, namespaces, outputToConsole)

def reap(credentials, type, namespaces, console):

    outputToConsole = False
    if console is not None and console > 0:
        outputToConsole = True

    if type == "ingress":
        reap_ingress(credentials, namespaces, outputToConsole)
    elif type == "gw":
        reap_gw_template(credentials, namespaces, outputToConsole)
    else:
        reap_conf(credentials, namespaces, outputToConsole)

