import os
 
 
directory = "/opt/ros/groovy/include/std_msgs"
for path,dirs,files in os.walk(directory):
    for file in files:
        print 'print "#include <ros/'+file+'>"'
