from environment import Environment
from population import Population
from persist import dump_environment, dump_metadata, load_environment, save_environment
from logger import log
from time import time, sleep
import signal, sys

config = {
    'population_size': 2000,
    'hidden_layer_size': 10,
    'network_mutation_rate': 0.03,
    'actions': ['move_north', 'move_south', 'move_west', 'move_east', 'eat', 'reproduce'],
    'ui_update_seconds': 1,
    'environment_tick_seconds': 1,
    'environment_regeneration_rate': 0.01,
    'view_attributes': ['energy', 'nr', 'ng', 'nb', 'sr', 'sg', 'sb', 'wr', 'wg', 'wb', 'er', 'eg', 'eb'],
    'grid_width': 100,
    'grid_height': 100,
    'cell_min_init_energy': 0.5,
    'agent_energy': {
        'initial': 1,
        'reproduce': 1.1,
        'reproduce_fail': 0.01,
        'move_success': 0.00,
        'move_fail': 0.01,
        'loss_per_second': 0.01,
        'eat_fail': 0.01
    }
}

def signal_handler(sig, frame):
    save_environment(environment)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

persisted_environment = load_environment()
if persisted_environment:
    environment = persisted_environment
    population = environment.population
else:
    population = Population(config)
    environment = Environment(config, population)

dump_metadata(environment)
i = 0
last_ui_update = time()
last_environment_tick = time()

log.info('Starting population {}'.format(population.size()))
while population.size():
    agent = population.get_random_agent()
    view = environment.get_view(agent)
    action = agent.act(view)
    environment.update(agent, action)

    if time() - last_ui_update > config['ui_update_seconds']:
        dump_environment(environment)
        # log.info('Action {}'.format(i))
        last_ui_update = time()

    elapsed_time_seconds = time() - last_environment_tick
    if elapsed_time_seconds > config['environment_tick_seconds']:
        environment.tick(elapsed_time_seconds)
        last_environment_tick = time()

    # sleep(0.001)
    i += 1

dump_environment(environment)
log.info('Finished, population is 0')
