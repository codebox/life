import json

def dump_environment(environment):
    with open('public/state.json', 'w') as f:
        cells = [cell for row in environment.grid.cells for cell in row]
        json.dump({'locations': cells, 'population': environment.population.size()}, f)
