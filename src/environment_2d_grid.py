from random import randrange
import json

GRID_WALL = 'W'
GRID_FREE = ' '
GRID_AGENT = 'A'

ACTION_MOVE_UP = 'U'
ACTION_MOVE_DOWN = 'D'
ACTION_MOVE_LEFT = 'L'
ACTION_MOVE_RIGHT = 'R'

class Environment2DGrid():
    def __init__(self, size):
        self.size = size
        self.grid = [[None] * size for n in range(size)]

    def populate(self, agents):
        for agent in agents:
            while True:
                x = randrange(self.size)
                y = randrange(self.size)
                if self.grid[x][y] is None:
                    self.grid[x][y] = agent
                    agent.position = x, y
                    break

    def __get_grid_item(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return GRID_WALL

        if self.grid[x][y]:
            return GRID_AGENT
        else:
            return GRID_FREE

    def get_view(self, agent):
        view_radius = 1
        agent_x, agent_y = agent.position
        view = []
        for x in range(agent_x - view_radius, agent_x + view_radius + 1):
            view_row = []
            for y in range(agent_y - view_radius, agent_y + view_radius + 1):
                view_row.append(self.__get_grid_item(x,y))
            view.append(view_row)

        return view

    def __move_agent(self, agent, x, y):
        self.grid[x][y] = agent
        agent.position = x, y

    def update(self, agent, action):
        x_delta = 1 if action == ACTION_MOVE_RIGHT else -1 if action == ACTION_MOVE_LEFT else 0
        y_delta = 1 if action == ACTION_MOVE_DOWN else -1 if action == ACTION_MOVE_UP else 0
        old_x, old_y = agent.position
        new_x = old_x + x_delta
        new_y = old_y + y_delta
        if self.__is_vacant(new_x, new_y):
            self.grid[old_x][old_y] = None
            self.__move_agent(agent, new_x, new_y)

    def __is_vacant(self, x, y):
        return self.__get_grid_item(x, y) == GRID_FREE

    def __grid_to_string(self, grid):
        rows = []
        for row in grid:
            rows.append(','.join(map(lambda c: str(c) if c else '_', row)))
        return '\n'.join(rows)

    def save_metadata(self):
        with open('public/metadata.json', 'w') as f:
            json.dump({'h':self.size, 'w':self.size}, f)

    def save(self):
        rows = []
        for row in self.grid:
            rows.append(list(map(lambda c: str(c) if c else ' ', row)))

        with open('public/state.json', 'w') as f:
            json.dump(rows, f)

    def __str__(self):
        return self.__grid_to_string(self.grid)
