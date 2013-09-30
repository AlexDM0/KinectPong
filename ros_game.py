from pygame.locals import *
from threading import Thread
from settings import *
import numpy,ctypes
import copy
import random


from ros_classes import *

from functions import *
import ctypes

from basicGUI import *
from networkingGame import networkingGame
# from basicGame import basicGame as networkingGame

class ROS_game(networkingGame):
    
    def initGUI(self):
        networkingGame.initGUI(self)
        self.roscore_running = False
        self.ROS_connections_initialized = False
    
    def alternativeControls(self):
        self.runROS()
        
    def drawInformation(self):
        networkingGame.drawInformation(self)
        
        if not self.roscore_running:
            self.writetext("RosCore is not running...",2,self.x/2,self.y/2,True,True)
    
    def shutNetworkingDown(self):
        pass
    
    def clearPlayers(self):
        threshold = 4 #seconds
        for obj in self.control_objects:
            if time.time() - obj.user_assignment_time > threshold: 
                obj.user_id = "empty"
                
    def startNetworking(self):
        pass
    
    def runROS(self):
        if not self.roscore_running:
            try:
                rostopic._check_master()
                print "RosCore detected!"
                self.roscore_running = True
            except rostopic.ROSTopicIOException:
                pass
                #print "Can't find RosCore.."
        else:
            rospy.init_node("py_gui")
            if not self.ROS_connections_initialized:
                self.getKinectUsers()
#                 self.getKinectRGB()
                self.ROS_connections_initialized = True
            else:
                self.useROS()
                
    def useROS(self):
        if self.users.amount_of_messages_received > 0:
            for kinectUser in self.users.data.users: 
                if kinectUser.isActive:
                    control_index = self.assignUserToOpenControl(self.player_id + "_player" + str(kinectUser.userIndex))
                    if control_index != -1:
                        self.controlUser(kinectUser,control_index)

    def controlUser(self,user,index):
        multiplier_x = 250
        multiplier_y = 1500
        
        initial_xpos = self.control_objects[index].initial_pos[0]
        initial_ypos = self.control_objects[index].initial_pos[1]
        upper_ybound = self.y-0.5*self.control_objects[index].size[1] # top
        lower_ybound = 0.5*self.control_objects[index].size[1] # bottom
        
        if index == 0: # use left hand
            target_x = min(initial_xpos+100  , max(initial_xpos-20   , initial_xpos + multiplier_x*((user.spine.x - user.l_hand.x))))
            target_y = min(upper_ybound     , max(lower_ybound      , initial_ypos + multiplier_y*((user.spine.z + user.hip.z)*0.5 - user.l_hand.z)))
        elif index == 1: # use right hand
            target_x = min(initial_xpos+20  , max(initial_xpos-100   , initial_xpos - multiplier_x*((user.spine.x - user.r_hand.x))))
            target_y = min(upper_ybound     , max(lower_ybound      , initial_ypos + multiplier_y*((user.spine.z + user.hip.z)*0.5 - user.r_hand.z)))
        
        self.control_objects[index].target_pos[0] = target_x
        self.control_objects[index].target_pos[1] = target_y
        
        user.projection = True
        user.scale_factor = 0.2
        if index == 0:
            user.center = 200,120
        else:
            user.center = 600,120
        user.getCenters()
        user.drawFull(self.screen,writetext_function=self.writetext)
        
                      
    def getKinectUsers(self):
        self.users = informationFlowThread("/skeleton_markers",visualization_msgs.msg.Marker,skeletonDataHandler) 
        self.users.run()
        
    def getKinectRGB(self):
        self.kinectRGB = informationFlowThread('/camera/rgb/image_color', sensor_msgs.msg.Image, cameraDataHandler)
        self.kinectRGB.run()



        
if __name__ == '__main__':
#     import cProfile, pstats, io
#     pr = cProfile.Profile()
#     pr.enable()
    
    a = ROS_game()
    a.initGUI()
    a.buildWorld()
    a.run()
    
#     pr.disable()
#     p = pstats.Stats(pr)
#     p.sort_stats('cumulative').print_stats(50)
#     p.sort_stats('time').print_stats(50)
#     p.sort_stats('calls').print_stats(50)
