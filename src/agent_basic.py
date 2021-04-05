class AgentBasic:
    def __init__(self, id):
        self.id = id
        self.position = None

    def act(self, view):
        pass

    def __str__(self):
        return str(self.id)