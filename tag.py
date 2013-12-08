tags = {}

# oversees actor logic by describing actor response to events
class Tag:
    def __init__(self, name, events):
        self.name = name
        tags[self.name] = self
        self.events = events

# add or find tags
def add(name, **kwargs):
    Tag(name, kwargs['events'])
def get(name):
    return tags.get(name)

