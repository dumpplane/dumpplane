
import os
import re

lists = []

def extractHost(filename):
    result = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').search(filename)
    return result.group()

def extractFilepathName(item):
    filename = None
    dirname = None
    filepath = item.split()
    filepath = filepath[len(filepath) -1]
    if filepath.endswith(":"):
        filepath = filepath[0:len(filepath)-1]
        dirname = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
    return (filepath, dirname, filename)

def split_file(file, out):
    filename = os.path.basename(file)
    output = os.path.join( out, filename )
    if not os.path.exists(output):
        os.makedirs(output)
    config = {'dumpFileName': filename, 'ngxHost': extractHost(filename), 'diskPath': output}

    with open(file, 'r') as fo:
        data_all = fo.read()

    subfiles = re.findall(r'# configuration file\s+\S+:',data_all, re.I)
    basePath = None
    conf_list = []
    dumpplane = []

    for item in subfiles:
        conf_list.append(item)

    for item, num in zip(subfiles,range(len(subfiles))):
        if num < len(conf_list) - 1:
            conf_data_start = re.search(item, data_all, re.I).start()
            conf_data_end = re.search(conf_list[num + 1], data_all[conf_data_start:]).start()
            conf_data_detail = data_all[conf_data_start:][:conf_data_end]  
        else:
            conf_data_start = re.search(item, data_all, re.I).start()
            conf_data_detail = data_all[conf_data_start:]

        conf_path_details = extractFilepathName(item)

        if basePath is None:
            basePath = conf_path_details[1]
        elif conf_path_details[1] in basePath:
            basePath = conf_path_details[1]

        dumpplane.append({'filepath': conf_path_details[0], 'dirname': conf_path_details[1], 'filename': conf_path_details[2], 'content': conf_data_detail})

    config['basePath'] = basePath
    config['dumpplane'] = dumpplane

    lists.append(config)


def dump_to_disk():
    for c in lists:
        basePath = c['basePath']
        dumpplane = c['dumpplane']
        diskPath = c['diskPath']
        for d in dumpplane:
            prefix = d['dirname'][len(basePath):]
            out_dir = diskPath + prefix
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            file_to_write = os.path.join( out_dir, d['filename'] )
            f = open(file_to_write, "w")
            content = d['content']

            if basePath in content:
                content = content.replace(basePath + "/", "") 

            f.write(content)



def spliti_files(conf, out):
    for filename in os.listdir(conf):
        f = os.path.join(conf, filename)
        if os.path.isfile(f):
            split_file(f, out)
        else:
            spliti_files(f, out)


def split(conf, out, dump):
    spliti_files(conf, out)
    if dump:
        dump_to_disk()
    return lists
