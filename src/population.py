from agent import Agent, Network
from random import choice


class Population:
    def __init__(self, config):
        self.config = config
        self.next_agent_id = 1
        self.agents = [self._build_agent() for _ in range(config['population_size'])]

    def get_random_agent(self):
        return choice(self.agents)

    def size(self):
        return len(self.agents)

    def _build_agent(self, parent=None):
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

