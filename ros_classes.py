import pygame,os,sys,time,random
from pygame.locals import *
from threading import Thread
from functions import *
from basicGUI import *
import copy

PKG = 'py_gui' # this package name
import roslib; roslib.load_manifest(PKG)
import rospy
import rostopic
import std_msgs.msg
import sensor_msgs.msg
import visualization_msgs.msg
import rostopic

class skeletonDataHandler():
    
    def __init__(self,raw_data,previous_data):
        self.data = raw_data
        self.previous_data = previous_data
        self.amount_of_points = len(raw_data.points)
        self.amount_of_users = self.amount_of_points/15
        self.getUsers()
        
    def getUsers(self):
        self.users = []
        
        # identify the datapoints and check if the user is active
        for user in range(self.amount_of_users):
            self.users.append(skeleton(self.data.points,
                                      self.previous_data,
                                      user))
        # get the amount of users that are active
        self.active_users = 0
        for user in self.users:
            if user.isActive:
                self.active_users += 1
        
class skeleton():
    
    def __init__(self,points,previous_data,user):
        self.scale = [320,385]
        self.depth_multiplier = 0.7
        self.center = [320,235]
        self.scale_factor = 1.0
        #projection means the skeleton is only projected in a 2D space
        self.projection = False
        

        self.identifyPoints(points, user)
        
        if previous_data != []:
            previous_points = previous_data.points
            self.isActive = self.checkIfActive(points,
                                               previous_points,
                                               user)
        else:
            self.isActive = False
            
        
        self.userIndex = user
        
        self.userColors = (
                           (255,0,0,255),
                           (0,255,0,255),
                           (0,0,255,255),
                           (255,0,255,255),
                           (255,0,0,255),
                           (0,255,0,255),
                           (0,0,255,255),
                           (255,0,255,255),
                           (255,0,0,255),
                           (0,255,0,255),
                           (0,0,255,255),
                           (255,0,255,255)
                           ) 
        
    def identifyPoints(self, points, user):
        # this points array is expected to have 15 entrees
        user_offset = 15*user
        self.head       = points[0 +user_offset]
        self.spine      = points[1 +user_offset]
        self.hip        = points[2 +user_offset]
        
        self.r_shoulder = points[3 +user_offset]
        self.r_elbow    = points[4 +user_offset]
        self.r_hand     = points[5 +user_offset]

        self.l_shoulder = points[6 +user_offset]
        self.l_elbow    = points[7 +user_offset]
        self.l_hand     = points[8 +user_offset]
        
        self.r_hip      = points[9 +user_offset]
        self.r_knee     = points[10+user_offset]
        self.r_foot     = points[11+user_offset]
        
        self.l_hip      = points[12+user_offset]
        self.l_knee     = points[13+user_offset]
        self.l_foot     = points[14+user_offset]
        
        self.points = points[user_offset:user_offset+15]
        
    def checkIfActive(self, points, previous_points, user, threshold=5):
        active = False
        if (user+1)*15-1 < len(previous_points):
            important_points = [0,1,2,5,8,11,14] # head hands feet center
            user_offset = user*15
            
            moving_points = 0
            for important_point in important_points:
                if points[important_point + user_offset].y != previous_points[important_point + user_offset].y:
                    moving_points += 1
                    
            self.active_points = moving_points
            if moving_points > (threshold-1):
#                 print "moving points", moving_points, "threshold", threshold
                active = True
            else:
                active = False
        else:   
            active = False
            
        if active:
            tmp_scale_factor = copy.copy(self.scale_factor)
            self.scale_factor = 1
            inside_bounds = 0
            for i,point in enumerate(self.points):
                if 1 < self.depthToCam(point,'x') < 639:
                    inside_bounds += 1
                if 1 < self.depthToCam(point,'y') < 479:
                    inside_bounds += 1
            
            if 30 - inside_bounds > 5:
                active = False
