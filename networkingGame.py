from pygame.locals import *
from threading import Thread
from settings import *
import numpy,ctypes
import copy
import random

from functions import *
import ctypes
from basicGUI import basicGUI
from basicGame import basicGame
from networking_classes import *

class networkingGame(basicGame):
    
    def run(self):
        background = pygame.image.load('system_resources/connecting_background.png').convert()
        self.screen.blit(background,(0,0))
        pygame.display.flip()#refresh the screen
                
        self.initializeNetworking()
        
        basicGame.run(self)
            
    def initializeNetworking(self,dedicated_server = False):        
        self.dedicated_server = dedicated_server
        self.start_reconnect = False
#         self.networking = networking(5560,5565,5570,"http://www.avalondesigns.nl/ip_overlord")
        self.networking = networking(5560,5565,5570,"http://94.210.7.227:6900/php")
        self.networking.setup()
        self.assignUsers()
        self.keep_alive_time = time.time()
        
    def assignUsers(self):
        #server is player 1
        for i in range(self.amount_of_players):
            self.control_objects[i].user_id = "empty"

        if not self.dedicated_server:
            self.control_objects[0].user_id = self.player_id
    
    def drawInformation(self):
        basicGame.drawInformation(self)
        if self.networking.is_server:
            self.writetext("SERVER",5,self.x/2,100,True)
            self.writetext("Subscribed users: " + str(self.networking.me.subscribers),3,self.x/2,130,True)
        else:
            self.writetext("CLIENT",5,self.x/2,100,True)
                
    def doNetworking(self, timeout=1):
        # reporting to the online service that this user is still here
        if time.time() - self.keep_alive_time > 3:
            self.keep_alive_time = time.time()
            self.networking.keepAlive()
            
        if self.networking.is_server:
            self.networking.me.REQUEST_TIMEOUT = 1
            self.networking.me.checkForConnectingClients()
            self.handleClients()
            
            self.networking.me.REQUEST_TIMEOUT = timeout
            self.networking.me.listenToClients()
            self.processClientData()
            
            self.networking.me.sendData()
        else:
            self.player_id = self.networking.me.unit_id
            self.networking.me.REQUEST_TIMEOUT = 40
            if self.networking.me.enabled:
                if not self.networking.me.publisher_initialized:
                    self.networking.me.subscribeToServer()
                    self.networking.me.setupPublisher()
                else:
                    if self.start_reconnect:
                        self.networking.me.checkIfServerIsAlive()
                        self.start_reconnect = False
                    if not self.networking.me.connection_to_server_lost:
                        if not self.networking.me.registered_with_server:
                            self.networking.me.applyToServer()
                        else:
                            self.networking.me.data_to_send = self.createClientGameState()
                            self.networking.me.sendToServer()
                            self.networking.me.listenToServer()
                            self.loadGameState() 
                    else:
                        self.writetext("Connection to Server Lost.. Trying to Reconnect...",4,self.x/2,self.y/2 - 60,True)
                        self.start_reconnect = True
            else:
                self.networking.replaceServer()


    
    def handleClients(self):
        for data in self.networking.me.client_data:
            client_already_playing = False
            if len(data) == 4:
                for i,obj in enumerate(self.control_objects):
                    if data[0] in obj.user_id:
                        self.assignUser(data[3],i)
                        client_already_playing = True
                if not client_already_playing:
                    for i,obj in enumerate(self.control_objects):
                        if obj.user_id == "empty":
                            self.assignUser(data[0],i)
                            self.scores = [0 for i in range(self.amount_of_players)]
                            break
    
    def processClientData(self):
        for data in self.networking.me.client_data:
            if len(data) == 4:
                for obj in self.control_objects:
                    if data[0] in obj.user_id:
                        obj.target_pos[0] = float(data[1])
                        obj.target_pos[1] = float(data[2])
                        obj.user_id = data[3]
                        break
        self.networking.me.data_to_publish = self.createServerGameState()
        
    def createServerGameState(self):
        gameState = []
        gameState.append(str(self.dt))
        gameState.append(len(self.dynamic_objects))
        gameState.append(len(self.static_objects))
        
        for obj in self.dynamic_objects + self.static_objects:
            gameState += [obj.pos[0],obj.pos[1],obj.vel[0],obj.vel[1],obj.size[0],obj.size[1], obj.user_id]
            
        gameState = [str(i) for i in gameState]    
        return gameState
        
    def createClientGameState(self):
        clientGameState   = []
        for obj in self.control_objects:
            if self.networking.me.unit_id in obj.user_id:
                clientGameState += [obj.target_pos[0],obj.target_pos[1],obj.user_id]
        
        clientGameState = [str(i) for i in clientGameState]    
        return clientGameState
        
    def loadGameState(self):
        gamestate_iterator = 0
        if self.networking.me.server_data[0] != "ping":
            self.dt = float(self.networking.me.server_data[0])
            if (len(self.dynamic_objects)) < int(self.networking.me.server_data[1]):
                self.addBox(1, 1, (100, 100), (0, 0), True)
            if (len(self.static_objects)) < int(self.networking.me.server_data[2]):
                self.addBox(1, 1, (100, 100), (0, 0), False, False, False, False)
            
            for obj in self.dynamic_objects + self.static_objects:
                if self.player_id not in obj.user_id:
                    obj.pos[0]  = float(self.networking.me.server_data[3+gamestate_iterator*7])
                    obj.pos[1]  = float(self.networking.me.server_data[4+gamestate_iterator*7])
                    obj.vel[0]  = float(self.networking.me.server_data[5+gamestate_iterator*7])
                    obj.vel[1]  = float(self.networking.me.server_data[6+gamestate_iterator*7])
                    obj.size[0] = float(self.networking.me.server_data[7+gamestate_iterator*7])
                    obj.size[1] = float(self.networking.me.server_data[8+gamestate_iterator*7])
#                 else:
#                     print obj.pos
                obj.user_id = self.networking.me.server_data[9+gamestate_iterator*7]
                gamestate_iterator += 1
        
    def shutNetworkingDown(self):
        self.networking.me.closeAll()
        self.networking.close()
        
    def mouseClicked(self,x,y,obj_size=-1,color=(255,255,255,255),force=False):
        if self.networking.is_server or force:
            if obj_size == -1:
                xsize = random.randint(5,50)
            else:
                xsize = obj_size
                
            size = (xsize,xsize)
            self.addBox(size[0],size[1],(x,y),(random.randint(300,500) * ((2 * random.randint(0,1))-1),0),dynamic=True, color=color)
        
if __name__ == '__main__':
    
#     import cProfile, pstats, io
#     pr = cProfile.Profile()
#     pr.enable()
    
    a = networkingGame()
    a.initGUI()
    a.buildWorld()
    a.run()
    
#     pr.disable()
#     p = pstats.Stats(pr)
#     p.sort_stats('cumulative').print_stats(50)
#     p.sort_stats('time').print_stats(50)
#     p.sort_stats('calls').print_stats(50)
