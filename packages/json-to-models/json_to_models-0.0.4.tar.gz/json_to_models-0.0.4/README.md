# json to models
 
extracts python models from json files

## usage

- input: [./json_data](https://github.com/tesla-cat/json-to-models/tree/main/json_data)

```cmd
pip install json-to-models
```

```python
from json_to_models import JsonToModels
import glob, json

jtm = JsonToModels(root_name='Root')

for path in glob.glob(f'./json_data/*.json'):
    print(path)
    with open(path) as f:
        data = json.load(f)
    jtm.extract_models(data)   

jtm.write_models()
```

- output: [models.py](https://github.com/tesla-cat/json-to-models/blob/main/models.py)
