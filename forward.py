import actor
import sys

# any attempts to access a field return triggers on actors
class Forward(object):
    def __init__(self, module):
        self.module = module
    def __getattr__(self, name):
        try:
            return getattr(self.module, name)
        except AttributeError:
            return self.createCall(name)

    def createCall(self, event):
        def call(cont):
            obj = cont.owner

            # create and bind new actor if needed
            if not 'actor' in obj:
                actor.Actor(obj)
                obj['actor'].trigger('create')

            obj['actor'].trigger(event)

        return call

sys.modules[__name__] = Forward(sys.modules[__name__])

