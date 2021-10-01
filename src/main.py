from environment_2d_grid import Environment2DGrid
from agent_random import AgentRandom
from random import shuffle
from time import sleep

SIZE=20
AGENTS=5
environment = Environment2DGrid(SIZE)
agents = [AgentRandom(i) for i in range(AGENTS)]
environment.save_metadata()
environment.populate(agents)

while True:
    shuffle(agents)
    for agent in agents:
        view = environment.get_view(agent)
        action = agent.act(view)
        environment.update(agent, action)
    environment.save()
    environment.tick()
    sleep(0.3)

