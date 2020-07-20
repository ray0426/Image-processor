import json

data = {'a': 100, 'b': 1000, 'c': 10000}
with open('abc.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

with open('abc.json', 'r', encoding='utf-8') as f:
    output = json.load(f)
print(output)
