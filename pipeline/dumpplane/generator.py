#!/usr/bin/python3

import sys
import ast
import re
import socket
import ipaddress

from .nginxlib import conf
from pypinyin import pinyin, Style


def generate(dict):
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
        upstreamserver = conf.get('nginx', 'conf.upstream.server').replace("${replacement.endpoint}", member).replace("${replacement.blank}", CONSTANT_STR_TAB)
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
    locations = ""
    for url in url_list:
        proxy_pass_raw = "vs_" + resource_namespace + "_" + resource_type + "_" + service + "_app" + url.replace("/", "-")
        proxy_pass = proxy_pass_raw.lower()
        upstream = conf.get('nginx', 'conf.upstream').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.upstream.servers}", upstreamservers).replace("${replacement.proxy_pass}", proxy_pass)
        if len(upstreams) > 0:
            upstreams += "\n"
        upstreams += upstream;

        location = conf.get('nginx', 'conf.location.no.ws').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.uri}", url).replace("${replacement.service}", service).replace("${replacement.proxy_pass}", proxy_pass)
        if len(locations) > 0:
            locations += "\n"
        locations += location

    status_zone_raw = dict['host'] + "_" + resource_namespace + "_" + resource_type
    status_zone = status_zone_raw.lower()
    server = conf.get('nginx', 'conf.server').replace("${replacement.blank}", CONSTANT_STR_TAB).replace("${replacement.server.port}", dict['port']).replace("${replacement.server.host}", dict['host']).replace("${replacement.server.zone}", status_zone).replace("${replacement.resource_type}", resource_type).replace("${replacement.resource_namespace}", resource_namespace).replace("${replacement.resource_name}", resource_name).replace("${replacement.locations}", locations)

    configuration = upstreams
    if len(configuration) > 0:
        configuration += "\n"
    configuration += server

    print(configuration)


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

def generate_api():
    api = conf.get('nginx', 'conf.server.api').replace("${replacement.blank}", CONSTANT_STR_TAB)
    print(api)

def generate_requests(fileadd):
    config_list = load_app_request_form(fileadd)
    for config in config_list:
        generate(config)

def generator(target):
    
    if target == "api":
        generate_api()
    else:
        generate_requests(target)



