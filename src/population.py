from random import choice
from agent.herbivore import Herbivore
from agent.carnivore import Carnivore


class Population:
    def __init__(self, config):
        self.config = config
        self.agents = []
        self.next_id = 1
        for species_name in config['species'].keys():
            self.agents.extend(self._build_agents_of_type(species_name))

    def _build_agents_of_type(self, species_name):
        return [self._build_agent_of_type(species_name) for _ in range(self.config['species'][species_name]['count'])]

    def _build_agent_of_type(self, species_name):
        config = self.config['species'][species_name]
        if species_name == 'herbivore':
            agent = Herbivore(config)

        elif species_name == 'carnivore':
            agent = Carnivore(config)

        else:
            assert False, 'Unknown agent name: ' + species_name

        agent.id = self.next_id
        self.next_id += 1
        return agent

    def size(self):
        return len(self.agents)

    def is_viable(self):
        return self.size() >= self.config['minimum']

    def get_random_agent(self):
        return choice(self.agents)

    def get_agent_by_id(self, id):
        return next((agent for agent in self.agents if agent.id == id), None)

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def reproduce(self, parent_agent):
        species_name = parent_agent.species_name
        child_agent = self._build_agent_of_type(species_name)
        child_agent.network = parent_agent.network.copy(delta=self.config['network_mutation_rate'])
        self.agents.append(child_agent)
        return child_agent
