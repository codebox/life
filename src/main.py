from environment_2d_grid import Environment2DGrid
from agent_basic import AgentBasic
from random import shuffle
import asyncio
from webserver.server import Server

state = []
async def go():
    s = Server(state)
    await s.start()
    await s.stop()

asyncio.run(go())

# environment = Environment2DGrid(10)
# agents = [AgentBasic(i) for i in range(3)]
#
# environment.populate(agents)
#
# for t in range(10):
#     print(environment)
#     shuffle(agents)
#     for agent in agents:
#         view = environment.get_view(agent)
#         action = agent.act(view)
#         environment.update(agent, action)
#         # print(environment)

