from random import sample
from agent import AgentRandom, AgentMaxFood, AgentNetwork

class Population:
    def __init__(self, count):
        self.next_id = 1
        self.agents = []
        for _ in range(count):
            self.add()

    def add(self, parent = None):
        if parent:
            new_agent = AgentNetwork(self.next_id, parent.network.copy())
        else:
            new_agent = AgentNetwork(self.next_id)

        self.agents.append(new_agent)
        self.next_id += 1
        return new_agent

    def remove(self, agent_to_remove):
        self.agents.remove(agent_to_remove)

    def get_all(self):
        return sample(self.agents, len(self.agents))

    def __str__(self):
        return str(self.agents)