#             else:
#                 print "bounds", inside_bounds
            self.scale_factor = tmp_scale_factor
        return active
        
    def draw(self, surface, force=False, debug=False, writetext_function=False, white=False):
        # draws a skeleton
        if white:
            block = getBox(5,5,(255,255,255,255))
        else:
            block = getBox(5,5,self.userColors[self.userIndex])
        
        if self.isActive or force:
            for i,point in enumerate(self.points):
                if debug:
                    writetext_function(str(i),5,self.depthToCam(point,'x',-5),self.depthToCam(point,'y',-10))
                surface.blit(block,(self.depthToCam(point,'x'),self.depthToCam(point,'y')))
     
    def getCenters(self):
        self.head_center =   (self.depthToCam(self.head,'x')     ,self.depthToCam(self.head,'y'))
        self.spine_center =  (self.depthToCam(self.spine,'x')    ,self.depthToCam(self.spine,'y'))
        self.hip_center =    (self.depthToCam(self.hip,'x')      ,self.depthToCam(self.hip,'y'))
        
        self.r_shoulder_center = (self.depthToCam(self.r_shoulder,'x'),self.depthToCam(self.r_shoulder,'y'))
        self.r_elbow_center = (self.depthToCam(self.r_elbow,'x')  ,self.depthToCam(self.r_elbow,'y'))
        self.r_hand_center =  (self.depthToCam(self.r_hand,'x')   ,self.depthToCam(self.r_hand,'y'))
        
        self.l_shoulder_center = (self.depthToCam(self.l_shoulder,'x'),self.depthToCam(self.l_shoulder,'y'))
        self.l_elbow_center = (self.depthToCam(self.l_elbow,'x')  ,self.depthToCam(self.l_elbow,'y'))
        self.l_hand_center =  (self.depthToCam(self.l_hand,'x')   ,self.depthToCam(self.l_hand,'y'))
        
        self.r_hip_center = (self.depthToCam(self.r_hip,'x'),self.depthToCam(self.r_hip,'y'))
        self.r_knee_center = (self.depthToCam(self.r_knee,'x')  ,self.depthToCam(self.r_knee,'y'))
        self.r_foot_center =  (self.depthToCam(self.r_foot,'x')   ,self.depthToCam(self.r_foot,'y'))
        
        self.l_hip_center = (self.depthToCam(self.l_hip,'x'),self.depthToCam(self.l_hip,'y'))
        self.l_knee_center = (self.depthToCam(self.l_knee,'x')  ,self.depthToCam(self.l_knee,'y'))
        self.l_foot_center =  (self.depthToCam(self.l_foot,'x')   ,self.depthToCam(self.l_foot,'y'))
        
    def drawFull(self, surface, force=False, debug=False, writetext_function=False):
        # draws a pretty skeleton
        if self.isActive or force:
            pygame.draw.lines(surface, self.userColors[self.userIndex], False, [
                                                                                (self.head_center[0],self.head_center[1]),
                                                                                ([self.spine_center[0],self.spine_center[1]]),
                                                                                ([self.hip_center[0],self.hip_center[1]]),
                                                                                ([self.r_hip_center[0],self.r_hip_center[1]]),
                                                                                ([self.r_knee_center[0],self.r_knee_center[1]]),
                                                                                ([self.r_foot_center[0],self.r_foot_center[1]])
                                                                                ]
                                                                                ,5)
            pygame.draw.lines(surface, self.userColors[self.userIndex], False, [
                                                                                ([self.hip_center[0],self.hip_center[1]]),
                                                                                ([self.l_hip_center[0],self.l_hip_center[1]]),
                                                                                ([self.l_knee_center[0],self.l_knee_center[1]]),
                                                                                ([self.l_foot_center[0],self.l_foot_center[1]])
                                                                                ]
                                                                                ,5)
            
            pygame.draw.lines(surface, self.userColors[self.userIndex], False, [
                                                                                ([self.l_hand_center[0],self.l_hand_center[1]]),
                                                                                ([self.l_elbow_center[0],self.l_elbow_center[1]]),
                                                                                ([self.l_shoulder_center[0],self.l_shoulder_center[1]]),
                                                                                ([self.spine_center[0],self.spine_center[1]]),
                                                                                ([self.r_shoulder_center[0],self.r_shoulder_center[1]]),
                                                                                ([self.r_elbow_center[0],self.r_elbow_center[1]]),
                                                                                ([self.r_hand_center[0],self.r_hand_center[1]])
                                                                                ]
                                                                                ,5)
            
            #head
            pygame.draw.ellipse(surface, 
                                self.userColors[self.userIndex],
                                [
                                 self.head_center[0]-0.5*self.scale_factor*50,
                                 self.head_center[1]-0.5*self.scale_factor*80,
                                 self.scale_factor*50,
                                 self.scale_factor*80
                                ], 0)
            #hands
            pygame.draw.ellipse(surface,
                                 self.userColors[self.userIndex],
                                 [
                                  self.r_hand_center[0]-0.5*self.scale_factor*50,
                                  self.r_hand_center[1]-0.5*self.scale_factor*30,
                                  self.scale_factor*50,
                                  self.scale_factor*30
                                 ], 0)
            pygame.draw.ellipse(surface,
                                 self.userColors[self.userIndex],
                                 [
                                  self.l_hand_center[0]-0.5*self.scale_factor*50,
                                  self.l_hand_center[1]-0.5*self.scale_factor*30,
                                  self.scale_factor*50,
                                  self.scale_factor*30
                                 ], 0)
            #feet 
            pygame.draw.ellipse(surface,
                                 self.userColors[self.userIndex],
                                 [
                                  self.r_foot_center[0]-0.5*self.scale_factor*70,
                                  self.r_foot_center[1]-0.5*self.scale_factor*30,
                                  self.scale_factor*70,
                                  self.scale_factor*30
                                 ], 0)
            pygame.draw.ellipse(surface,
                                 self.userColors[self.userIndex],
                                 [
                                  self.l_foot_center[0]-0.5*self.scale_factor*70,
                                  self.l_foot_center[1]-0.5*self.scale_factor*30,
                                  self.scale_factor*70,
                                  self.scale_factor*30
                                 ], 0)
                  
    def depthToCam(self,point,axis,offset=0):
        if not self.projection:
            if axis == 'x':
                return max(0,min(640,self.center[0] + (self.scale_factor*self.scale[0]*point.y)/(self.depth_multiplier*point.x)))
            elif axis == 'y':
                return max(0,min(480,self.center[1] - (self.scale_factor*self.scale[1]*point.z)/(self.depth_multiplier*point.x)))
        else:
            if axis == 'x':
                return max(0,min(640,self.center[0] + (self.scale_factor*self.scale[0]*point.y)))
            elif axis == 'y':
                return max(0,min(480,self.center[1] - (self.scale_factor*self.scale[1]*point.z)))
                          
