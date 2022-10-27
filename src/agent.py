from abc import ABC, abstractmethod
from random import choice
from environment import *

class Agent(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def act(self, state_view, actions):
        return

    def __str__(self):
        return str(self.id)

class AgentRandom(Agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, state_view, actions):
        return choice(actions)

class AgentMaxFood(Agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, state_view, actions):
        if state_view[VIEW_ENERGY] > 1.5:
            return ACTION_REPRODUCE

        food = {k: state_view[k] for k in [VIEW_FOOD_NORTH, VIEW_FOOD_SOUTH, VIEW_FOOD_EAST, VIEW_FOOD_WEST]}
        max_food = max(food, key=food.get)
        return {
            VIEW_FOOD_NORTH: ACTION_MOVE_NORTH,
            VIEW_FOOD_SOUTH: ACTION_MOVE_SOUTH,
            VIEW_FOOD_WEST: ACTION_MOVE_WEST,
            VIEW_FOOD_EAST: ACTION_MOVE_EAST
        }[max_food]
