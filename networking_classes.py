import time
import zmq, urllib2
import random,hashlib,socket
from functions import *
from threading import Thread

class onlineServiceCommunication(Thread):
    
    def __init__(self, address, message, function):
        self.address = address
        self.message = message
        self.function = function
        Thread.__init__(self)
        
    def run(self):
        if self.function == 'keepAlive':
            self.keepAlive()
        elif self.function == 'reportExit':
            self.reportExit()
        elif self.function == 'register':
            self.register()
        elif self.function == 'getServer':
            self.getServer()
    
    def keepAlive(self):
        service_connection = urllib2.urlopen(self.address + "/index.php?alive=" + self.message)
        service_connection.close()
        
    def reportExit(self, message=''):
        if message == "":
            message = self.message
        service_connection = urllib2.urlopen(self.address + "/index.php?quit=" + message)
        service_connection.close()
        
    def register(self):
        service_connection = urllib2.urlopen(self.address + "/index.php?ip=" + self.message)
        service_connection.close()

    def getServer(self):
        service_connection = urllib2.urlopen(self.address + "/index.php?getServer=1")
        server_ip = service_connection.read()
        service_connection.close()
        return server_ip

class networking(object):
    
    def __init__(self, server_pub_port, server_req_port, server_sub_port, service_address):
        self.context = zmq.Context()
        self.is_server = True
        self.service_address = service_address
        self.server_pub_port = str(server_pub_port)
        self.server_req_port = str(server_req_port)
        self.server_sub_port = str(server_sub_port)
        self.getIP()
        
        self.registerWithService()
        
    def registerWithService(self):
        self.service_connection = onlineServiceCommunication(self.service_address,self.own_ip, 'register')
        self.service_connection.register()
        print 'registered'       
        
        self.server_ip = self.service_connection.getServer()
        print 'server_ip' , self.server_ip, "own ip:", self.own_ip
        
    def replaceServer(self):
        self.service_connection.reportExit(self.server_ip)
        print "removing Server from Service"
        self.server_ip = self.service_connection.getServer()
        print 'server_ip' , self.server_ip, "own ip:", self.own_ip
        self.setup()
    
    def setupServer(self):
        print self.server_ip, self.own_ip
        if self.server_ip == self.own_ip: #you are server
            try:
                self.server = self.context.socket(zmq.PUB)
                self.server.setsockopt(zmq.HWM, 1)  
                self.server.bind("tcp://*:" + self.server_pub_port)
                print "no server found, switching to server mode"
                self.is_server = True
            except zmq.core.error.ZMQError:
                print "server already running, switching to compliant mode"
                self.is_server = False
        else: #is the server online?
            self.is_server = False
            print "I'm not server.. starting client mode."
            
    def getIP(self):
        print 'getting ips...'
        # getting global IP
        import urllib2
        self.global_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
        
        # getting local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.own_ip = self.global_ip + ":" + (s.getsockname()[0])
        self.local_ip = (s.getsockname()[0])
        s.close()
        
    def setup(self):
        self.setupServer()
        if self.is_server:
            self.me = server(self.server, self.server_req_port, self.server_sub_port, self.own_ip, self.service_address, self.context)
        else:
            self.me = client(self.server_pub_port, self.server_req_port, self.server_sub_port, self.server_ip, self.own_ip, self.service_address, self.context)
        self.me.setup()
        
    def init(self):
        self.me.init()
        self.close()
        
    def keepAlive(self, message=''):
        
        if message == '':
            message = self.own_ip
        print 'keepalive', message
        self.service_connection = onlineServiceCommunication(self.service_address,message, 'keepAlive')
        self.service_connection.start()
    
    def close(self):
#         self.service_connection.reportExit()
        self.context.destroy()
        print 'Closed process gracefully.'

