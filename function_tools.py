import os.path
import json

base_path = os.path.abspath(os.getcwd())
data_path = os.path.join(base_path, 'data')
if not os.path.exists(data_path):
    os.mkdir(data_path)


def read_json(file_name):
    file = os.path.join(data_path, file_name + '.json')
    if not os.path.exists(file):
        f = open(file, 'w')
        f.write("{}")
        f.close()

    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def write_json(file_name, data):
    file = os.path.join(data_path, file_name + '.json')
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def select(file, name):
    data = read_json(file)
    if name == 'all':
        return data

    result = data.get(name)
    return result


def insert(file, obj):
    data = read_json(file)
    if not isinstance(obj, dict):
        raise TypeError('argus must be dict')
    if len(obj) > 1:
        raise ValueError('obj length must be 1')
    key = list(obj.keys())[0]
    if key in data.keys():
        raise ValueError(key + ' has exist, not allow insert')
    data.update(obj)
    write_json(file, data)


def update(file, obj):
    data = read_json(file)
    if not isinstance(obj, dict):
        raise TypeError('argus must be dict')
    if len(obj) > 1:
        raise ValueError('obj length must is 1')
    key = list(obj.keys())[0]
    if key not in data.keys():
        raise ValueError(key + ' not exist, not allow update')
    data.update(obj)
    write_json(file, data)


def delete(file, name):
    data = read_json(file)
    data.pop(name)
    write_json(file, data)
