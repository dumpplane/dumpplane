
import os
import json

from pymongo.mongo_client import MongoClient
from .split import split

def dump_to_mongodb(config, conn, db_name, table_name):
    db = conn[db_name]
    collection = db[table_name]
    filter = {'dumpFileName': config['dumpFileName'], 'ngxHost': config['ngxHost']}
    matched_count = collection.replace_one(filter, config, True).matched_count
    print("dump " + config['dumpFileName'] + " to mongodb, modified: " + str(matched_count))

def dump_to_elastic(config, conn):
    #print(config, conn)
    print("ELASTIC")

def dump_to_file(config, out):
    dumpFileName = config['dumpFileName'] + ".json"
    out_file = os.path.join( out, dumpFileName )
    json_data = json.dumps(config)
    file = open(out_file, "w")
    file.write(json_data)
    print("dump " + dumpFileName + " to " + out)

def init_conn(out):
    conn_mongo = None
    conn_elastic = None
    conn_file = None
    if out.startswith("mongodb://") or out.startswith("mongodb+srv://") :
        conn_mongo = MongoClient(out)
        print("create connection " + out)
    elif out.startswith("http://") or out.startswith("https://") :
        conn_elastic = None
    else:
        conn_file = out

    return (conn_mongo, conn_elastic, conn_file)

def dump(conf, input, out, db_name, table_name):
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
            dump_to_elastic(config, conn_tuple[1])
        elif conn_tuple[0] is None and conn_tuple[1] is None and conn_tuple[2] is not None:
            dump_to_file(config, conn_tuple[2])
        else:
            dump_to_file(config, out)

    if conn_tuple[0] is not None:
        conn_tuple[0].close()
