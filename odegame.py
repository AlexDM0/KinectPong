from pygame.locals import *
from threading import Thread
from settings import *
import numpy
import copy
import random
import ode

from basicGUI import *

from functions import *
import ctypes

import cProfile, pstats, StringIO



class ball():
    
    def __init__(self,x,y,vx,vy,width,height,color=(255,0,0,255)):
        self.pos = numpy.array([x,y]) #center
        self.speed = numpy.array([vx,vy]) #speed is in pixels per second
        self.original_speed = copy.copy(self.speed)
        self.size = numpy.array([width,height])
        
        self.color = color
        self.ghostColor = (color[0],color[1],color[2],20)
       
        self.itemID = str(random.randint(0,100000000))
        self.previous_update = pygame.time.get_ticks()
       
        self.current_ticks = 0
        self.pos_array = []
        
    def startTicks(self):
        self.current_ticks = pygame.time.get_ticks()
        self.original_speed = copy.copy(self.speed)
        
    def endTicks(self):
        self.pos_array.append(self.pos)
        self.previous_update = self.current_ticks
        
    def update(self,collision_objects,dynamic_objects,dt):
        pos = self.move(dt)
        collided = self.checkDynamicCollisions(collision_objects,dynamic_objects,pos,dt)
        collided = self.checkCollisions(collision_objects,pos)
        self.pos = self.move(dt)
        
    def move(self,multiplier=1):        
        ticks = multiplier * 0.001 * (self.current_ticks - self.previous_update)
        return self.pos + ticks * self.speed        
    
    def moveX(self,multiplier=1):        
        ticks = multiplier * 0.001 * (self.current_ticks - self.previous_update)
        return self.pos[0] + ticks * self.speed[0]  
    
    def moveY(self,multiplier=1):        
        ticks = multiplier * 0.001 * (self.current_ticks - self.previous_update)
        return self.pos[1] + ticks * self.speed[1]  
    
    def checkCollisions(self,collision_objects,pos):
        hw = self.size[0] * 0.5
        hh = self.size[1] * 0.5
        
        collided = False
        for obj in collision_objects:
            if obj[0][0] <= pos[0] + hw <= obj[1][0] and obj[0][1] <= pos[1] <= obj[1][1]:
#                 print "collision on right"
                self.speed[0] *= -1
                collided = True
            elif obj[0][0] <= pos[0] - hw <= obj[1][0] and obj[0][1] <= pos[1] <= obj[1][1]:
#                 print "collision on left"
                self.speed[0] *= -1
                collided = True
            elif obj[0][0] <= pos[0] <= obj[1][0] and obj[0][1] <= pos[1] + hh <= obj[1][1]:
#                 print "collision on bottom"
                self.speed[1] *= -1
                collided = True
            elif obj[0][0] <= pos[0] <= obj[1][0] and obj[0][1] <= pos[1] - hh <= obj[1][1]:
#                 print "collision on top"
                self.speed[1] *= -1
                collided = True
            elif obj[0][0] <= pos[0] + hw <= obj[1][0] and obj[0][1] <= pos[1] + hh <= obj[1][1]:
#                 print "collision on lower right corner"
                self.speed *= -1
                collided = True
            elif obj[0][0] <= pos[0] + hw <= obj[1][0] and obj[0][1] <= pos[1] - hh <= obj[1][1]:
#                 print "collision on upper right corner"
                self.speed *= -1
                collided = True
            elif obj[0][0] <= pos[0] - hw <= obj[1][0] and obj[0][1] <= pos[1] + hh <= obj[1][1]:
#                 print "collision on lower left corner"
                self.speed *= -1
                collided = True
            elif obj[0][0] <= pos[0] - hw <= obj[1][0] and obj[0][1] <= pos[1] - hh <= obj[1][1]:
#                 print "collision on upper left corner"
                self.speed *= -1
                collided = True
        
        return collided

    def checkDynamicCollisions(self,collision_objects,dynamic_objects,pos,dt):
        hw = self.size[0] * 0.5
        hh = self.size[1] * 0.5
        collided = False
        for obj in dynamic_objects:
            if obj.itemID != self.itemID:
                obj_pos = obj.move(dt)
                pos0 = obj_pos - 0.5 * obj.size
                pos1 = obj_pos + 0.5 * obj.size
                if pos0[0] <= pos[0] + hw <= pos1[0] and pos0[1] <= pos[1] <= pos1[1]:
