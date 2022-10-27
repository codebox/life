from random import randrange, random, choice
import json

ACTION_MOVE_NORTH = 'N'
ACTION_MOVE_SOUTH = 'S'
ACTION_MOVE_WEST = 'W'
ACTION_MOVE_EAST = 'E'
ACTION_STAY = 'STAY'
ACTION_REPRODUCE = 'REPRODUCE'

VIEW_FOOD_NORTH = 'FOOD_N'
VIEW_FOOD_SOUTH = 'FOOD_S'
VIEW_FOOD_WEST = 'FOOD_W'
VIEW_FOOD_EAST = 'FOOD_E'
VIEW_AGENT_NORTH = 'AGENT_N'
VIEW_AGENT_SOUTH = 'AGENT_S'
VIEW_AGENT_WEST = 'AGENT_W'
VIEW_AGENT_EAST = 'AGENT_E'
VIEW_ENERGY = 'ENERGY'

MAX_ENERGY = 20
INITIAL_ENERGY = 1
MOVE_ENERGY_COST = 0.3
NO_MOVE_ENERGY_COST = 0.1
FOOD_REGROWTH_RATE = 0.03
REPRODUCE_AFTER=10

class Environment2D:
    def __init__(self, width, height, population):
        self.width = width
        self.height = height
        self.t = 0
        locations = [{
            'id': self._get_location_id(x, y),
            'x': x,
            'y': y,
            'food': random()
        } for x in range(width) for y in range(height)]
        self.state = {
            'locations': {loc['id']: loc for loc in locations},
            'agent_data': {}
        }
        self.population = population
        for agent in population.get_all():
            while True:
                x = randrange(width)
                y = randrange(height)
                if self._is_vacant(x, y):
                    self._add_new_agent(agent, x, y)
                    break

    def get_view(self, agent):
        def get_location_value(location, value, present_value=None):
            if location:
                value = location.get(value, None)
                if value:
                    if present_value:
                        return present_value
                    else:
                        return value
            return 0

        agent_location = self._get_location_of_agent(agent)
        agent_data = self.state['agent_data'][agent.id]
        agent_x = agent_location['x']
        agent_y = agent_location['y']
        n_location = self._get_location(agent_x, agent_y - 1)
        s_location = self._get_location(agent_x, agent_y + 1)
        w_location = self._get_location(agent_x - 1, agent_y)
        e_location = self._get_location(agent_x + 1, agent_y)
        view = {
            VIEW_FOOD_NORTH: get_location_value(n_location, 'food'),
            VIEW_FOOD_SOUTH: get_location_value(s_location, 'food'),
            VIEW_FOOD_WEST: get_location_value(w_location, 'food'),
            VIEW_FOOD_EAST: get_location_value(e_location, 'food'),
            VIEW_AGENT_NORTH: get_location_value(n_location, 'agent_id', 1),
            VIEW_AGENT_SOUTH: get_location_value(s_location, 'agent_id', 1),
            VIEW_AGENT_WEST: get_location_value(w_location, 'agent_id', 1),
            VIEW_AGENT_EAST: get_location_value(e_location, 'agent_id', 1),
            VIEW_ENERGY: agent_data['energy']
        }

        return view

    def update(self, agent, action):
        def attempt_move(old_x, old_y, new_x, new_y):
            if self._is_vacant(new_x, new_y):
                old_location = self._get_location(old_x, old_y)
                new_location = self._get_location(new_x, new_y)
                del old_location['agent_id']
                new_location['agent_id'] = agent.id
                current_food = new_location['food']
                current_agent_energy = self.state['agent_data'][agent.id]['energy'] - MOVE_ENERGY_COST
                current_agent_appetite = MAX_ENERGY - current_agent_energy
                if current_agent_appetite > current_food:
                    new_agent_energy = current_agent_energy + current_food
                    new_food = 0
                else:
                    new_agent_energy = MAX_ENERGY
                    new_food = current_food - current_agent_appetite

                self.state['agent_data'][agent.id]['energy'] = new_agent_energy
                new_location['food'] = new_food
            else:
                self.state['agent_data'][agent.id]['energy'] -= NO_MOVE_ENERGY_COST

        def attempt_stay(agent_x, agent_y):
            current_energy = self.state['agent_data'][agent.id]['energy']
            current_food = self._get_location(agent_x, agent_y)['food']
            appetite = MAX_ENERGY - current_energy
            consume = min(current_food, appetite)
            self.state['agent_data'][agent.id]['energy'] += (consume - NO_MOVE_ENERGY_COST)
            self._get_location(agent_x, agent_y)['food'] -= consume

        agent_location = self._get_location_of_agent(agent)
        agent_current_x = agent_location['x']
        agent_current_y = agent_location['y']

        if action == ACTION_MOVE_NORTH:
            attempt_move(agent_current_x, agent_current_y, agent_current_x, agent_current_y - 1)
        elif action == ACTION_MOVE_SOUTH:
            attempt_move(agent_current_x, agent_current_y, agent_current_x, agent_current_y + 1)
        elif action == ACTION_MOVE_WEST:
            attempt_move(agent_current_x, agent_current_y, agent_current_x - 1, agent_current_y)
        elif action == ACTION_MOVE_EAST:
            attempt_move(agent_current_x, agent_current_y, agent_current_x + 1, agent_current_y)
        elif action == ACTION_REPRODUCE:
            self._copy_agent(agent)
        elif action == ACTION_STAY:
            attempt_stay(agent_current_x, agent_current_y)
        else:
            assert False

        # if self.state['agent_data'][agent.id]['energy'] <= 0:
        #     self._remove_agent(agent)

    def save(self):
        with open('public/state.json', 'w') as f:
            json.dump(self.state, f)

    def save_metadata(self):
        with open('public/metadata.json', 'w') as f:
            json.dump({'h': self.height, 'w': self.width}, f)

    def tick(self):
        for loc in self.state['locations'].values():
            loc['food'] = min(loc['food'] + FOOD_REGROWTH_RATE * random(), 1)
        self.t += 1
        if self.t % REPRODUCE_AFTER == 0:
            all_agents = sorted(self.population.get_all(), key=lambda agent: self.state['agent_data'][agent.id]['energy'])
            n = int(len(all_agents)/2)
            weakest_half = all_agents[:n]
            for weak_agent in weakest_half:
                self._remove_agent(weak_agent)

            for a in self.population.get_all():
                self._copy_agent(a)

    def _add_new_agent(self, agent, x, y):
        location = self._get_location(x, y)
        assert not location.get('agent_id', None)
        location['agent_id'] = agent.id
        self.state['agent_data'][agent.id] = {'energy': INITIAL_ENERGY}

    def _remove_agent(self, agent):
        self.population.remove(agent)
        del self._get_location_of_agent(agent)['agent_id']
        del self.state['agent_data'][agent.id]

    def _copy_agent(self, agent):
        if self.state['agent_data'][agent.id]['energy'] <= INITIAL_ENERGY:
            return

        location = self._get_location_of_agent(agent)
        agent_x = location['x']
        agent_y = location['y']

        vacant_location_coords = [c for c in [
            (agent_x, agent_y - 1),
            (agent_x, agent_y + 1),
            (agent_x - 1, agent_y),
            (agent_x + 1, agent_y)] if self._is_vacant(c[0], c[1])
                                  ]
        if not vacant_location_coords:
            return

        child_location_coord = choice(vacant_location_coords)
        child = self.population.add(agent)
        self._add_new_agent(child, child_location_coord[0], child_location_coord[1])

        self.state['agent_data'][agent.id]['energy'] -= INITIAL_ENERGY

    def _is_vacant(self, x, y):
        location_id = self._get_location_id(x, y)
        location = self.state['locations'].get(location_id, None)
        return location and 'agent_id' not in location

    def _get_location_of_agent(self, agent):
        return next((loc for loc in self.state['locations'].values() if loc.get('agent_id', None) == agent.id), None)

    def _get_location(self, x, y):
        location_id = self._get_location_id(x, y)
        return self.state['locations'].get(location_id, None)

    def _get_location_id(self, x, y):
        return '{}:{}'.format(x, y)

    def get_view_values(self):
        return [VIEW_FOOD_NORTH, VIEW_FOOD_SOUTH, VIEW_FOOD_WEST, VIEW_FOOD_EAST,
                VIEW_AGENT_NORTH, VIEW_AGENT_SOUTH, VIEW_AGENT_WEST, VIEW_AGENT_EAST, VIEW_ENERGY]

    def get_actions(self):
        return [ACTION_MOVE_NORTH, ACTION_MOVE_SOUTH, ACTION_MOVE_WEST, ACTION_MOVE_EAST, ACTION_REPRODUCE, ACTION_STAY]

    def __str__(self):
        return str(self.locations)
