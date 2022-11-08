from environment import Environment
from population import Population
from persist import dump_environment

config = {
    'population_size': 10,
    'hidden_layer_size': 10,
    'network_mutation_rate': 0.01,
    'actions': ['move_north', 'move_south', 'move_west', 'move_east'],
    'ui_update_rate': 10,
    'view_attributes': ['energy', 'nr', 'ng', 'nb', 'sr', 'sg', 'sb', 'wr', 'wg', 'wb', 'er', 'eg', 'eb'],
    'grid_width': 40,
    'grid_height': 40,
    'agent_initial_energy': 1
}

population = Population(config)
environment = Environment(config, population)
i = 0

while population.size():
    agent = population.get_random_agent()
    view = environment.get_view(agent)
    action = agent.act(view)
    environment.update(agent, action)

    if i % config['ui_update_rate']:
        dump_environment(environment)

    i += 1

dump_environment(environment)
print('Population 0')
