import player

classes = {
        'Player': player.Player
        }

def update(cont):
    obj = cont.owner

    if not 'actor' in obj:
        cls = classes[obj.get('class_name')]
        obj['actor'] = cls(obj, cont)
    else:
        obj['actor'].update()

def collide(cont):
    obj = cont.owner
    obj['actor'].collide()

