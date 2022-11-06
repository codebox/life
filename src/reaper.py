class Reaper:
    def __init__(self, p, environment):
        self.p = p
        self.environment = environment
        self.count = 0

    def _evaluate(self, agent):
        x = self.environment._get_location_of_agent(agent)['x']
        y = self.environment._get_location_of_agent(agent)['y']
        return -(x * x + y * y)
        # return self.environment.state['agent_data'][agent.id]['energy']

    def reap(self, population):
        print('Generation {}'.format(self.count))
        self.count += 1
        all_agents = population.get_all()
        all_agents_sorted = sorted(all_agents, key=lambda agent: self._evaluate(agent))
        survivor_count = int(len(all_agents) * self.p)
        survivors = all_agents_sorted[-survivor_count:]

        for agent in all_agents:
            self.environment._remove_agent(agent)

        population.new_generation(survivors)
