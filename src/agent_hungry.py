import random
from agent import Agent

MOVEMENT_MAP = {
    '0 -1': 'U',
    '0 1': 'D',
    '-1 0': 'L',
    '1 0': 'R'
}
class AgentHungry(Agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, state_view):
        movements_to_food = []
        for view_key, direction in MOVEMENT_MAP.items():
            movements_to_food.append((direction, state_view[view_key]))

        return max(movements_to_food, key=(lambda v: v[1]['food'] if v[1] else -1))[0]

