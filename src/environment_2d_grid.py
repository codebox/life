from random import randrange
import json
from environment import Environment

GRID_WALL = 'W'
GRID_FREE = ' '
GRID_AGENT = 'A'

ACTION_MOVE_UP = 'U'
ACTION_MOVE_DOWN = 'D'
ACTION_MOVE_LEFT = 'L'
ACTION_MOVE_RIGHT = 'R'

class Environment2DGrid(Environment):
    def __init__(self, size):
        super().__init__({
            'agents': {},
            'locations': [[None] * size for _ in range(size)]
        })
        self.size = size

    def populate(self, agents):
        for agent in agents:
            agent_id = agent.id
            agent_state = {}
            self.state['agents'][agent_id] = agent_state
            while True:
                x = randrange(self.size)
                y = randrange(self.size)
                if self._is_vacant(x, y):
                    self._move_agent(agent, x, y)
                    break

    def _get_grid_item(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return GRID_WALL

        if self.state['locations'][x][y]:
            return GRID_AGENT
        else:
            return GRID_FREE

    def _get_visible_state(self, agent):
        view_radius = 1
        agent_x, agent_y = self.state['agents'][agent.id]['position']
        view = []
        for x in range(agent_x - view_radius, agent_x + view_radius + 1):
            view_row = []
            for y in range(agent_y - view_radius, agent_y + view_radius + 1):
                view_row.append(self._get_grid_item(x,y))
            view.append(view_row)

        return view

    def _move_agent(self, agent, new_x, new_y):
        current_position = self.state['agents'][agent.id].get('position')
        if current_position:
            current_x, current_y = current_position
            self.state['locations'][current_x][current_y] = None

        self.state['locations'][new_x][new_y] = agent.id
        self.state['agents'][agent.id]['position'] = new_x, new_y

    def update(self, agent, action):
        x_delta = 1 if action == ACTION_MOVE_RIGHT else -1 if action == ACTION_MOVE_LEFT else 0
        y_delta = 1 if action == ACTION_MOVE_DOWN else -1 if action == ACTION_MOVE_UP else 0
        old_x, old_y = self.state['agents'][agent.id]['position']
        new_x = old_x + x_delta
        new_y = old_y + y_delta
        if self._is_vacant(new_x, new_y):
            self._move_agent(agent, new_x, new_y)

    def _is_vacant(self, x, y):
        return self._get_grid_item(x, y) == GRID_FREE

    def _grid_to_string(self, grid):
        rows = []
        for row in grid:
            rows.append(','.join(map(lambda c: str(c) if c else '_', row)))
        return '\n'.join(rows)

    def save_metadata(self):
        with open('public/metadata.json', 'w') as f:
            json.dump({'h':self.size, 'w':self.size}, f)

    def save(self):
        rows = []
        for row in self.state['locations']:
            rows.append(list(map(lambda c: str(c) if c else ' ', row)))

        with open('public/state.json', 'w') as f:
            json.dump(rows, f)

    def __str__(self):
        return self._grid_to_string(self.grid)
