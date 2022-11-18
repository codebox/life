from persist import Persistence
from environment import Environment
from random import random, shuffle
from time import time


config = {
    'save_location': 'save',
    'web_location': 'public',
    'locations': {
        'width': 100,
        'height': 100
    },
    'population': {
        'species': {
            'herbivore': {
                'count': 4000,
                'hidden_layer_size': 100,
                'energy': {
                    'initial': 1,
                    'move_success': 0,
                    'move_fail': 0.002,
                    'eat_fail': 0.002,
                    'reproduce_min': 1.1,
                    'reproduce_fail': 0.002,
                    'ageing': 0.0005
                }
            },
            'carnivore': {
                'count': 1000,
                'hidden_layer_size': 500,
                'energy': {
                    'initial': 2,
                    'move_success': 0,
                    'move_fail': 0.001,
                    'eat_success': 0,
                    'eat_fail': 0.001,
                    'reproduce_min': 2.1,
                    'reproduce_fail': 0.001,
                    'ageing': 0.008
                }
            },
        },
        'minimum': 10,
        'network_mutation_rate': 0.03,
    },
    'food': {
        'regrow_interval': 1000,
        'regrow_amount': 0.0004,
        'initial_max': 1,
        'initial_min': 0.2,
        'max': 1,
    },
}


def init_locations_with_random_food(environment):
    def init_food(location):
        location['food'] = config['food']['initial_min'] + random() * (config['food']['initial_max'] - config['food']['initial_min'])

    environment.locations.for_each_location(init_food)

def place_agents_randomly(environment):
    for agent, location in zip(environment.population.agents, environment.locations.get_locations_in_random_order()):
        agent.coords = location['coords']
        location['agent'] = {'id': agent.id, 'type': agent.species_name}

def agents_with_zero_energy_are_removed(environment, agent, _):
    if agent.energy <= 0:
        environment.remove_agent(agent)

def food_regrows(environment, _1, _2):
    def regrow_food(loc):
        loc['food'] = min(config['food']['max'], loc['food'] + config['food']['regrow_amount'])

    if environment.update_count % config['food']['regrow_interval'] == 0:
        environment.locations.for_each_location(regrow_food)

def run(environment, persist):
    persist.metadata_to_json(environment)

    population = environment.population
    persist.environment_to_json(environment)
    last_save = time()

    while population.is_viable():
        agent = population.get_random_agent()
        view = agent.view(environment)
        action = agent.act(view)
        environment.update(agent, action)
        if time() - last_save > 1:
            last_save = time()
            persist.environment_to_json(environment)

    persist.environment_to_json(environment)
    # print('Stopped, population size = {}'.format(len(population.agents)))


if __name__ == '__main__':
    persist = Persistence(config['save_location'], config['web_location'])
    environment = persist.restore_environment()
    if environment:
        run(environment, persist)
    else:
        while True:
            environment = Environment(config, [
                init_locations_with_random_food,
                place_agents_randomly
            ], [
                agents_with_zero_energy_are_removed,
                food_regrows
            ])
            run(environment, persist)



