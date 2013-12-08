from bge import logic, events, render
import mathutils

import Sprites
import util

import tag

# --- jetpack -----------------------------------------------------------------

def update(self, args):
    self.obj.applyForce(mathutils.Vector([0, 0, 70]))

tag.add('jetpack',
        events = dict(
            update = update,
            )
        )


# --- player ------------------------------------------------------------------

def findChild(self, f):
    for o in self.obj.children:
        if f(o):
            return o
    return None

def create(self, args):
    self.sprite = [o for o in self.obj.children if 'Spr' in o.name][0]
    self.animations = {
            'walk': [['PlayerWalkR', 0, 1, 2], 7],
            'idle': [['PlayerWalkR', 0], 1]
            }

    self.keys = {
            'left': events.LEFTARROWKEY,
            'right': events.RIGHTARROWKEY,
            'jump': events.UPARROWKEY
            }

    self.friction = 0.4
    self.accel = 0.8 + self.friction
    self.maxspd = 10.0 + self.friction
    self.jumpspd = 15

    self.touch = self.obj.sensors['Collision']

    groundSensorObj = findChild(self, lambda o: o.name == 'GroundSensor')
    self.groundTouch = groundSensorObj.sensors['Collision']

def animate(self):
    mv = self.obj.getLinearVelocity()

    if abs(mv.x) > 0.1:
        self.anim = 'walk'
    else:
        self.anim = 'idle'

    anim = self.animations[self.anim]
    self.sprite['spranim'] = anim[0]
    self.sprite['sprfps'] = anim[1]
    Sprites.SpriteMesh(self.sprite)

def update(self, args):
    mv = self.obj.getLinearVelocity()

    # apply friction
    mvf = mathutils.Vector(mv)
    mvf.y, mvf.z = 0, 0
    if mvf.magnitude > self.friction:
        mvf.magnitude -= self.friction
    else:
        mvf.magnitude = 0
    mv.x = mvf.x

    # left/right controls
    if util.keyDown(self.keys['left']):
        mv.x -= self.accel
    elif util.keyDown(self.keys['right']):
        mv.x += self.accel

    # jetpack
    if util.keyJustPressed(events.SKEY):
        self.tag('jetpack')
    if util.keyJustReleased(events.SKEY):
        self.untag('jetpack')

    # weird jump
    if util.keyJustPressed(self.keys['jump']):
        grounded = False
        for other in self.groundTouch.hitObjectList:
            print(other.name) # DEBUGGING
            if 'solid' in other:
                grounded = True
        if grounded:
            mv.z = self.jumpspd

    # max speed, 2d constraints
    mv.x = self.maxspd if mv.x > self.maxspd else mv.x
    mv.x = -self.maxspd if mv.x < -self.maxspd else mv.x
    mv.y = 0
    self.obj.setLinearVelocity(mv)
    self.obj.worldPosition.y = 0

    animate(self)

def collide(self, args):
    pass

tag.add('player',
        events = dict(
            create = create,
            update = update,
            collide = collide
            )
        )


