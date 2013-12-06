from bge import logic

def keyDown(keycode):
    return logic.keyboard.events[keycode] == logic.KX_INPUT_ACTIVE
def keyJustPressed(keycode):
    return logic.keyboard.events[keycode] == logic.KX_INPUT_JUST_ACTIVATED

def test(cont):
    pass
    #for o in cont.sensors['Collision'].hitObjectList:
        #print(o.name)

