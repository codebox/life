from random import random, randint, choice
from logger import log


class Environment:
    def __init__(self, config, population):
        self.config = config
        self.population = population
        self.grid = Grid(config['grid_width'], config['grid_height'], self._init_cell)
        self._populate_grid_with_agents()

    def _init_cell(self, cell):
        cell['food'] = self.config['cell_min_init_energy'] + random() * (1 - self.config['cell_min_init_energy'])
        return cell

    def _populate_grid_with_agents(self):
        for agent in self.population.agents:
            while True:
                cell = self.grid.get_random()
                if self._put_agent_in_cell(agent, cell):
                    agent.state['energy'] = self.config['agent_energy']['initial']
                    break

    def _put_agent_in_cell(self, agent, cell):
        if cell and 'agent' not in cell:
            if 'x' in agent.state:
                self._remove_agent_from_cell(agent)

            agent.state['x'] = cell['x']
            agent.state['y'] = cell['y']
            cell['agent'] = agent.id
            return True

    def _remove_agent_from_cell(self, agent):
        cell = self.grid.get(agent.state['x'], agent.state['y'])
        del cell['agent']

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
            return {'r': 1, 'g': 0, 'b': 0}
        else:
            return {'r': 0, 'g': cell['food'], 'b': 0}

    def _attempt_move(self, agent, x, y):
        new_cell = self.grid.get(x, y)

        if new_cell and 'agent' not in new_cell:
            self._put_agent_in_cell(agent, new_cell)
            energy_cost = self.config['agent_energy']['move_success']
        else:
            energy_cost = self.config['agent_energy']['move_fail']

        agent.state['energy'] -= energy_cost

    def _attempt_eat(self, agent):
        x = agent.state['x']
        y = agent.state['y']
        cell = self.grid.get(x, y)
        energy_gain = cell['food']
        if energy_gain > 0:
            cell['food'] = 0
            agent.state['energy'] += energy_gain
        else:
            agent.state['energy'] -= self.config['agent_energy']['eat_fail']

    def _attempt_reproduce(self, parent):
        success = False
        if parent.state['energy'] >= self.config['agent_energy']['reproduce']:
            x = parent.state['x']
            y = parent.state['y']
            energy_transfer = self.config['agent_energy']['initial']
            available_locations = [l for l in [
                self.grid.get(x+1, y),
                self.grid.get(x-1, y),
                self.grid.get(x, y+1),
                self.grid.get(x, y-1)
            ] if l and 'agent' not in l]
            if available_locations:
                spawn_location = choice(available_locations)
                child = self.population.add_new_agent(parent)
                child.state['energy'] = energy_transfer
                parent.state['energy'] -= energy_transfer
                self._put_agent_in_cell(child, spawn_location)
                log.info('New agent added {}'.format(child.id))
                success = True

        if not success:
            parent.state['energy'] -= self.config['agent_energy']['reproduce_fail']

    def update(self, agent, action):
        # log.info('Agent {} {}'.format(agent.id, action))
        x = agent.state['x']
        y = agent.state['y']

        if action == 'move_north':
            self._attempt_move(agent, x, y - 1)
        elif action == 'move_south':
            self._attempt_move(agent, x, y + 1)
        elif action == 'move_west':
            self._attempt_move(agent, x - 1, y)
        elif action == 'move_east':
            self._attempt_move(agent, x + 1, y)
        elif action == 'reproduce':
            self._attempt_reproduce(agent)
        elif action == 'eat':
            self._attempt_eat(agent)

        self._check_for_agent_death(agent)

    def _check_for_agent_death(self, agent):
        if agent.state['energy'] <= 0:
            log.info('Agent {} died'.format(agent.id))
            self.population.remove_agent(agent)
            self._remove_agent_from_cell(agent)

    def tick(self, elapsed_time_seconds):
        def regrow_food(cell):
            current_food = cell['food']
            cell['food'] = min(1, current_food + self.config['environment_regeneration_rate'] * elapsed_time_seconds)

        self.grid.for_each_cell(regrow_food)

        for agent in self.population.agents:
            old_energy = agent.state['energy']
            new_energy = old_energy - self.config['agent_energy']['loss_per_second'] * elapsed_time_seconds
            agent.state['energy'] = new_energy
            self._check_for_agent_death(agent)

class Grid:
    def __init__(self, width, height, fn_init_cell):
        self.width = width
        self.height = height
        self.cells = [[fn_init_cell({'x': x, 'y': y}) for x in range(width)] for y in range(height)]

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]

    def for_each_cell(self, fn):
        for y in range(self.height):
            for x in range(self.width):
                fn(self.cells[y][x])

    def get_random(self):
        return self.get(randint(0, self.width-1), randint(0, self.height-1))

