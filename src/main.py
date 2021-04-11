from environment_2d_grid import Environment2DGrid
from agent_basic import AgentBasic
from random import shuffle

SIZE=20
ROUNDS=10
environment = Environment2DGrid(SIZE)
agents = [AgentBasic(i) for i in range(3)]
environment.save_metadata()
environment.populate(agents)

for t in range(ROUNDS):
    shuffle(agents)
    for agent in agents:
        view = environment.get_view(agent)
        action = agent.act(view)
        environment.update(agent, action)

    environment.save()

