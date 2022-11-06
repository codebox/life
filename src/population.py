from random import sample
from agent import AgentRandom, AgentMaxFood, AgentNetwork

class Population:
    def __init__(self, count, mutation_factor):
        self.next_id = 1
        self.agents = []
        self.count = count
        self.mutation_factor = mutation_factor
        for _ in range(count):
            self.add()

    def add(self, parent = None):
        if parent:
            new_agent = AgentNetwork(self.next_id, parent.network.copy(self.mutation_factor))
        else:
            new_agent = AgentNetwork(self.next_id)

        self.agents.append(new_agent)
        self.next_id += 1
        return new_agent

    def remove(self, agent_to_remove):
        self.agents.remove(agent_to_remove)

    def get_all(self):
        return sample(self.agents, len(self.agents))

    def new_generation(self, parents):
        self.agents = []
        parent_index = 0
        while len(self.agents) < self.count:
            self.add(parents[parent_index])
            parent_index = (parent_index + 1) % len(parents)

    def __str__(self):
        return str(self.agents)