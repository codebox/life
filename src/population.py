from agent import Agent, Network
from random import choice


class Population:
    def __init__(self, config):
        self.config = config
        self.next_agent_id = 1
        self.agents = [self._build_new_agent() for _ in range(config['population_size'])]

    def get_random_agent(self):
        return choice(self.agents)

    def add_new_agent(self, parent=None):
        new_agent = self._build_new_agent(parent)
        self.agents.append(new_agent)
        return new_agent

    def _build_new_agent(self, parent=None):
        agent_id = self.next_agent_id
        self.next_agent_id += 1

        if parent:
            network = parent.network.copy(delta=self.config['network_mutation_rate'])

        else:
            network = Network(
                len(self.config['view_attributes']),
                self.config['hidden_layer_size'],
                len(self.config['actions']),
            )

        return Agent(agent_id, network, self.config['actions'])

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def size(self):
        return len(self.agents)