class server(networking):
    
    def __init__(self, server, server_req_port, server_sub_port, own_ips, service_address, context):
        self.server = server
        
        self.own_ips = own_ips
        self.service_address = service_address
        self.server_req_port = str(server_req_port)
        self.server_sub_port = str(server_sub_port)
        
        self.context = context
        self.subscribers = 0
        self.req_poller = zmq.Poller()
        self.sub_poller = zmq.Poller()
        self.enabled = True
        self.clients = []
        
        self.unit_id = "server"
        
        self.last_keep_alive_message = time.time()
        
        self.CLIENT_TIMEOUT             = 1 #s
        self.CLIENT_RECONNECT_TIMEOUT   = 5 #s
        self.REQUEST_TIMEOUT            = 1 #ms
        self.RECONNECTION_ATTEMPTS      = 5 #times
        self.KEEP_ALIVE_FREQUENCY       = 1 #seconds
        
        self.data_to_publish = ['ping']
        self.client_data = []
        
    def initiateService(self):
        # Socket to receive signals
        self.connectionService = self.context.socket(zmq.REP)
        self.connectionService.bind('tcp://*:' + self.server_req_port)
        self.req_poller.register(self.connectionService, zmq.POLLIN)
        
        self.clientService = self.context.socket(zmq.SUB)
        self.clientService.bind("tcp://*:" + self.server_sub_port)
        self.clientService.setsockopt(zmq.SUBSCRIBE,"")
        self.sub_poller.register(self.clientService, zmq.POLLIN)
        
    def registerClient(self,clientID,client_index=-1):
        if client_index != -1:
            self.clients[client_index] = [clientID, time.time()]
        else:
            self.clients.append([clientID, time.time()])
   
    def isClientRegistered(self, clientID):
        for client_index, client in enumerate(self.clients):
            if clientID == client[0]:
                return client_index
        return False
    
    def setup(self):
        self.initiateService()
    
    def checkForConnectingClients(self):
        incoming_messages = dict(self.req_poller.poll(self.REQUEST_TIMEOUT))
        # this handles the communication with new clients
        if self.connectionService in incoming_messages and incoming_messages[self.connectionService] == zmq.POLLIN:
            request = self.connectionService.recv_multipart()
            if request[0] == 'ping':
                self.connectionService.send("Server is back online.")
            else:
                client_index = self.isClientRegistered(request[0])
                if client_index is not False:
                    print 'Client '+request[0]+' registration restored.'
                    self.connectionService.send("Restoring registration")
                    self.registerClient(request[0],client_index)
                else:
                    print 'Client '+request[0]+' registered.'
                    self.registerClient(request[0])
                    self.connectionService.send("Registered")
                    self.subscribers += 1
        else:
            pass
            #print 'no clients'
    
    def listenToClients(self):
        # once someone is subscribed, the server sends and receives communications
        if self.subscribers != 0:
            self.client_data = []
            clients_to_kill = []
            # ensuring the entire buffer is empty
            # even WITH HWM, it takes some time for the subscriber to report the queue back to the publisher
            # this means messages can stack. Usually 1 or 2 is enough, 10 to be safe.
            # messaging is very fast. This should not hurt performance IF THE TIMEOUT IS LOW
            for j in range(10):
                for i in range(self.subscribers):
                    incoming_messages = dict(self.sub_poller.poll(0.1)) #ms
                    #get reports from all clients
                    if self.clientService in incoming_messages and incoming_messages[self.clientService] == zmq.POLLIN:
                        client_talk = self.clientService.recv_multipart()     
