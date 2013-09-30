This game is created in python.

It requires ROS with the openNI tracker if you want to use the kinect. It subscribes to the /skeleton_markers channel.

The python modules that are required are:

pygame, zmq (2.2), numpy

To run the game with just the keyboard: 
python basicGame.py 

To test the kinect:
python ros_classes.py

To run the game with networking:
python networkingGame.py

To run the game with ROS and Networking:
python ros_game.py

All networking needs the PHP server running. This server gives the clients the IP of the hosting player. This can be a dedicated server. In that case, run python dedicated_game_server.py on the server. Run before starting the clients.


