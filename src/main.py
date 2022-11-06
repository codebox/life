from time import sleep
from population import Population
from environment import Environment2D
from reaper import Reaper
from agent import AgentRandom, AgentMaxFood

GRID_SIZE = 40
POPULATION_SIZE = 100
MUTATION_FACTOR = 0.005
population = Population(POPULATION_SIZE, MUTATION_FACTOR)
environment = Environment2D(GRID_SIZE, GRID_SIZE, population)
reaper = Reaper(0.5, environment)
actions = environment.get_actions()
environment.save_metadata()

while True:
    for agent in population.get_all():
        view = environment.get_view(agent)
        action = agent.act(view, actions)
        environment.update(agent, action)

    environment.tick(reaper)
    # sleep(0.01)

