import json
import pickle
import redis


def run_json(mode, data):
    if mode == 'w':
        return json.dumps(data)
    else:
        return json.loads(data)

def run_pickle(mode, data):
    if mode == 'w':
        return pickle.dumps(data)
    else:
        return pickle.loads(data)

def serialize(ser_opt, obj):
    return serialization_options[ser_opt]('w', obj)

def deserialize(ser_opt, data):
    return serialization_options[ser_opt]('r', data)

def run_files(mode, ser_opt, input_obj, file):
    """
    A function to store/retrieve data using files.
    Input parameters: 
    - operating mode ('w'rite, 'r'ead)
    - serialization option (json, pickle)
    - object to be stored
    - storage file
    """
    if ser_opt == 'pickle':
        mode = mode + 'b'

    if mode[0] == 'w':
        with open(file, mode) as f:
            data_to_store = serialize(ser_opt, input_obj)
            f.write(data_to_store)

    elif mode[0] == 'r':
        with open(file, mode) as f:
            data_to_read = f.read()
            result = deserialize(ser_opt, data_to_read)
            return result

def redis_client(url):
    if url:
        if not url.startswith('redis://'):
            url = 'redis://' + url
        return redis.Redis.from_url(url)
    else:
        return redis.Redis(host='localhost', port=6379, db=0)

def run_redis(mode, ser_opt, obj, key, url=None):
    """
    A function to store/retrieve data using Redis DB.
    Input parameters: 
    - operating mode ('w'rite, 'r'ead)
    - serialization option (json, pickle)
    - object to be stored
    - key to the data entry
    - optional URL for a remote redis server
    """
    r = redis_client(url)

    if mode == 'w':
        data_to_store = serialize(ser_opt, obj)
        processed_data = pickle.dumps(data_to_store)
        r.set(key, processed_data)
        print ('The key for your data is:', key)

    elif mode == 'r':
        retrieved_data = pickle.loads(r.get(key))
        result = deserialize(ser_opt, retrieved_data)
        return result

def store(service, ser_opt, target, key, server_url=None):
    """
    A function to store objects using the selected method.
    Input parameters: 
    - storage service (file, redis)
    - serialization option (json, pickle)
    - target object to be stored
    - key for the data srorage service (file name, password)
    - remote server URL (optional)
    """
    try:
        storage_options[service]('w', ser_opt, target, key, server_url)
    except TypeError:
        storage_options[service]('w', ser_opt, target, key)
    except KeyError:
        print ("The storage service is not supported")

def get(service, ser_opt, key, server_url=None):
    """
    A function to retrieve objects using the selected method.
    Input parameters: 
    - storage service (file, redis)
    - serialization option (json, pickle)
    - key for the data srorage service (file name, password)
    - remote server URL (optional)
    """
    try:
        result = storage_options[service]('r', ser_opt, "", key, server_url)
        return result
    except TypeError:
        result = storage_options[service]('r', ser_opt, "", key)
        return result
    except KeyError:
        print ("The storage service is not supported")
    except FileNotFoundError:
        print ("There is no such file")

serialization_options = {'json' : run_json, 'pickle' : run_pickle}
storage_options = {'redis' : run_redis, 'file' : run_files}
