from random import randrange, random
import json
from environment import Environment
from abc import abstractmethod

ACTION_MOVE_UP = 'U'
ACTION_MOVE_DOWN = 'D'
ACTION_MOVE_LEFT = 'L'
ACTION_MOVE_RIGHT = 'R'

class Environment2DGrid(Environment):
    def __init__(self, size):
        super().__init__({
            'agents': {},
            'locations': [[self._init_location_state({'agent': None}) for _2 in range(size)] for _1 in range(size)]
        })
        self.size = size

    @abstractmethod
    def _init_agent_state(self, agent):
        return

    @abstractmethod
    def _update_state_on_agent_move(self, agent):
        return

    @abstractmethod
    def _init_location_state(self, location):
        return

    def populate(self, agents):
        for agent in agents:
            agent_id = agent.id
            self.state['agents'][agent_id] = self._init_agent_state({})
            while True:
                x = randrange(self.size)
                y = randrange(self.size)
                if self._is_vacant(x, y):
                    self._move_agent(agent, x, y)
                    break

    def _get_grid_item(self, x, y):
        if x >= 0 and x < self.size and y >=0 and y < self.size:
            return self.state['locations'][x][y]

    def _get_visible_state(self, agent):
        view_radius = 1
        agent_x, agent_y = self.state['agents'][agent.id]['position']
        view = {}
        for x in range(agent_x - view_radius, agent_x + view_radius + 1):
            for y in range(agent_y - view_radius, agent_y + view_radius + 1):
                key = '{} {}'.format(x - agent_x, y - agent_y)
                view[key] = self._get_grid_item(x,y)

        return view

    def _move_agent(self, agent, new_x, new_y):
        current_position = self.state['agents'][agent.id].get('position')
        if current_position:
            current_x, current_y = current_position
            self.state['locations'][current_x][current_y]['agent'] = None

        new_location = self.state['locations'][new_x][new_y]
        new_location['agent'] = agent.id
        agent_state = self.state['agents'][agent.id]
        agent_state['position'] = new_x, new_y
        self._update_state_on_agent_move(agent_state, new_location)

    def update(self, agent, action):
        x_delta = 1 if action == ACTION_MOVE_RIGHT else -1 if action == ACTION_MOVE_LEFT else 0
        y_delta = 1 if action == ACTION_MOVE_DOWN else -1 if action == ACTION_MOVE_UP else 0
        old_x, old_y = self.state['agents'][agent.id]['position']
        new_x = old_x + x_delta
        new_y = old_y + y_delta
        if self._is_vacant(new_x, new_y):
            self._move_agent(agent, new_x, new_y)

    def _is_vacant(self, x, y):
        location = self._get_grid_item(x, y)
        return location and not location['agent']

    def _grid_to_string(self, grid):
        rows = []
        for row in grid:
            rows.append(','.join(map(lambda c: str(c) if c else '_', row)))
        return '\n'.join(rows)

    def save_metadata(self):
        with open('public/metadata.json', 'w') as f:
            json.dump({'h':self.size, 'w':self.size}, f)

    @abstractmethod
    def tick(self):
        return

    def save(self):
        with open('public/state.json', 'w') as f:
            json.dump(self.state, f)

    def __str__(self):
        return self._grid_to_string(self.grid)
