import glob, json, keyword
from typing import Dict

# extracts python models from json files

models_type = Dict[str, Dict[str, str]]

class JsonToModels:
    def __init__(s, root_name):
        s.models: models_type = {}
        s.root_name: str = root_name

    def extract_models(s, data):

        def get_type(value, key: str):
            
            if isinstance(value, dict):
                name = key.title().replace('_','')
                attrs = {}
                for k, v in value.items():
                    k: str
                    if not k.isidentifier(): 
                        continue
                    if keyword.iskeyword(k):
                        k += '_'
                    attrs[k] = get_type(v, k)
                if name in s.models:
                    s.models[name].update(attrs)
                else:
                    s.models[name] = attrs 
                return name 
            
            elif isinstance(value, list):
                if key.endswith('s'):
                    key = key[:-1]
                item_type = None 
                for item in value:
                    item_type = get_type(item, key)
                return f'List[ {item_type} ]'

            else:
                return type(value).__name__
        
        get_type(data, s.root_name)

    def write_models(s):        
        models2: models_type = {}

        def add_model(name: str, attrs: Dict[str, str]):
            for k, v in attrs.items():
                if 'List' in v:
                    v = v.split('List[ ')[1].split(' ]')[0]
                if v in s.models and v not in models2:
                    return
            models2[name] = attrs

        while len(s.models) != len(models2):
            for name, attrs in s.models.items():
                if name in models2:
                    continue
                add_model(name, attrs)
            print('added', len(models2), '/', len(s.models), 'models')

        lines = ['from typing import List']
        for name, attrs in models2.items():
            lines.append(f'\nclass {name}:')
            for k, v in attrs.items():
                lines.append(f'    {k}: {v}')
            if len(attrs) == 0:
                lines.append(f'    pass')
        
        with open('models.py', 'w+') as f:
            f.write('\n'.join(lines))


if __name__=='__main__':
    jtm = JsonToModels(root_name='Root')
    data_dir = './json_data'
    for path in glob.glob(f'{data_dir}/*.json'):
        print(path)
        with open(path) as f:
            data = json.load(f)
        jtm.extract_models(data)   
    jtm.write_models()

"""
python -m build
python -m twine upload dist/*
"""