from threading import Thread
from settings import *
import numpy,ctypes
import copy
import random

from functions import *
import ctypes
from networkingGame import networkingGame
from networking_classes import *

class game(networkingGame):
     
    def loadSystemImages(self):
        self.system_images['background'] = ''
        self.system_images['left_batter'] = ''
        self.system_images['right_batter'] = ''
        
    def initGUI(self,x=800,y=600):      
        self.x = x
        self.y = y
                  
        self.font = []
        self.frametimes_deck = []
        self.notification_center = []
        self.notification_time_start = 0
        
        self.system_images = {}
        
        self.system_images_loaded = False         
        self.showScreenSpace_on = False
        self.showCollisionSpace_on = False
        self.alignmentTools_on = False
        self.mouse_pressed_xy = [0,0]

        
        self.loadSystemImages()

        
        self.selected_item_id = ''
        self.selected_table = "none"
        self.time_clicked = 0
        
        self.shift_on,self.control_on,self.alt_on = False,False,False
        
        #initialization
        self.interface = ""
        self.menu_selection = ""
        self.category_field = ""
        
        # scrollbar
        self.last_scroll_time = 0
        self.max_scroll_distance = 0
        
        #key presses
        self.pressed_threshold = 0.4
        self.repeat_threshold = 0.1
        
        self.resetFields()
    
    def run(self):
        self.running = True                
        substeps = 10
        
        current_milli_time = lambda: int(round(time.time() * 1000))
        
        prev_tick = current_milli_time()-5
        
        self.mouseClicked(400,300,30) #ball
        
        self.roscore_running = False
        self.ROS_connections_initialized = False
        self.previous_messages = 0
        
        while self.running:
            
            t0 = time.time()
            self.screenspace = {}
            if self.running:
                try:
                    tick = current_milli_time()
                    ticks = tick - prev_tick
                    prev_tick = tick
                    
                    self.dt = ticks/1000.0
                    
                    self.clearPlayers()
                                
                    self.doNetworking()
                    
                    self.useAI()
                    
                    self.runSimulation(self.dt,substeps)
                    
                    self.checkSpecialEvents()
                    
                    pygame.time.wait(10) #saves cpu time
                    
                except KeyboardInterrupt:
                    print "cleanly handling keyboard interrupt"
                    self.running = False 
                    
        self.shutNetworkingDown()
    
    def initializeNetworking(self):        
        networkingGame.initializeNetworking(self, True)
                   
    def doNetworking(self):
        if time.time() - self.keep_alive_time > 3:
            self.keep_alive_time = time.time()
            self.networking.keepAlive()
            
        if self.networking.is_server:
            self.networking.me.REQUEST_TIMEOUT = 1
            self.networking.me.checkForConnectingClients()
            self.handleClients()
            
            self.networking.me.REQUEST_TIMEOUT = 0.1
            self.networking.me.listenToClients()
            self.processClientData()
            
            self.networking.me.sendData()
        
if __name__ == '__main__':
    
#     import cProfile, pstats, io
#     pr = cProfile.Profile()
#     pr.enable()
    
    a = game()
    a.initGUI()
    a.buildWorld()
    a.initializeNetworking()
    a.run()
    
#     pr.disable()
#     p = pstats.Stats(pr)
#     p.sort_stats('cumulative').print_stats(50)
#     p.sort_stats('time').print_stats(50)
#     p.sort_stats('calls').print_stats(50)