#                     print "DYN collision on right " + self.itemID
                    self.speed[0] = obj.original_speed[0]
                    obj.speed[0] = self.original_speed[0]
                    collided = True
                elif pos0[0] <= pos[0] - hw <= pos1[0] and pos0[1] <= pos[1] <= pos1[1]:
#                     print "DYNcollision on left" + self.itemID
                    self.speed[0] = obj.original_speed[0]
                    obj.speed[0] = self.original_speed[0]
                    collided = True
                elif pos0[0] <= pos[0] <= pos1[0] and pos0[1] <= pos[1] + hh <= pos1[1]:
#                     print "DYNcollision on bottom" + self.itemID
                    self.speed[1] = obj.original_speed[1]
                    obj.speed[1] = self.original_speed[1]
                    collided = True
                elif pos0[0] <= pos[0] <= pos1[0] and pos0[1] <= pos[1] - hh <= pos1[1]:
#                     print "DYNcollision on top" + self.itemID
                    self.speed[1] = obj.original_speed[1]
                    obj.speed[1] = self.original_speed[1]
                    collided = True
                elif pos0[0] <= pos[0] + hw <= pos1[0] and pos0[1] <= pos[1] + hh <= pos1[1]:
#                     print "DYNcollision on lower right corner" + self.itemID
                    self.speed = obj.original_speed
                    obj.speed = self.original_speed
                    collided = True
                elif pos0[0] <= pos[0] + hw <= pos1[0] and pos0[1] <= pos[1] - hh <= pos1[1]:
#                     print "DYNcollision on upper right corner" + self.itemID
                    self.speed = obj.original_speed
                    obj.speed = self.original_speed
                    collided = True
                elif pos0[0] <= pos[0] - hw <= pos1[0] and pos0[1] <= pos[1] + hh <= pos1[1]:
#                     print "DYNcollision on lower left corner" + self.itemID
                    self.speed = obj.original_speed
                    obj.speed = self.original_speed
                    collided = True
                elif pos0[0] <= pos[0] - hw <= pos1[0] and pos0[1] <= pos[1] - hh <= pos1[1]:
#                     print "DYNcollision on upper left corner" + self.itemID
                    self.speed = obj.original_speed
                    obj.speed = self.original_speed
                    collided = True
        
        return collided

    def draw(self,surface):
        surface.blit(getBlock(self.size[0],self.size[1],self.color),self.pos - 0.5*self.size)
        
    def drawGhosting(self,surface,ghosts=10):
        if len(self.pos_array) > ghosts:
            self.pos_array.pop(0)
        for i,pos in enumerate(reversed(self.pos_array)):
            surface.blit(getBlock(self.size[0],self.size[1],self.ghostColor),(pos-0.5*self.size))

class game(basicGUI):
    
    def initGUI(self):
        super(game,self).initGUI()
    
    def run(self):
        self.running = True
        
        pygame.event.set_blocked(MOUSEMOTION)
        
        self.system_images_loaded = True
        
        
        self.buildWorld()
        
        # Do the simulation...
        total_time = 0.0
        dt = 0.04
        
        
        contactgroup = ode.JointGroup()
        
        while self.running:
            t0 = time.time() #@UnusedVariable
            self.screenspace = {}
            if self.running:                    
                    self.screen.fill((0,0,0))
                    substeps = 4      
                    for i in range(substeps):
                        self.space.collide((self.world, contactgroup), self.near_callback)
                        self.world.step(dt/substeps)
                        self.force2D()
                        self.disableRotation()
                        self.drawBodies()
                        contactgroup.empty()
                        
                    
                    pygame.time.wait(5) #saves cpu time
                    
                    frametime = time.time() - t0
                    self.writetext(self.refreshrate_deck(frametime) + " Hz",3,self.x - 70,3,False,False,color=(255,0,0))
                    
                    pygame.display.flip()#refresh the screen
                    
                    #this checks the events of the program
                    self.checkEvents()
                    
        pygame.quit()
        
    def mouseClicked(self,x,y):
        xsize = random.randint(10,100)
        size = (xsize,xsize,xsize)
        self.addBox((x,self.y - y,0),size)
        self.dynamic_bodies[-1]
        self.dynamic_bodies[-1].addForce((random.randint(-10000,10000),random.randint(-10000,10000),0))
    
    def buildWorld(self):
        # Create a world object
        self.space = ode.Space()
        self.world = ode.World()
        self.world.setGravity( (0,0,0) )
        self.world.setERP(0.8)
        self.world.setCFM(1e-8)
        
        self.world.setLinearDamping(0.0) #friction for linear movements
