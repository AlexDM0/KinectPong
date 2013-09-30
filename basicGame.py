from pygame.locals import *
from threading import Thread
from settings import *
import numpy,ctypes
import copy
import random

from functions import *
import ctypes

# import cProfile, pstats, StringIO

from basicGUI import *

class simulation():
    
    def __init__(self,dynamic_objects,static_objects,control_objects,special_objects,dt,substeps,bounciness=1.0,linear_damping=0.0,max_velocity = 1000):
        self.dynamic_objects = dynamic_objects
        self.static_objects = static_objects
        self.control_objects = control_objects
        self.special_objects = special_objects
        self.dt = dt
        self.substeps = substeps
        self.bounciness = bounciness
        self.linear_damping = linear_damping
        self.max_velocity = max_velocity
    
    def run(self):
#         libc = numpy.ctypeslib.load_library('libcollision_detection.so',"../../../../workspace/collision_detection/Release")\
        libc = numpy.ctypeslib.load_library('libcollision_detection.so',"./")
        
        cFunction = libc.collision_detection
        
        cFunction.argtypes = [
                              ctypes.c_int,   # amount_of_dynamic_objects 
                              ctypes.c_int,   # amount_of_static_objects         
                              ctypes.c_int,   # amount of special objects
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous,writeable'),       # double* dynamic_positions
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous,writeable'),       # double* dynamic_velocities
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous'),                 # double* dynamic_sizes
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous,writeable'),       # double* static_positions
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous,writeable'),       # double* static_velocities
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous'),                 # double* static_sizes
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous'),                 # double* special_positions
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('f8'),flags='aligned,contiguous'),                 # double* special_sizes
                              numpy.ctypeslib.ndpointer(dtype=numpy.dtype('int32'),flags='aligned,contiguous,writeable'),      # int* static_sizes
                              ctypes.c_double, # bounciness
                              ctypes.c_double, # linear_damping
                              ctypes.c_double, # double dt
                              ctypes.c_int # substeps
                              ]
        cFunction.restype = None
        
        amount_of_dynamic_obj = len(self.dynamic_objects)
        amount_of_static_obj  = len(self.static_objects)
        amount_of_special_obj  = len(self.special_objects)
        
        for obj in self.control_objects:
            if obj.target_pos[0] != -1:
                obj.vel[0] = (obj.target_pos[0] - obj.pos[0])/self.dt #dx dt
            if obj.target_pos[1] != -1:
                obj.vel[1] = (obj.target_pos[1] - obj.pos[1])/self.dt #dx dt
            obj.target_pos = [-1,-1]
                        
        dynamic_pos_array   = []
        dynamic_vel_array   = []
        dynamic_sizes_array = []
        for obj in self.dynamic_objects:
            dynamic_pos_array   += obj.pos
            dynamic_vel_array   += obj.vel
            dynamic_sizes_array += obj.size
            
        static_pos_array   = []
        static_vel_array   = []
        static_sizes_array = []
        for obj in self.static_objects:
            static_pos_array   += obj.pos
            static_vel_array   += obj.vel
            static_sizes_array += obj.size
            
        special_pos_array   = []
        special_sizes_array = []
        special_hit_array = []
        for obj in self.special_objects:
            special_pos_array   += obj.pos
            special_sizes_array += obj.size
            special_hit_array.append(-1)
                        
        requires_CAW = ['CONTIGUOUS', 'ALIGNED', 'WRITEABLE']
        requires_CA = ['CONTIGUOUS', 'ALIGNED']
        
        dtype_double = numpy.dtype('f8')
        dtype_int = numpy.dtype('int32')
        
        dynamic_positions = numpy.require(dynamic_pos_array, dtype_double, requires_CAW)
        dynamic_velocities = numpy.require(dynamic_vel_array, dtype_double, requires_CAW)
        dynamic_sizes = numpy.require(dynamic_sizes_array, dtype_double, requires_CA)
        
        static_positions = numpy.require(static_pos_array, dtype_double, requires_CAW)
        static_velocities = numpy.require(static_vel_array, dtype_double, requires_CAW)
        static_sizes = numpy.require(static_sizes_array, dtype_double, requires_CA)
        
        special_positions = numpy.require(special_pos_array, dtype_double, requires_CA)
        special_sizes = numpy.require(special_sizes_array, dtype_double, requires_CA)
        special_hits = numpy.require(special_hit_array, dtype_int, requires_CAW)
        
        cFunction(
                  amount_of_dynamic_obj,
                  amount_of_static_obj,
                  amount_of_special_obj,
                  dynamic_positions,
                  dynamic_velocities,
                  dynamic_sizes,
                  static_positions,
                  static_velocities,
                  static_sizes,
                  special_positions,
                  special_sizes,
                  special_hits,
                  self.bounciness,
                  self.linear_damping,
                  self.dt,
                  self.substeps
                  )   
        
        for i,obj in enumerate(self.dynamic_objects):
            obj.pos[0] = dynamic_positions[0 + 2*i]
            obj.pos[1] = dynamic_positions[1 + 2*i]
 
            obj.vel[0] = max(-1*self.max_velocity,min(self.max_velocity,dynamic_velocities[0 + 2*i]))
            obj.vel[1] = max(-1*self.max_velocity,min(self.max_velocity,dynamic_velocities[1 + 2*i]))
         
        for i,obj in enumerate(self.static_objects):
            obj.pos[0] = static_positions[0 + 2*i]
            obj.pos[1] = static_positions[1 + 2*i]
 
            obj.vel[0] = max(-1*self.max_velocity,min(self.max_velocity,static_velocities[0 + 2*i]))
            obj.vel[1] = max(-1*self.max_velocity,min(self.max_velocity,static_velocities[1 + 2*i]))
         
        for i,obj in enumerate(self.special_objects):
            obj.hit = special_hits[i]

