import json, math, pickle, os.path
from pathlib import Path


def get_agent_colour(agent):
    energy_factor = min(1, agent.state['energy'])
    inputs = [1] * agent.network.input_size
    result = agent.network.calc([inputs])[0]
    hue = 0
    for i, r in enumerate(result):
        hue += r * i * 360 / len(result)

    return 'hsla({}, 100%, 50%, {})'.format(hue, energy_factor)

def dump_environment(environment):
    def get_details(cell):
        details = dict(cell)
        if 'agent' in cell:
            agent = environment.population.get_agent_by_id(cell['agent'])
            details['agent'] = {'colour': get_agent_colour(agent)}
        return details

    with open('public/state.json', 'w') as f:
        cells = [get_details(cell) for row in environment.grid.cells for cell in row]
        json.dump({'locations': cells, 'population': environment.population.size()}, f)

def dump_metadata(environment):
    with open('public/metadata.json', 'w') as f:
        json.dump({'h': environment.grid.height, 'w': environment.grid.width}, f)

modeL_save_dir = 'save'
environment_save_file = '{}/environment.p'.format(modeL_save_dir)
def save_environment(environment):
    [f.unlink() for f in Path(modeL_save_dir).glob("*.p")]
    pickle.dump(environment, open(environment_save_file, "wb"))

def load_environment():
    if os.path.exists(environment_save_file):
        return pickle.load(open(environment_save_file, "rb"))
