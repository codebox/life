import json


class Persistence:
    def __init__(self, save_location, web_location):
        self.save_location = save_location
        self.web_location = web_location

    def restore_environment(self):
        pass

    def environment_to_json(self, environment):
        def get_agent_colour(agent):
            energy_factor = min(1, agent.energy)
            inputs = [1] * agent.network.input_size
            result = agent.network.calc([inputs])[0]
            hue = 0
            for i, r in enumerate(result):
                hue += r * i * 360 / len(result)

            return 'hsla({}, 100%, 50%, {})'.format(hue, energy_factor)

        def get_details(cell):
            details = dict(cell)
            if 'agent' in cell:
                agent = environment.population.get_agent_by_id(cell['agent']['id'])
                details['agent'] = {'colour': get_agent_colour(agent), 'id': cell['agent']['id'], 'type': agent.species_name}
            return details

        with open('{}/state.json'.format(self.web_location), 'w') as f:
            cells = [get_details(cell) for row in environment.locations.cells for cell in row]
            json.dump({'locations': cells, 'population': environment.population.size(), 'age': environment.update_count}, f)

    def metadata_to_json(self, environment):
        with open('{}/metadata.json'.format(self.web_location), 'w') as f:
            json.dump({'h': environment.locations.height, 'w': environment.locations.width}, f)