class box():
    
    def __init__(self,width,height,(xpos,ypos),(xvel,yvel),dynamic,color=(255,0,0,255),hidden=False,image=''):
        self.pos = [xpos,ypos]      #center
        self.vel = [xvel,yvel]      #speed is in pixels per second
        self.size = [width,height]
        self.dynamic = dynamic
        
        self.image = image
        
        self.target_pos = [-1,-1]
        self.initial_pos = [xpos,ypos]
        
        self.hidden = hidden
        
        self.color = color
        
        self.user_id = "empty"
        self.user_assignment_time = 1000
       
        self.itemID = str(random.randint(0,100000000))
        self.pos_array = []
        self.ghosts = 10
        
        self.hit = -1
         
    def assignEvent(self,event_function,*default_arguments):
        self.event = event_function
        self.event_default_arguments = default_arguments
    
    def executeEvent(self,*args):
        arguments = self.event_default_arguments + args
        self.event(*arguments)

    def draw(self,surface):
        if self.image != '':
            surface.blit(self.image,(self.pos[0] - 0.5*self.size[0],self.pos[1] - 0.5*self.size[1]))
        else:
            surface.blit(getBox(self.size[0],self.size[1],self.color),(self.pos[0] - 0.5*self.size[0],self.pos[1] - 0.5*self.size[1]))
        if len(self.pos_array) > self.ghosts:
            self.pos_array.pop(0)
        self.pos_array.append([self.pos[0],self.pos[1]])
              
class basicGame(basicGUI):
    
    def initGUI(self):
        basicGUI.initGUI(self)
        
        self.player_id = "player"
    
    def loadSystemImages(self):
        self.system_images['background'] = pygame.image.load('system_resources/background.png').convert()
        self.system_images['left_batter'] = pygame.image.load('system_resources/left_batter.png').convert_alpha()
        self.system_images['right_batter'] = pygame.image.load('system_resources/right_batter.png').convert_alpha()
    
    def run(self):
        self.running = True
        pygame.event.set_blocked(MOUSEMOTION)
                
        substeps = 10
