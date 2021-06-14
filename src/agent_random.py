import random

class AgentRandom:
    def __init__(self, id):
        self.id = id
        self.position = None

    def act(self, view):
        return random.choice(['L','R','U','D'])

    def __str__(self):
        return str(self.id)