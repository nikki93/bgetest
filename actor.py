import player
import tag

# stores all game logic data for an entity, has tags which
# are notified of events
class Actor:
    # bind to a Blender GameObject
    def __init__(self, obj):
        assert('actor' not in obj)
        self.obj = obj
        obj['actor'] = self
        self.tags = set(self.obj.get('tags', '').split())

    # add/remove tag
    def tag(self, tagName):
        self.tags.add(tagName)
    def untag(self, tagName):
        self.tags.remove(tagName)

    # trigger an event by calling all tag handlers
    def trigger(self, event, **kwargs):
        for tagName in self.tags:
            t = tag.get(tagName)
            if t and event in t.events:
                t.events[event](self, kwargs)

