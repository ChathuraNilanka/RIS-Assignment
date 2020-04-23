#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler

PI = 3.1415926535897


def callback(msg):
	angel = 90*2*PI/360
	speed = 10*2*PI/360

	move.linear.x=0
	move.linear.y=0
	move.linear.z=0
	move.angular.x = 0
	move.angular.y = 0

	print "Distance between robot and wall :", msg.ranges[270]
	
	if msg.ranges[270] > 1.0 :
		move.angular.z = -abs(speed)
		t0 = rospy.Time.now().to_sec()
    		current_angle = 0

	    	while(current_angle < angle):
        		vel_pub.publish(move)
        		t1 = rospy.Time.now().to_sec()
        		current_angle = speed*(t1-t0)
		
		move.angular.z = 0
		vel_pub.publish(move)

	if msg.ranges[270] < 1.0 :
		move.angular.z = abs(speed)
		t0 = rospy.Time.now().to_sec()
    		current_angle = 0

	    	while(current_angle < angle):
        		vel_pub.publish(move)
        		t1 = rospy.Time.now().to_sec()
        		current_angle = speed*(t1-t0)
		
		move.angular.z = 0
		vel_pub.publish(move)

	while not rospy.is_shutdown():
		print "Distance between robot and wall :" 
		print msg.ranges[270]
	
		move.linear.x = 0.1
		vel_pub.publish(move)
		if msg.ranges[0] < 0.2:
			move.linear.x = 0
			print "Finished..!"
			vel_pub.publish(move)


rospy.init_node('assignment')

rospy.sleep(3)

scan_sub = rospy.Subscriber('/scan', LaserScan, callback)
vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
move = Twist()

rospy.spin()
