from time import sleep
from population import Population
from environment import Environment2D
from agent import AgentRandom, AgentMaxFood

GRID_SIZE = 30
POPULATION_SIZE = 10
population = Population(POPULATION_SIZE)
environment = Environment2D(GRID_SIZE, GRID_SIZE, population)
actions = environment.get_actions()
environment.save_metadata()

while True:
    for agent in population.get_all():
        view = environment.get_view(agent)
        action = agent.act(view, actions)
        environment.update(agent, action)

    environment.save()
    environment.tick()
    sleep(1)

