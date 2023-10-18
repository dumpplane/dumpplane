#!/usr/bin/python3

import sys
import ast
import re
import socket
import ipaddress

from .nginxlib import utils
from pypinyin import pinyin, Style


def generate(dict, health_check_path):
    first_later_list = pinyin(dict['name'], style=Style.NORMAL)
    resource_name = listToString(first_later_list)
    resource_namespace = dict['zone']
    resource_type = dict['type']
    service = dict['service']
    if len(service) == 0 :
        service = resource_type
    serlist = dict['serverlist']
    serport = dict['serverport']
    upstreamservers = ""
    for ip in serlist:
        member = " " + ip + ":" + str(serport)
        upstreamserver = utils.get('nginx', 'conf.upstream.server').replace("${replacement.endpoint}", member).replace("${replacement.blank}", CONSTANT_STR_TAB)
        if len(upstreamservers) > 0:
            upstreamservers += "\n"
        upstreamservers += upstreamserver 

    url_list = []
    urls = dict['urls']
    if("," in urls) :
        url_list = urls.split(",")
    else:
        url_list.append(urls)

    
    upstreams = ""
    matchs = ""
    locations = ""
    for url in url_list:
        proxy_pass_raw = "vs_" + resource_namespace + "_" + resource_type + "_" + service + "_app" + url.replace("/", "-")
        proxy_pass = proxy_pass_raw.lower()
        upstream = utils.get('nginx', 'conf.upstream').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.upstream.servers}", upstreamservers).replace("${replacement.proxy_pass}", proxy_pass)
        if len(upstreams) > 0:
            upstreams += "\n"
        if dict['persist'] == "Yes":
            cookie = utils.get('nginx', 'conf.upstream.cookie').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.upstream.cookie}", resource_name + "_" + service + "_cookie")
            upstream = upstream.replace("${replacement.upstream.persist}", cookie)
        else:
            upstream = upstream.replace("${replacement.upstream.persist}", CONSTANT_STR_ENTER)
        upstreams += upstream;

        location = utils.get('nginx', 'conf.location').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.uri}", url).replace("${replacement.service}", service).replace("${replacement.proxy_pass}", proxy_pass)
        if len(locations) > 0:
            locations += "\n"
        locations += location

        if health_check_path is not None:
            hc_location = location = utils.get('nginx', 'conf.location.hc').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.proxy_pass}", proxy_pass)
            locations += "\n"
            locations += hc_location
            match = utils.get('nginx', 'conf.match').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.proxy_pass}", proxy_pass)
            if len(matchs) > 0:
                matchs += "\n"
            matchs += match

    status_zone_raw = dict['host'] + "_" + resource_namespace + "_" + resource_type
    status_zone = status_zone_raw.lower()
    server = utils.get('nginx', 'conf.server').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.server.port}", dict['port']).replace("${replacement.server.host}", dict['host']).replace("${replacement.server.zone}", status_zone).replace("${replacement.resource_type}", resource_type).replace("${replacement.resource_namespace}", resource_namespace).replace("${replacement.resource_name}", resource_name).replace("${replacement.locations}", locations)

    if dict['sec_contorl'] == "Yes":
        server_security = utils.get('nginx', 'conf.server.security').replace("${replacement.blank}", CONSTANT_STR_TAB)
        server = server.replace("${replacement.server.security}", server_security) 
    else:
        server = server.replace("${replacement.server.security}", CONSTANT_STR_ENTER)

    configuration = upstreams
    if len(configuration) > 0:
        configuration += "\n"

    if len(matchs) > 0:
        matchs += "\n"
    configuration += matchs
    configuration += server

    utils.write_to_file(resource_name + ".conf", configuration)


def listToString(s):
    result = ""
    for l in s:
        item = l[0]
        item = item[0].upper() + item[1:]
        result += item
    return result

def find_last_index(str, substr):
    last_index = -1
    while True:
        index = str.find(substr, last_index + 1)
        if index == -1:
            return last_index
        last_index = index

def format_app_table_ip_addr(ip):
    list = []
    if("-" in ip) :
        ips = ip.split("-")
        list.insert(0, ips[0])
        lastdot = find_last_index(list[0], ".")
        prefix = list[0][:(lastdot + 1)]
        start = list[0][(lastdot + 1):]
        last = ips[1]
        for i in range(int(last) - int(start)):
            num = int(start) + i + 1
            list.insert(i + 1, prefix + str(num))
    else:
        list.insert(0, ip)
    return list

