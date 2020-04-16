#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler


def callback(msg):
	while not rospy.is_shutdown():
		print "Distance between robot and wall :" 
		print msg.ranges[270]
	
		move.linear.x = 0.1
		if msg.ranges[0] < 0.2:
			move.linear.x = 0
			print "Finished..!"

		pub.publish(move)

rospy.init_node('assignment')

pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
rospy.sleep(3)
start_pose = PoseWithCovarianceStamped()
 
start_pose.pose.pose.position.x = 0.0
start_pose.pose.pose.position.y = 1
start_pose.pose.pose.position.z = 0.0
 
[x,y,z,w]=quaternion_from_euler(0.0,0.0,0.0)
start_pose.pose.pose.orientation.x = x
start_pose.pose.pose.orientation.y = y
start_pose.pose.pose.orientation.z = z
start_pose.pose.pose.orientation.w = w

pub.publish(start_pose)
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist)
move = Twist()

rospy.spin()
