from .agent import Agent
from enum import Enum
from random import choice

class ViewAttributes(Enum):
    ENERGY = 1
    FOOD_NORTH = 2
    FOOD_SOUTH = 3
    FOOD_EAST = 4
    FOOD_WEST = 5
    BLOCK_NORTH = 6
    BLOCK_SOUTH = 7
    BLOCK_EAST = 8
    BLOCK_WEST = 9

class Actions(Enum):
    EAT = 1
    MOVE_NORTH = 2
    MOVE_SOUTH = 3
    MOVE_EAST = 4
    MOVE_WEST = 5
    REPRODUCE = 6

class Herbivore(Agent):
    def __init__(self, config):
        super().__init__(config, 'herbivore')

    def view(self, environment):
        def get_food(loc):
            return loc['food'] if loc else 0

        def get_block(loc):
            return 0 if loc and 'agent' not in loc else 1

        x = self.coords['x']
        y = self.coords['y']
        location_north = environment.locations.get(x, y-1)
        location_south = environment.locations.get(x, y+1)
        location_east = environment.locations.get(x+1, y)
        location_west = environment.locations.get(x-1, y)

        return {
            ViewAttributes.ENERGY: self.energy,
            ViewAttributes.FOOD_NORTH: get_food(location_north),
            ViewAttributes.FOOD_SOUTH: get_food(location_south),
            ViewAttributes.FOOD_EAST: get_food(location_east),
            ViewAttributes.FOOD_WEST: get_food(location_west),
            ViewAttributes.BLOCK_NORTH: get_block(location_north),
            ViewAttributes.BLOCK_SOUTH: get_block(location_south),
            ViewAttributes.BLOCK_EAST: get_block(location_east),
            ViewAttributes.BLOCK_WEST: get_block(location_west)
        }

    def _attempt_move(self, environment, x, y):
        new_location = environment.locations.get(x, y)

        if new_location and 'agent' not in new_location:
            environment.move_agent_to_location(self, new_location)
            energy_cost = self.config['energy']['move_success']
        else:
            energy_cost = self.config['energy']['move_fail']

        self.energy -= energy_cost

    def _attempt_eat(self, environment):
        location = environment.locations.get(self.coords)
        energy_gain = location['food']

        if energy_gain > 0:
            location['food'] = 0
            self.energy += energy_gain
        else:
            self.energy -= self.config['energy']['eat_fail']

    def _attempt_reproduce(self, environment):
        success = False
        energy_transfer = self.config['energy']['initial']
        if self.energy > energy_transfer:
            x = self.coords['x']
            y = self.coords['y']
            available_locations = [l for l in [
                environment.locations.get(x+1, y),
                environment.locations.get(x-1, y),
                environment.locations.get(x, y+1),
                environment.locations.get(x, y-1)
            ] if l and 'agent' not in l]
            if available_locations:
                spawn_location = choice(available_locations)
                child = environment.population.reproduce(self)
                child.energy = energy_transfer
                self.energy -= energy_transfer
                environment.move_agent_to_location(child, spawn_location)
                success = True

        if not success:
            self.energy -= self.config['energy']['reproduce_fail']

    def update(self, environment, action):
        x = self.coords['x']
        y = self.coords['y']

        if action == Actions.MOVE_NORTH:
            self._attempt_move(environment, x, y-1)
        elif action == Actions.MOVE_SOUTH:
            self._attempt_move(environment, x, y+1)
        elif action == Actions.MOVE_EAST:
            self._attempt_move(environment, x+1, y)
        elif action == Actions.MOVE_WEST:
            self._attempt_move(environment, x-1, y)
        elif action == Actions.EAT:
            self._attempt_eat(environment)
        elif action == Actions.REPRODUCE:
            self._attempt_reproduce(environment)
        else:
            assert False, 'Unexpected action: ' + str(action)

        self.energy -= self.config['energy']['ageing']

    def get_view_attributes(self):
        return ViewAttributes

    def get_actions(self):
        return Actions