#         prev_tick = pygame.time.get_ticks()-5
        
        current_milli_time = lambda: int(round(time.time() * 1000))
        prev_tick = current_milli_time()-5
        
        
        self.mouseClicked(400,300,30,force=True) #ball
        
        self.previous_messages = 0
        
        while self.running:
            t0 = time.time()
            self.screenspace = {}
            self.screen.blit(self.system_images['background'],(0,0))
            try:
#                 tick = pygame.time.get_ticks()
#                 ticks = tick - prev_tick
#                 prev_tick = tick
                
                tick = current_milli_time()
                ticks = tick - prev_tick
                prev_tick = tick
#                 
#                 
                self.dt = ticks/1000.0
                
                self.clearPlayers()
                
                self.alternativeControls()
                self.checkPressedKeys()
                
                self.doNetworking()

                self.useAI()
                
                self.runSimulation(self.dt,substeps)
                
                self.drawObjects()
                self.drawInformation()
                self.checkSpecialEvents()
                
                time.sleep(0.01)
#                 pygame.time.wait(5) #saves cpu time
                
                frametime = time.time() - t0
                self.writetext(self.refreshrate_deck(frametime) + " Hz",3,self.x - 150,10,False,False,color=(255,255,255))
                
                pygame.display.flip()#refresh the screen
                
                #this checks the events of the program
                self.checkEvents()    
                
            except KeyboardInterrupt:
                print "cleanly handling keyboard interrupt"
                self.running = False 
                    
        self.shutNetworkingDown()
        pygame.quit()
    
    def alternativeControls(self):
        pass
    
    def shutNetworkingDown(self):
        pass
    
    def clearPlayers(self):
        threshold = 4 #seconds
        for obj in self.control_objects:
            if time.time() - obj.user_assignment_time > threshold: 
                obj.user_id = "empty"
                
    def doNetworking(self):
        pass
        
    def drawInformation(self):
        self.writetext("Scores:",4,self.x/2,20,centerx=True)
        spread = 100    
        if self.amount_of_players == 1:
            spread = 0    
        for i,score in enumerate(self.scores):
            self.writetext(str(score),3,self.x/2 - 0.5*spread + i*(spread/(self.amount_of_players-1)),50,centerx=True)
    
    def checkSpecialEvents(self):
        for obj in self.special_objects:
            if obj.hit != -1:
                obj.executeEvent(obj.hit)
            obj.hit = -1
            
    def scorePlayer(self,player_index,score,collision_object_index):
        self.scores[player_index] += score
        # assuming only dynamic objects hit special objects
        self.dynamic_objects.pop(collision_object_index)
        
        self.mouseClicked(400,300,30)
    
    def mouseClicked(self,x,y,obj_size=-1,color=(255,255,255,255),force=False):
        if obj_size == -1:
            xsize = random.randint(5,50)
        else:
            xsize = obj_size
            
        size = (xsize,xsize)
        self.addBox(size[0],size[1],(x,y),(random.randint(300,500) * ((2 * random.randint(0,1))-1),0),dynamic=True, color=color)
#         self.addBox(size[0],size[1],(x,y),(random.randint(300,500) * ((2 * random.randint(0,1))-1),random.randint(-300,300)),dynamic=True, color=color)
          
    def buildWorld(self):
        self.pressed_threshold = 0
        self.repeat_threshold = 0
        self.movement_speed = 5
        
        self.amount_of_players = 2
        
        self.dynamic_objects = [] # objects that bounce around and react to collisions
        self.static_objects  = [] # objects that are rigid (do not change on collision with other object)
        self.special_objects = [] # objects that fire events on collision
        self.control_objects = [] # objects controlled by a user
        
        self.scores = [0 for i in range(self.amount_of_players)]
        
        # the score zone
        self.addBox(100,self.y+2000,(-100,self.y/2),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,1,1)
        self.addBox(800,30,(-200,-20),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,1,1)
        self.addBox(800,30,(-200,self.y+20),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,1,1)
        
        self.addBox(100,self.y+2000,(900,self.y/2),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,0,1)
        self.addBox(800,30,(1000,-20),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,0,1)
        self.addBox(800,30,(1000,self.y+20),(0,0),dynamic=False,color=(0,255,0,255),special=True)
        self.special_objects[-1].assignEvent(self.scorePlayer,0,1)
        
        # the walls
        self.addBox(800,10,(self.x/2,5),(0,0),  color=(10,10,30,255),dynamic=False)  
        self.addBox(800,10,(self.x/2,595),(0,0),color=(10,10,30,255),dynamic=False)
