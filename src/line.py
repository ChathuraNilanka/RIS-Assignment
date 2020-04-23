#!/usr/bin/env python

import rospy 
import math
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry


def callback(msg):
	if not(math.isinf(msg.ranges[260])):
		print "Distance between robot and wall :", msg.ranges[270]
		

	if msg.ranges[270] <= 1:
		move.angular.z = 0.01
		move.linear.x = 0.1

	if msg.ranges[270] >= 1:
		move.angular.z = -0.01
		move.linear.x = 0.1

	if msg.ranges[270] < 1 and msg.ranges[270] > 1:
		move.angular.z = 0
		move.linear.x = 0.1

	if msg.ranges[0] <= 0.3:
		move.angular.z = 0
		move.linear.x = 0

	if math.isinf(msg.ranges[260]):
		move.angular.z = 0
		move.linear.x = 0

	pub.publish(move)
			
def calcDistance(val):
	distance = val.pose.pose.position.x
	print "Distance :", distance
	return distance

rospy.init_node('assignment')

rospy.sleep(3)

sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
move = Twist()
odm = rospy.Subscriber('/odom', Odometry, calcDistance)
rospy.spin()
