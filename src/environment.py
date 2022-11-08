from random import random, randint


class Environment:
    def __init__(self, config, population):
        self.config = config
        self.population = population
        self.grid = Grid(config['grid_width'], config['grid_height'], self._init_cell)
        self._populate_grid_with_agents()

    def _init_cell(self, cell):
        cell['food'] = random()
        return cell

    def _populate_grid_with_agents(self):
        for agent in self.population.agents:
            while True:
                cell = self.grid.get_random()
                if 'agent' not in cell:
                    cell['agent'] = agent.id
                    agent.state['x'] = cell['x']
                    agent.state['y'] = cell['y']
                    agent.state['energy'] = self.config['agent_initial_energy']
                    break

    def get_view(self, agent):
        x = agent.state['x']
        y = agent.state['y']

        n_colour = self._get_cell_colour(x, y-1)
        s_colour = self._get_cell_colour(x, y+1)
        w_colour = self._get_cell_colour(x-1, y)
        e_colour = self._get_cell_colour(x+1, y)

        return {
            'nr': n_colour['r'],
            'ng': n_colour['g'],
            'nb': n_colour['b'],
            'sr': s_colour['r'],
            'sg': s_colour['g'],
            'sb': s_colour['b'],
            'er': e_colour['r'],
            'eg': e_colour['g'],
            'eb': e_colour['b'],
            'wr': w_colour['r'],
            'wg': w_colour['g'],
            'wb': w_colour['b'],
            'energy': agent.state['energy']
        }

    def _get_cell_colour(self, x, y):
        cell = self.grid.get(x, y)
        if not cell:
            return {'r': 0, 'g': 0, 'b': 0}
        elif 'agent' in cell:
            return {'r': 255, 'g': 0, 'b': 0}
        else:
            return {'r': 0, 'g': cell['food'] * 255, 'b': 0}

    def update(self, agent, action):
        pass


class Grid:
    def __init__(self, width, height, fn_init_cell):
        self.width = width
        self.height = height
        self.cells = [[fn_init_cell({'x': x, 'y': y}) for x in range(width)] for y in range(height)]

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]

    def get_random(self):
        return self.get(randint(0, self.width-1), randint(0, self.height-1))

