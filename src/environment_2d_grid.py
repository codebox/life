from random import randrange

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
                    break

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(','.join(map(lambda c: str(c) if c else '_', row)))
        return '\n'.join(rows)


