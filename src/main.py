from environment import Environment
from population import Population
from persist import dump_environment, dump_metadata, load_environment, save_environment
from logger import log
from time import time, sleep
import signal, sys

config = {
    'population_size': 4000,
    'hidden_layer_size': 1000,
    'network_mutation_rate': 0.03,
    'actions': ['move_north', 'move_south', 'move_west', 'move_east', 'eat', 'reproduce'],
    'ui_update_seconds': 1,
    'environment_tick_updates': 5000,
    'environment_regeneration_rate': 0.0000003,
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
        'loss_per_update': 0.000001,
        'eat_fail': 0.01
    }
}

def signal_handler(sig, frame):
    save_environment(environment)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

agent_id = None
if len(sys.argv) > 1:
    agent_id = int(sys.argv[1])

persisted_environment = load_environment()
if persisted_environment:
    environment = persisted_environment
    population = environment.population
    if agent_id:
        agent_with_id = population.get_agent_by_id(agent_id)
        for agent in population.agents:
            population.remove_agent(agent)
            environment._remove_agent_from_cell(agent)

        for i in range(100):
            new_agent = population.add_new_agent()
            new_agent.network = agent_with_id.network.copy(0)

        environment._populate_grid_with_agents()

    config = environment.config
else:
    population = Population(config)
    environment = Environment(config, population)

dump_metadata(environment)

min_population=10
while True:
    last_ui_update = time()
    last_environment_update = 0

    log.info('Starting population {}'.format(population.size()))
    while population.size() > min_population:
        agent = population.get_random_agent()
        view = environment.get_view(agent)
        action = agent.act(view)
        environment.update(agent, action)

        if time() - last_ui_update > config['ui_update_seconds']:
            dump_environment(environment)
            # log.info('Action {}'.format(i))
            last_ui_update = time()

        elapsed_updates = environment.updates - last_environment_update
        if elapsed_updates > config['environment_tick_updates']:
            environment.tick(elapsed_updates)
            last_environment_update = environment.updates

        # sleep(1)

    dump_environment(environment)
    log.info('Finished, population is {}'.format(min_population))

    population = Population(config)
    environment = Environment(config, population)

