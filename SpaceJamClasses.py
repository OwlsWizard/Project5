"""
Highest level classes for SpaceJam.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task

from CollideObjectBase import *

#import math

class Universe(InverseSphereCollideObj):
    def __init__(self,
                 loader: Loader, parentNode: NodePath,
                 nodeName: str, modelPath: str,   
                 texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):

        super(Universe, self).__init__(loader, parentNode, nodeName, modelPath, Vec3(0,0,0), 0.9)

        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)    

class Planet(SphereCollideObj):
    def __init__(self,
                 loader: Loader, parentNode: NodePath,
                 nodeName: str, modelPath: str,   
                 texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):

        super(Planet, self).__init__(loader, parentNode, nodeName, modelPath, Vec3(0,0,0), 1.1)
        
        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)       

class SpaceStation(CapsuleCollidableObject): 
    def __init__(self,
                 loader: Loader, parentNode: NodePath,
                 nodeName: str, modelPath: str,   
                 texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):

        super(SpaceStation, self).__init__(loader, parentNode, nodeName, modelPath, 5, 0, 5, -7.5, 0, -10, 10)
        
        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)      

class Drone(CapsuleCollidableObject):
    
    droneCount = 0
    
    def __init__(self,
                 loader: Loader, parentNode: NodePath,
                 nodeName: str, modelPath: str,   
                 texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):

        super(Drone, self).__init__(loader, parentNode, nodeName, modelPath, 0, 1.5, 1.5, 0, -1.5, -1.5, 2) 
        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)      


class Player(CapsuleCollidableObject, ShowBase):
    def __init__(self,
                 loader: Loader, parentNode: NodePath,
                 nodeName: str, modelPath: str,   
                 texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float,
                 taskMgr: Task, renderer: NodePath):

        super(Player, self).__init__(loader, parentNode, nodeName, modelPath, 0, 0, 5, 0, 0, 4, 15) 
        
        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)  
        
        self.taskManager = taskMgr
        self.render = renderer
        
        self.turnRate = 0.5
        self.setKeybinds()

    def setKeybinds(self): 
        self.accept("space", self.thrust, [1])
        self.accept("space-up", self.thrust, [0])
        
        self.accept("a", self.leftTurn, [1])
        self.accept("a-up", self.leftTurn, [0])
        
        self.accept("d", self.rightTurn, [1])
        self.accept("d-up", self.rightTurn, [0])
        
        self.accept("w", self.upTurn, [1])
        self.accept("w-up", self.upTurn, [0])

        self.accept("s", self.downTurn, [1])
        self.accept("s-up", self.downTurn, [0])
        
        self.accept("arrow_left", self.leftRoll, [1])
        self.accept("arrow_left-up", self.leftRoll, [0])

        self.accept("arrow_right", self.rightRoll, [1])
        self.accept("arrow_right-up", self.rightRoll, [0])
             
    def thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyThrust, "forward-thrust")
        else:
            self.taskManager.remove("forward-thrust")
            
    def leftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyLeftTurn, "left-turn")
        else:
            self.taskManager.remove("left-turn")
            #print(self.modelNode.getHpr())
    
    def rightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyRightTurn, "right-turn")
        else:
            self.taskManager.remove("right-turn")
            #print(self.modelNode.getHpr())    

    def upTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyUpTurn, "up-turn")
        else:
            self.taskManager.remove("up-turn")
            #print(self.modelNode.getHpr())
    
    def downTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyDownTurn, "down-turn")
        else:
            self.taskManager.remove("down-turn")
            #print(self.modelNode.getHpr())
            
    def leftRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyLeftRoll, "left-roll")
        else:
            self.taskManager.remove("left-roll")
            #print(self.modelNode.getHpr())                   

    def rightRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyRightRoll, "right-roll")
        else:
            self.taskManager.remove("right-roll")
            #print(self.modelNode.getHpr())    
                
    def applyThrust(self, task):
        shipSpeed = 5 #rate of movement
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward()) #Pulls direction ship is facing
        """
        FIXME: If trajectory is set to self.modelNode, then the ship will fly forward regardless of the direction the camera is facing.
        unknown cause, passing in a seperate renderer like is implemented now seems to fix the issue.
        """
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * shipSpeed) #controls movement itself
        return Task.cont
    
    #FIXME: Old methods for relative direction error at odd angles. Scraped for now, might try to reimplement later. 
    """
    def applyLeftTurn(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorLR(rotation)
        vectorX = vector[0]
        vectorY = vector[1]
        self.modelNode.setHpr(self.modelNode.getH() + vectorX, self.modelNode.getP() + vectorY, self.modelNode.getR())
        return Task.cont    
    
    def applyRightTurn(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorLR(rotation)
        vectorX = vector[0]
        vectorY = vector[1]
        self.modelNode.setHpr(self.modelNode.getH() - vectorX, self.modelNode.getP() - vectorY, self.modelNode.getR())
        return Task.cont    

    def applyUpTurn(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorUD(rotation)
        vectorX = vector[0] 
        vectorY = vector[1] 
        self.modelNode.setHpr(self.modelNode.getH() + vectorX, self.modelNode.getP() + vectorY, self.modelNode.getR())
        return Task.cont   

    def applyDownTurn(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorUD(rotation)
        vectorX = vector[0] 
        vectorY = vector[1] 
        self.modelNode.setHpr(self.modelNode.getH() - vectorX, self.modelNode.getP() - vectorY, self.modelNode.getR())
        return Task.cont   

    #FIXME: Need logic to determine if ship is up or down relative to world (180 <= x < 270 is cutoff for directions reversed, inclusive)
    def pullVectorLR(self, hpr: Vec3):
        
        Pulls XZ vectors to increase in movement direction for left, right movement, and returns as a list in format [x,y]. 
        Needed to fix movement issues where tilting "left" tilts ship left relative to world, not the ship itself
        
        rotation = hpr[2]
        relativeX = self.turnRate * math.cos(math.radians(rotation))
        relativeY = self.turnRate * math.sin(math.radians(rotation))
        cordinateList = [relativeX, relativeY]
        
        return cordinateList
    
    def pullVectorUD(self, hpr: Vec3):
        
        Pulls XZ vector to increase in movement direction for Up, Down movement, abd returns as a list in format [x,z]. 
        Needed to fix movement issues where tilting "up" tilts ship up relative to world, not the ship itself.
        
        rotation = hpr[2] + 90
        relativeX = self.turnRate * math.cos(math.radians(rotation))
        relativeY = self.turnRate * math.sin(math.radians(rotation))
        cordinateList = [relativeX, relativeY]
        
        return cordinateList
    """
   
    #OLD METHODS FOR TURNING
    def applyLeftTurn(self, task):
        self.modelNode.setH(self.modelNode.getH() + self.turnRate)
        return Task.cont
    
    def applyRightTurn(self, task):
        self.modelNode.setH(self.modelNode.getH() + -self.turnRate)
        return Task.cont
    
    def applyUpTurn(self, task):
        self.modelNode.setP(self.modelNode.getP() + self.turnRate)
        return Task.cont
  
    def applyDownTurn(self, task):
        self.modelNode.setP(self.modelNode.getP() + -self.turnRate)
        return Task.cont
    
    def applyLeftRoll(self, task): 
        self.modelNode.setR(self.modelNode.getR() + -self.turnRate)
        return Task.cont

    def applyRightRoll(self, task): 
        self.modelNode.setR(self.modelNode.getR() + self.turnRate)
        return Task.cont      