#         self.addBox(10,580,(780,self.y/2),(0,0),dynamic=False)
        
        
        # the paddle
        self.addBox(10,110,(20,self.y/2),(0,0),dynamic=False,color=(255,0,0,255),control_object=True, image=self.system_images['left_batter'])
        
        self.addBox(10,110,(780,self.y/2),(0,0),dynamic=False,color=(255,0,0,255),control_object=True,image=self.system_images['right_batter'])
        
    def upArrowKeyPressed(self):
        control_index = self.assignUserToOpenControl(self.player_id + "_keyboard")
        if control_index != -1:
            self.control_objects[control_index].target_pos[1] = max(0.5*self.control_objects[control_index].size[1]+10,self.control_objects[control_index].pos[1] - self.movement_speed)
    
    def downArrowKeyPressed(self):
        control_index = self.assignUserToOpenControl(self.player_id + "_keyboard")
        if control_index != -1:
            self.control_objects[control_index].target_pos[1] = min(self.y-0.5*self.control_objects[control_index].size[1]-10,self.control_objects[control_index].pos[1] + self.movement_speed)
                 
    def assignUserToOpenControl(self,ID):
        user_assigned = False
        index = -1
        for i,obj in enumerate(self.control_objects):
            if obj.user_id == ID:
                self.assignUser(ID,i)
                user_assigned = True
                index = i
                break
        if not user_assigned:
            for i,obj in enumerate(self.control_objects):
                if obj.user_id == "empty":
                    self.assignUser(ID,i)
                    user_assigned = True
                    index = i
                    break
    
        return index
    
    def assignUser(self,ID,control_index):
        self.control_objects[control_index].user_id = ID
        self.control_objects[control_index].user_assignment_time = time.time()
    
    def drawObjects(self):
        for obj in  self.special_objects + self.dynamic_objects + self.static_objects:
            if not obj.hidden:
                obj.draw(self.screen)
              
    def addBox(self,width,height,(xpos,ypos),(xvel,yvel),dynamic=True,color=(20,20,50,255),control_object = False, special = False, hidden = False, image=''):
        if not special:
            if dynamic and not control_object:
                self.dynamic_objects.append(box(width,height,(xpos,ypos),(xvel,yvel),dynamic,color,hidden,image))
            else:
                if control_object:
                    self.control_objects.append(box(width,height,(xpos,ypos),(xvel,yvel),dynamic,color,hidden,image))
                    self.static_objects.append(self.control_objects[-1])
                else:
                    self.static_objects.append(box(width,height,(xpos,ypos),(xvel,yvel),dynamic,color,hidden,image))
        else:
            self.special_objects.append(box(width,height,(xpos,ypos),(xvel,yvel),False,color,hidden,image))
            
    def runSimulation(self,dt,substeps):
        a = simulation(self.dynamic_objects,self.static_objects,self.control_objects,self.special_objects,dt,substeps)
        a.run()
        
    def useAI(self):
        for obj in self.control_objects:
            if obj.user_id == "empty":
                min_distance = self.x
                min_distance_index = 0
                for i,dobj in enumerate(self.dynamic_objects):
                    if abs(dobj.pos[0] - obj.pos[0]) < min_distance:
                        min_distance = abs(dobj.pos[0] - obj.pos[0]) 
                        min_distance_index = i
                obj.vel[0] = (obj.initial_pos[0] - obj.pos[0])/self.dt #dx dt
                obj.vel[1] = (self.dynamic_objects[min_distance_index].pos[1] - obj.pos[1])/self.dt #dy dt    


        
if __name__ == '__main__':
    a = basicGame()
    a.initGUI()
    a.buildWorld()
    a.run()
