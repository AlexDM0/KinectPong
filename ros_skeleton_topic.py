from ros_classes import *
from std_msgs.msg import Float32MultiArray,MultiArrayLayout,MultiArrayDimension


class topicBroadcaster(object):
    
    def __init__(self, channel_name='portaudio__in', topic='/skeleton_markers'):
        self.channel_name = channel_name
        
        self.roscore_running = False
        self.ROS_connections_initialized = False
        
        self.last_reported_datastream = 0
    
    def getKinectUsers(self):
        self.users = informationFlowThread("/skeleton_markers",visualization_msgs.msg.Marker,skeletonDataHandler) 
        self.users.run()
      
    def broadcast(self,DEBUG_DATA = False):
        if not self.roscore_running:
            try:
                rostopic._check_master()
                print "RosCore detected!"
                self.roscore_running = True
            except rostopic.ROSTopicIOException:
                print "Can't find RosCore.."
            
        if self.roscore_running:
            rospy.init_node("pySkeleton")
            if not self.ROS_connections_initialized:
                self.getKinectUsers()
                self.ROS_connections_initialized = True
        
        if self.ROS_connections_initialized:
            self.pub = rospy.Publisher(self.channel_name, Float32MultiArray)
            while not rospy.is_shutdown():
                if DEBUG_DATA:
                    data = [2.71,3.1415]
                    self.publishData(data)
                else:
                    if self.last_reported_datastream != self.users.amount_of_messages_received:
                        user_data = self.getUserData()
                        if len(user_data) > 0:
                            self.publishData(user_data)
                time.sleep(0.5)
                        
                
    def publishData(self,data):
        dimensions = []
        dimensions.append(MultiArrayDimension('users',1,len(data)))
        layout = MultiArrayLayout(dimensions,0)
        array = Float32MultiArray(layout,data)
        
        rospy.loginfo(data)
        self.pub.publish(array)
    
        self.last_reported_datasteam = self.users.amount_of_messages_received
    
    def getUserData(self):
        user_data = []
        if self.users.amount_of_messages_received > 0:
           for user in self.users.data.users:
               if user.isActive:
                   for point in user.points:
                       user_data += [point.y,point.z,point.x] #standard x,y,z axis.. those in ROS are weird..
                    
        return user_data
                   


if __name__ == '__main__':
    a = topicBroadcaster()
    a.broadcast(DEBUG_DATA=False)
    