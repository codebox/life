from environment import Environment
from population import Population
from persist import dump_environment
from logger import log
from time import time, sleep

config = {
    'population_size': 100,
    'hidden_layer_size': 10,
    'network_mutation_rate': 0.01,
    'actions': ['move_north', 'move_south', 'move_west', 'move_east', 'reproduce'],
    'ui_update_seconds': 1,
    'view_attributes': ['energy', 'nr', 'ng', 'nb', 'sr', 'sg', 'sb', 'wr', 'wg', 'wb', 'er', 'eg', 'eb'],
    'grid_width': 40,
    'grid_height': 40,
    'agent_energy': {
        'initial': 1,
        'reproduce': 2,
        'reproduce_fail': 0.1,
        'move_success': 0.1,
        'move_fail': 0.1
    }
}

population = Population(config)
environment = Environment(config, population)
i = 0
t = time()

log.info('Starting population {}'.format(population.size()))
while population.size():
    agent = population.get_random_agent()
    view = environment.get_view(agent)
    action = agent.act(view)
    environment.update(agent, action)

    if time() - t > config['ui_update_seconds']:
        dump_environment(environment)
        log.info('Action {}'.format(i))
        t = time()

    sleep(0.01)
    i += 1

dump_environment(environment)
log.info('Finished, population is 0')
