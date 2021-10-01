import copy
from abc import ABC, abstractmethod


class Environment(ABC):
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def _get_visible_state(self, agent):
        return

    def get_view(self, agent):
        return copy.deepcopy(self._get_visible_state(agent))

    @abstractmethod
    def update(self, agent, action):
        return

    @abstractmethod
    def save(self):
        return

    @abstractmethod
    def tick(self):
        return

    def __str__(self):
        return str(self.state)
