import random
from agent import Agent

class AgentRandom(Agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, state_view):
        return random.choice(['L','R','U','D'])

