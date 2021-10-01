from environment_with_food import EnvironmentWithFood
# from agent_random import AgentRandom
from agent_hungry import AgentHungry
from random import shuffle
from time import sleep

SIZE=20
AGENTS=5
environment = EnvironmentWithFood(SIZE)
agents = [AgentHungry(i) for i in range(AGENTS)]
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
    sleep(1)