class cameraDataHandler():
    
    def __init__(self,data,previous_data):
        self.data = data
        self.image = data.data
        self.width = data.width
        self.height = data.height
        
    def showImage(self,surface,(x,y)):
        surface.blit(pygame.image.fromstring(self.image[::-1],(self.width,self.height),'RGB',True),(0,0))
        
    def getImage(self):
        return pygame.image.fromstring(self.image[::-1],(self.width,self.height),'RGB',True)

class informationFlowThread(Thread):
    
    def __init__(self,topic,data_type,class_wrapper=""):
        self.topic = topic
        self.type = data_type
        self.data = []
        self.old_data = []
        self.class_wrapper = class_wrapper
        self.amount_of_messages_received = 0
        self.runThread = True
        Thread.__init__(self)
    
    def run(self):
        rospy.Subscriber(self.topic, self.type, self.callback)
        
    def callback(self,data):
        if self.class_wrapper != "":
            self.data = self.class_wrapper(data,self.old_data)
        else:
            self.data = data
        self.old_data = data
        self.amount_of_messages_received += 1
                 
class gui(basicGUI):
    
    def __init__(self):
        pass

    def getKinectUsers(self):
        self.users = informationFlowThread("/skeleton_markers",visualization_msgs.msg.Marker,skeletonDataHandler) 
        self.users.run()
        
    def getKinectRGB(self):
        self.kinectRGB = informationFlowThread('/camera/rgb/image_color', sensor_msgs.msg.Image, cameraDataHandler)
        self.kinectRGB.run()
    
    def run(self):
        self.running = True
        showScreenSpace_on = False
        
        #for refreshrate
        t_start = time.time() #@UnusedVariable
        pygame.event.set_blocked(MOUSEMOTION)
        start_time = time.time() #@UnusedVariable

        self.ROS_connections_initialized = False
        self.roscore_running = False
        while self.running:
            t0 = time.time() #@UnusedVariable
            self.screenspace = {}
            if self.running:
                self.screen.fill((255,255,255))
                
                self.checkROS()
                          
                pygame.time.wait(15) #saves cpu time
                
                #=========================== REFRESH RATE ====================================
                frametime = time.time() - t0
                self.writetext(self.refreshrate_deck(frametime) + " Hz",3,self.x - 70,3,False,False,color=(255,0,0))
                #=============================================================================
                
                pygame.display.flip()#refresh the screen
                
                #this checks the events of the program
                self.checkEvents()
        pygame.quit()
    
    def checkROS(self):
        if not self.roscore_running:
           try:
               rostopic._check_master()
               print "RosCore detected!"
               self.roscore_running = True
           except rostopic.ROSTopicIOException:
               print "Can't find RosCore.."
               self.writetext("Cannot connect to RosCore",5,50,50)
               pygame.display.flip()#refresh the screen
               time.sleep(0.5)
        else:
           if not self.ROS_connections_initialized:
               rospy.init_node("py_gui")
               self.getKinectUsers()
               self.getKinectRGB()
               self.ROS_connections_initialized = True
           
           self.writetext("RosCore Found. Loading camera image...",5,50,150)
           if self.kinectRGB.amount_of_messages_received > 0:
               self.kinectRGB.data.showImage(self.screen,(0,0))

           if self.users.amount_of_messages_received > 0:
               self.writetext('markers received: ' + str(self.users.amount_of_messages_received),3,10,10)
               self.writetext('points: ' + str(self.users.data.amount_of_points),3,10,30)
               self.writetext('active users: ' + str(self.users.data.active_users),3,10,50)
                
                
               for user in self.users.data.users:
                   user.getCenters()
                   user.drawFull(self.screen,debug=True,writetext_function=self.writetext)
                   user.draw(self.screen,writetext_function=self.writetext, white=True)
        
if __name__ == '__main__':
    
#     import cProfile, pstats, io
#     pr = cProfile.Profile()
#     pr.enable()

    a = gui()
    a.initGUI(640,480)
    a.run()
    
#     pr.disable()
#     p = pstats.Stats(pr)
#     p.sort_stats('cumulative').print_stats(50)
#     p.sort_stats('time').print_stats(50)
#     p.sort_stats('calls').print_stats(50)
