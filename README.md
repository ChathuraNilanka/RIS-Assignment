# RIS-Assignment

roslaunch ris2020 door1.launch

roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping

roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

rosrun map_server map_saver -f ~/map

rosrun assignment main.py

roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map/door1.yaml
