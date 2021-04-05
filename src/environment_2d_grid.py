from random import randrange

GRID_WALL = 'W'
GRID_FREE = ' '
GRID_AGENT = 'A'

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

        print(self.__grid_to_string(view))
        print()
        return view

    def update(self, agent, action):
        pass

    def __grid_to_string(self, grid):
        rows = []
        for row in grid:
            rows.append(','.join(map(lambda c: str(c) if c else '_', row)))
        return '\n'.join(rows)

    def __str__(self):
        return self.__grid_to_string(self.grid)