#         self.world.setAngularDamping(0.001) #friction for angular movement
        
        self.dynamic_bodies = []
        self.collision_bodies = []
        
        #positions are of center of mass positions (center of shape)
        
        #floor
        self.addBox((self.x/2,10,0),(800,10,10),dynamic=False)
        self.addBox((self.x/2,self.y - 10,0),(800,10,10),dynamic=False)
        self.addBox((10,self.y/2,0),(10,550,10),dynamic=False)
        self.addBox((790,self.y/2,0),(10,550,10),dynamic=False)
        

    def addBox(self,pos,size,mass=1.0,density=2500.0,dynamic=True):
        self.collision_bodies.append(ode.GeomBox(self.space,size))
        self.collision_bodies[-1].shape = 'box'
        self.collision_bodies[-1].draw_params = size
        self.collision_bodies[-1].setPosition(pos)

        if dynamic:
            self.dynamic_bodies.append(ode.Body(self.world))
            M = ode.Mass()
            M.setBox(density,  size[0],size[1],size[2])
            M.mass = mass
            self.dynamic_bodies[-1].setMass(M)
            
            self.dynamic_bodies[-1].shape = 'box'
            self.dynamic_bodies[-1].draw_params = size
            self.dynamic_bodies[-1].setPosition(pos)
            self.dynamic_bodies[-1].setFiniteRotationMode(0)
            
            self.collision_bodies[-1].setBody(self.dynamic_bodies[-1])
            
    def force2D(self):
        for body in self.collision_bodies:
            x,y,z = body.getPosition()
            body.setPosition((x,y,0))
        
        for body in self.dynamic_bodies:
            x,y,z = body.getPosition()
            body.setPosition((x,y,0))

            
            
    def disableRotation(self,method=2):
        if method == 1:
            #method 1: remove x-y axis rotation
            for body in self.collision_bodies + self.dynamic_bodies:
                q0,q1,q2,q3 = body.getQuaternion()
                z_angle = math.atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2 + q3*q3))
                body.setRotation((math.cos(z_angle),-1*math.sin(z_angle),0,math.sin(z_angle),math.cos(z_angle),0,0,0,1))
        
        if method == 2:
            #method 2: convert rotation energy into kinetic to perserve energy in system
            for body in self.dynamic_bodies:
                x,y,z = body.getAngularVel()
                angular_energy = math.pow(x,2) + math.pow(y,2) + math.pow(z,2)
                
                x,y,z = body.getLinearVel()
                kinetic_energy = math.pow(x,2) + math.pow(y,2) + math.pow(z,2)
                
                ratio = (1 + (angular_energy/kinetic_energy))
                
                body.setLinearVel((x*ratio,y*ratio,0))
                body.setAngularVel((0,0,0))
                
                body.setQuaternion((1,0,0,0))
                
                
                
    def drawBodies(self):
        for body in self.collision_bodies:
            x,y,z = body.getPosition()
            q0,q1,q2,q3 = body.getQuaternion()
            z_angle = 180*math.atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2 + q3*q3))/math.pi
            shape_params = body.draw_params
            if body.shape == 'box':
                box = getBox(shape_params[0],shape_params[1],(255,0,0,50))
                rotated_box = pygame.transform.rotate(box,z_angle)
                self.screen.blit(rotated_box,(x-0.5*rotated_box.get_width(),self.y-y-0.5*rotated_box.get_height()))
                
    def rot_center(self,image, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        return rot_image
   
    def near_callback(self,args, g0, g1):
        contacts = ode.collide(g0, g1)
        world, contactgroup = args
        for c in contacts:
            c.setBounce(1) # bounciness --> 1 = elastic collisions
            c.setMu(0)
            j = ode.ContactJoint(world, contactgroup, c)
            j.attach(g0.getBody(), g1.getBody())  
        
if __name__ == '__main__':
#     pr = cProfile.Profile()
#     pr.enable()

    a = game()
    a.initGUI()
    a.run()
    
#     pr.disable()
#     s = StringIO.StringIO()
#     sortby = 'cumulative'
#     ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#     ps.print_stats()
#     print s.getvalue()