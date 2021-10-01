from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def act(self, state_view):
        return

    def __str__(self):
        return str(self.id)