#                         print j, client_talk
                        for client in self.clients:
                            if client_talk[0] == client[0]:
                                client[1] = time.time() 
                                self.client_data.append(client_talk)    
                
            # check if clients have times out
            for client in self.clients:
                if time.time() - client[1] > self.CLIENT_RECONNECT_TIMEOUT:
                    clients_to_kill.append(i)
                    print "Client [" + client[0] + "] is being disconnected."
                else:
                    if time.time() - client[1] > self.CLIENT_TIMEOUT:
                        print "Client [" + client[0] + "] is not responding.. " + str(siground(self.CLIENT_RECONNECT_TIMEOUT - (time.time() - client[1]),2)) + " seconds left to respond."
                
                            
            # because we reversed the list, we can pop from back to forth which is not changing the indices upstream
            for client_index in reversed(clients_to_kill):
                self.clients.pop(client_index)
                self.subscribers -= 1
    
    def sendData(self):
        self.server.send_multipart(self.data_to_publish)

    def init(self):
        while self.enabled:
            if time.time() - self.last_keep_alive_message > self.KEEP_ALIVE_FREQUENCY:
                self.keepAlive(self.own_ips)
                self.last_keep_alive_message = time.time()
            try:
                self.checkForConnectingClients()
                if self.subscribers != 0:
                    self.listenToClients()
                    self.sendData()
                time.sleep(0.01)
            except KeyboardInterrupt:
                print "cleanly handling keyboard interrupt"
                self.enabled = False
        
        #closing connection sockets
        self.closeAll()
        
    def closeAll(self):
        print "Shutting Down"
        self.clientService.setsockopt(zmq.LINGER, 0)
        self.clientService.close()
        self.sub_poller.unregister(self.clientService)
        
        self.connectionService.setsockopt(zmq.LINGER, 0)
        self.connectionService.close()
        self.req_poller.unregister(self.connectionService)
        
        self.server.setsockopt(zmq.LINGER, 0)
        self.server.close()  
        self.context.destroy()       
            
class client(networking):
    
    def __init__(self, server_pub_port, server_req_port, server_sub_port, server_ips, own_ips, service_address, context):
        self.context = context
        self.server_pub_port = str(server_pub_port)
        self.server_req_port = str(server_req_port)
        self.server_sub_port = str(server_sub_port)
        
        self.own_ips = own_ips
        self.service_address = service_address
        
        server_ip_array = server_ips.split(":")
        own_ip_array    = own_ips.split(":")
        
        if own_ip_array[0] == server_ip_array[0]: # both global ips are the same --> this is a LAN connection
            self.server_ip = server_ip_array[1]
            print "Server is on Local Area Network. Connecting..."
        else:
            self.server_ip = server_ip_array[0]
            print "Server is on the Internet. Connecting..."
                
        self.registered_with_server = False
        self.publisher_initialized = False
        
        self.connection_to_server_lost = False
        self.enabled = True
        self.unit_id = hashlib.md5(str(random.randint(0,10000000))).hexdigest()
        self.unit_id = str(random.randint(0,10000000))
        
        self.sub_poller = zmq.Poller()
        self.req_poller = zmq.Poller()
        
        self.last_server_message = time.time()
        self.last_keep_alive_message = time.time()
        
        self.REQUEST_TIMEOUT = 500 #ms
        self.RECONNECTION_ATTEMPTS = 5
        self.SERVER_TIMEOUT = 2 #seconds
        self.KEEP_ALIVE_FREQUENCY = 1 #seconds
        
        self.data_to_send = ['attention']
        self.serverData = []
        
    def subscribeToServer(self):
        self.listener = self.context.socket(zmq.SUB)
        self.listener.connect('tcp://' + self.server_ip + ':' + self.server_pub_port)
        self.listener.setsockopt(zmq.SUBSCRIBE,"")
        self.sub_poller.register(self.listener, zmq.POLLIN)
        
    def setupPublisher(self):
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.setsockopt(zmq.HWM, 1)  
        self.publisher.connect("tcp://" + self.server_ip + ":" + self.server_sub_port)
        self.publisher_initialized = True      
    
    def applyToServer(self):
        self.request = self.context.socket(zmq.REQ)
        self.request.setsockopt(zmq.HWM, 1) 
        self.request.connect('tcp://' + self.server_ip + ':' + self.server_req_port)    
        self.request.send_multipart([self.unit_id])
        reply = self.request.recv()
        self.request.setsockopt(zmq.LINGER, 0)
        self.request.close()
        self.registered_with_server = True
        
    def reapplyToServer(self):
        reconnected = False
        for i in range(self.RECONNECTION_ATTEMPTS):
            self.request = self.context.socket(zmq.REQ)
            self.request.connect('tcp://' + self.server_ip + ':' + self.server_req_port)
            self.req_poller.register(self.request)  
            self.request.send_multipart(["ping"])
            
            retry = True
            while retry:
                socks = dict(self.req_poller.poll(500))
                if socks.get(self.request) == zmq.POLLIN:
                    reply = self.request.recv()
                    reconnected = True
                    break
                else:
                    print 'Could not connect to server within ' + str(siground(500/1000.0,2)) + " seconds."
                    break
            
            self.request.setsockopt(zmq.LINGER, 0)
            self.request.close()
            self.req_poller.unregister(self.request)  
            
            if reconnected:
                break
            
        return reconnected
    
    def setup(self):
        self.subscribeToServer()
        self.setupPublisher()
        self.channels_closed = False
    
    def init(self):
        if self.publisher_initialized:
            while self.enabled:
                if time.time() - self.last_keep_alive_message > self.KEEP_ALIVE_FREQUENCY:
                    self.keepAlive(self.own_ips)
                    self.last_keep_alive_message = time.time()
                try:
                    if not self.connection_to_server_lost:
                        if not self.registered_with_server:
                            self.applyToServer()
                        else:
                            self.sendToServer()
                            self.listenToServer()
                    else:
                        self.checkIfServerIsAlive()
                except KeyboardInterrupt:
                    print "cleanly handling keyboard interrupt"
                    self.enabled = False
        self.closeAll()
        
    def closeAll(self):
        print "Shutting Down"
        if not self.channels_closed:
            self.publisher.setsockopt(zmq.LINGER, 0)
            self.publisher.close()
            self.listener.setsockopt(zmq.LINGER, 0)
            self.listener.close()
            self.sub_poller.unregister(self.listener)
        self.context.destroy()
    
    def sendToServer(self):
        data_to_send = [self.unit_id] + self.data_to_send
        self.publisher.send_multipart(data_to_send)
              
    def listenToServer(self):
        # stay connected until the server shuts down
        for i in range(10):
            socks = dict(self.sub_poller.poll(0.1)) 
            if socks.get(self.listener) == zmq.POLLIN:
                if self.listener in socks:
                    self.server_data = self.listener.recv_multipart()
                    self.last_server_message = time.time()
