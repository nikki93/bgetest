from bge import logic

# keys
def keyDown(keycode):
    return logic.keyboard.events[keycode] == logic.KX_INPUT_ACTIVE
def keyJustPressed(keycode):
    return logic.keyboard.events[keycode] == logic.KX_INPUT_JUST_ACTIVATED
def keyJustReleased(keycode):
    return logic.keyboard.events[keycode] == logic.KX_INPUT_JUST_RELEASED

