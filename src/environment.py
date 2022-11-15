from random import shuffle
from population import Population


class Environment:
    def __init__(self, config, init_rules, update_rules):
        self.population = Population(config['population'])
        self.locations = Grid(
            config['locations']['width'],
            config['locations']['height']
        )

        for init_rule in init_rules:
            init_rule(self)

        self.update_rules = update_rules
        self.update_count = 0

    def move_agent_to_location(self, agent, location):
        if location and 'agent' not in location:
            if agent.coords:
                self._remove_agent_from_location(agent)

            agent.coords = location['coords']
            self.locations.get(location['coords'])['agent'] = {'id': agent.id, 'type': agent.species_name};
            return True

    def update(self, agent, action):
        agent.update(self, action)
        self.update_count += 1

        for update_rule in self.update_rules:
            update_rule(self, agent, action)

    def remove_agent(self, agent):
        self.population.remove_agent(agent)
        self._remove_agent_from_location(agent)

    def _remove_agent_from_location(self, agent):
        cell = self.locations.get(agent.coords)
        del cell['agent']
        del agent.coords

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[{'coords': {'x': x, 'y': y}} for x in range(width)] for y in range(height)]

    def get(self, c1, c2=None):
        if c2 is not None:
            x = c1
            y = c2
        else:
            x = c1['x']
            y = c1['y']

        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]

    def for_each_location(self, fn):
        for y in range(self.height):
            for x in range(self.width):
                fn(self.cells[y][x])

    def get_locations_in_random_order(self):
        shuffled_locations = [loc for row in self.cells for loc in row]
        shuffle(shuffled_locations)
        return shuffled_locations