#                     print i, self.server_data
        if time.time()-self.last_server_message > self.SERVER_TIMEOUT:
            self.connection_to_server_lost = True
            print 'Connection with server lost. Trying to reconnect...'
            self.registered_with_server = False
            
    def checkIfServerIsAlive(self):
        self.listener.setsockopt(zmq.LINGER, 0)
        self.listener.close()
        self.sub_poller.unregister(self.listener)
        self.publisher.setsockopt(zmq.LINGER, 0)
        self.publisher.close()
        self.channels_closed = True
        
        reconnected = self.reapplyToServer()
        
        if not reconnected:
            self.enabled = False
            print "Cannot reconnect to server. Aborting..."
        else:
            self.connection_to_server_lost = False
            self.subscribeToServer()
            self.setupPublisher()
            self.channels_closed = False
            if not self.publisher_initialized:
                self.enabled = False
                self.connection_to_server_lost = False
                print "Cannot communicate with server. Aborting..."


if __name__ == '__main__':
    a = networking(5560,5565,5570,"http://www.avalondesigns.nl/ip_overlord")
    a.setup()
    a.init()
    
    
    
#     
# # 
# # getter = context.socket(zmq.PULL)
# # getter.connect("tcp://localhost:5561")
# # 
# # # Initialize poll set
# # poller = zmq.Poller()
# # poller.register(getter, zmq.POLLIN)
# while True:
#     if iAmServer:
#         ran = str(random.randint(1,1000))
#         publisher.send("test1 : test" + ran)
#         print "SEND__TO: " + "test1 : test" + ran + "]"
# #     
# #     socks = dict(poller.poll())
# #     
# #     if getter in socks and socks[getter] == zmq.POLLIN:
# #         message = getter.recv()
# #         print "RESPONSE: " + message
# 
#     time.sleep(0.1)
#     