def format_app_table_ip_addr_to_list(ip):
    list = []
    if("," in ip) :
        ips = ip.split(",")
        for i in ips:
            list.extend(format_app_table_ip_addr(i))
    else:
        list = format_app_table_ip_addr(ip)
    return list

def load_app_request_form(fileadd):
    config_list = []
    with open(fileadd, "r") as file:
        for line in file:
            line = line.replace('[', '{').replace(']', '}')
            dict = ast.literal_eval(line)
            config = {'name': dict[k_name], 'ip': dict[k_ip], 'port': dict[k_port], 'host': dict[k_host], 'protocol': dict[k_protocol]}
            config['serverlist'] = format_app_table_ip_addr_to_list(dict[k_serveraddr])
            config['serverport'] = dict[k_serverport]
            config['service'] = dict[k_service]
            config['zone'] = dict[k_zone]
            config['type'] = dict[k_type]
            config['urls'] = dict[k_url] 
            config['lb_method'] = dict[k_lb_method]
            config['sec_contorl'] = dict[k_sec_contorl]
            config['persist'] = dict[k_persist]
            config_list.append(config)
    file.close
    return config_list

CONSTANT_STR_TAB = "    "
CONSTANT_STR_TAB5 = "                      "
CONSTANT_STR_ENTER = ""

k_name = '系统名称'
k_ip = '地址'
k_port = '端口'
k_host = '域名'
k_serverport = '服务器端口'
k_serveraddr = '真实服务器地址'
k_protocol = '协议类型'
k_service = '服务名称'
k_zone = '服务区域'
k_type = '服务类型'
k_persist = '会话保持'
k_url = 'URL路径'
k_lb_method = '负载算法'
k_sec_contorl = '安全控制'

def generate_api(port, allow):

    if port is None:
        port = "8001"

    if allow is None:
        allow = "0.0.0.0/0"

    api = utils.get('nginx', 'conf.server.api').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.server.port}", port).replace("${replacement.server.allow}", allow)
    utils.write_to_file("api.conf", api)

def generate_main(user, worker_processes, worker_connections, keepalive_timeout, keepalive_requests, hash_max_size, hash_bucket_size, enable_websocket):
    
    if user is None:
        user = "nginx"

    if worker_processes is None:
        worker_processes = "auto"

    if worker_connections is None:
        worker_connections = "1024"

    if keepalive_timeout is None:
        keepalive_timeout = "65"

    if keepalive_requests is None:
        keepalive_requests = "100"

    if hash_max_size is None:
        hash_max_size = "1024"

    if hash_bucket_size is None:
        hash_bucket_size = "256"

    events = utils.get('nginx', 'conf.main.events').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.main.events.connections}", worker_connections)

    http = utils.get('nginx', 'conf.main.http').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.blank.5}", CONSTANT_STR_TAB5).replace("${replacement.main.http.timeout}", keepalive_timeout).replace("${replacement.main.http.requests}", keepalive_requests).replace("${replacement.main.http.hash.maxsize}", hash_max_size).replace("${replacement.main.http.hash.bucketsize}", hash_bucket_size)

    if enable_websocket == "Yes":
        ws_map = utils.get('nginx', 'conf.main.http.ws').replace("${replacement.blank}", CONSTANT_STR_TAB)
        http = http.replace("${replacement.websocket}", ws_map)
    else:
        http = http.replace("${replacement.websocket}", CONSTANT_STR_ENTER)

    main = utils.get('nginx', 'conf.main').replace("${replacement.main.events}", events).replace("${replacement.enter}", CONSTANT_STR_ENTER).replace("${replacement.main.http}", http).replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.main.user}", user).replace("${replacement.main.processes}", worker_processes)

    utils.write_to_file("nginx.conf", main)


def generate_requests(fileadd, health_check_path):
    config_list = load_app_request_form(fileadd)
    for config in config_list:
        generate(config, health_check_path)

def generator(target, port, allow, user, worker_processes, worker_connections, keepalive_timeout, keepalive_requests, hash_max_size, hash_bucket_size, health_check_path, enable_websocket):
    
    if target == "api":
        generate_api(port, allow)
    elif target == "main":
        generate_main(user, worker_processes, worker_connections, keepalive_timeout, keepalive_requests, hash_max_size, hash_bucket_size, enable_websocket)
    else:
        generate_requests(target, health_check_path)



