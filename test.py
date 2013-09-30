#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray,MultiArrayLayout,MultiArrayDimension

import numpy as np


def talker():
    pub = rospy.Publisher('portroschannel', Float32MultiArray)
    rospy.init_node('talker')
    data = [2.3,5.1,63,345]
    dimensions = []
    dimensions.append(MultiArrayDimension('test',2,4))
    dimensions.append(MultiArrayDimension('banana',2,2))
    layout = MultiArrayLayout(dimensions,0)
    print layout.dim
    array = Float32MultiArray(layout,data)
#     layout.dim[0].label  = "height"
#     layout.dim[0].size   = 2
#     layout.dim[0].stride = 2*2
#     layout.dim[1].label  = "width"
#     layout.dim[1].size   = 2
#     layout.dim[1].stride = 2
# 
#     array = Float32MultiArray(layout,data)
    while not rospy.is_shutdown():
          
        rospy.loginfo(data)
        pub.publish(array)
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass