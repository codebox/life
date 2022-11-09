import json

def dump_environment(environment):
    with open('public/state.json', 'w') as f:
        cells = [cell for row in environment.grid.cells for cell in row]
        json.dump({'locations': cells, 'population': environment.population.size()}, f)

def dump_metadata(environment):
    with open('public/metadata.json', 'w') as f:
        json.dump({'h': environment.grid.height, 'w': environment.grid.width}, f)
