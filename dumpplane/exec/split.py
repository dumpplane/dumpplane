
import os
import re

lists = []

def extractHost(filename):
    result = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').search(filename)
    return result.group()

def split_file(file, out):
    filename = os.path.basename(file)
    output = os.path.join( out, filename )
    if not os.path.exists(output):
        os.makedirs(output)
    config = {'dumpFileName': file, 'ngxHost': extractHost(filename), 'diskPath': output}

    with open(file, 'r') as fo:
        data_all = fo.read()

    subfiles = re.findall(r'# configuration file\s+\S+:',data_all, re.I)
    for item,num  in zip(subfiles,range(len(subfiles))):
        print(item, type(item), num)

    config['basePath'] = '/etc/nginx'

    #print(subfiles)

def split(conf, out):
    for filename in os.listdir(conf):
        f = os.path.join(conf, filename)
        if os.path.isfile(f):
            split_file(f, out)
        else:
            split(f, out)
