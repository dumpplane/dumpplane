import sys
import os
import json

from pymongo.mongo_client import MongoClient
from elasticsearch import Elasticsearch

from .split import split, get_dumpplane_data_folder_path

def dump_to_mongodb(config, conn, db_name, table_name):
    db = conn[db_name]
    collection = db[table_name]
    filter = {'dumpFileName': config['dumpFileName'], 'ngxHost': config['ngxHost']}
    matched_count = collection.replace_one(filter, config, True).matched_count
    print("dump " + config['dumpFileName'] + " to mongodb, modified: " + str(matched_count))

def dump_to_elastic(config, conn, index_name):
    index_id = config['dumpFileName'] 
    resp = conn.index(index=index_name, id=index_id, document=config)
    print("dump " + index_id + " to elasticsearch, version: " + str(resp['_version']))

def dump_to_file(config, out):
    dumpFileName = config['dumpFileName'] + ".json"
    out_file = os.path.join( out, dumpFileName )
    json_data = json.dumps(config)
    file = open(out_file, "w")
    file.write(json_data)
    print("dump " + dumpFileName + " to " + out)

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def init_conn(out):
    conn_mongo = None
    conn_elastic = None
    conn_file = None
    if out.startswith("mongodb://") or out.startswith("mongodb+srv://") :
        conn_mongo = MongoClient(out)
        print("create connection " + out)
    elif out.startswith("http://") or out.startswith("https://") :
        conn_elastic = Elasticsearch(out)
    elif out.startswith("file://"):
        conn_file = out.lstrip("file://")
        create_folders(conn_file)
    else:
        conn_file = out
        create_folders(conn_file)

    return (conn_mongo, conn_elastic, conn_file)


def dump(conf, input, out, db_name, table_name):

    if input is None:
        input = get_dumpplane_data_folder_path()

    if out is None:
        current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        out = os.path.join( current_directory, 'output' )

    if db_name is None:
        db_name = "nginx"

    if table_name is None:
        table_name = "configurations"

    config_list = split(conf, input, False)
    conn_tuple = init_conn(out)

    for config in config_list:
        diskPath = config['diskPath']
        dumpFileName = config['dumpFileName']
        basePath = config['basePath'] 
        crossplne_file = os.path.join( input, dumpFileName + ".json" )
        with open(crossplne_file, 'r') as file:
            content = file.read()
            crossplane = json.loads(content)
            for c in crossplane['config']:
                conf = c['file']
                conf = conf.replace(diskPath, basePath)
                c['file'] = conf
            config['crossplane'] = crossplane
        if conn_tuple[0] is not None and conn_tuple[1] is None and conn_tuple[2] is None:
            dump_to_mongodb(config, conn_tuple[0], db_name, table_name)
        elif conn_tuple[0] is None and conn_tuple[1] is not None and conn_tuple[2] is None:
            dump_to_elastic(config, conn_tuple[1], db_name)
        elif conn_tuple[0] is None and conn_tuple[1] is None and conn_tuple[2] is not None:
            dump_to_file(config, conn_tuple[2])
        else:
            dump_to_file(config, out)

    if conn_tuple[0] is not None:
        conn_tuple[0].close()
