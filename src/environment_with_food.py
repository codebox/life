from random import random
from environment_2d_grid import Environment2DGrid


class EnvironmentWithFood(Environment2DGrid):

    def _update_state_on_agent_move(self, agent, location):
        energy = agent['energy']
        agent['energy'] = min(energy+0.01, 1)
        location['food'] = 0

    def _init_location_state(self, location):
        location['food'] = random()
        return location

    def _init_agent_state(self, agent):
        agent['energy'] = 0
        return agent

    def tick(self):
        for col in self.state['locations']:
            for cell in col:
                cell['food'] = min(cell['food'] + 0.003 * random(), 1)
