from bge import logic, events, render
import pdb
import mathutils

import Sprites
import util

class Player:
    def __init__(self, obj, cont):
        self.obj = obj

        self.sprite = [o for o in obj.children if 'Spr' in o.name][0]
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

        self.touch = obj.sensors['Collision']

        groundSensorObj = self.findChild(lambda o: o.name == 'GroundSensor')
        self.groundTouch = groundSensorObj.sensors['Collision']

    def findChild(self, f):
        for o in self.obj.children:
            if f(o):
                return o
        return None

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

    def update(self):
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

        self.animate()

    def collide(self):
        pass


