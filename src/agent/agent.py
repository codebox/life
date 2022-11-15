from abc import ABC, abstractmethod
from .network import Network
import numpy as np


class Agent(ABC):
    def __init__(self, config, species_name):
        self.config = config
        self.species_name = species_name
        self.network = Network(
            len(self.get_view_attributes()),
            config['hidden_layer_size'],
            len(self.get_actions())
        )
        self.coords = None
        self.energy = config['energy']['initial']
        self.id = None

    def act(self, view):
        l = list(view.values())
        r = np.argmax(self.network.calc([l]))
        return [a for a in self.get_actions()][r]

    @abstractmethod
    def get_view_attributes(self):
        pass

    @abstractmethod
    def get_actions(self):
        pass

    @abstractmethod
    def view(self):
        pass

    @abstractmethod
    def update(self, environment, action):
        pass
