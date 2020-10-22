import json

data = {}
data['bd'] = []
data['bd'].append({
    'nombre_BD': 'bd1',
    'Clasificacion': 'ALTO',
})
data['bd'].append({
    'nombre_BD': 'bd2',
    'Clasificacion': 'MEDIO',
})
data['bd'].append({
    'nombre_BD': 'bd3',
    'Clasificacion': 'BAJO',
})
data['bd'].append({
    'nombre_BD': 'bd4',
    'Clasificacion': 'ALTO',
})

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
