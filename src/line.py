#!/usr/bin/env python

import rospy 
import math
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry


odom_status = 0
line = 1
distance_x = 0
distance_y = 0
door_detected = 0
door_number = 0
rotate = 1
isRotated = 0
isExitedInDoor = 0
angular_speed = 0.1

def callback(msg):
	global odom_status, line, door_detected, angular_speed, distance_x, distance_y, door_number, rotate, isRotated, isExitedInDoor

	if line :
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
			odom_status = 1
			line = 0
			door_detected = 1
			
			if distance_x > 1 and distance_x < 3 :	
				door_number = 1
			if distance_x > 3 and distance_x < 5 :	
				door_number = 2
			if distance_x > 5 and distance_x < 7 :	
				door_number = 3
			if distance_x > 7 and distance_x < 9 :	
				door_number = 4
			
			print "Door number :", door_number 	

		pub.publish(move)

	if door_detected :
		if rotate :
			relative_angle = 1.5508
			t0_r = rospy.Time.now().to_sec()
			current_angle = 0
			move.angular.z = -abs(angular_speed)
			pub.publish(move)
			while(current_angle < relative_angle):
				t1_r = rospy.Time.now().to_sec()
				current_angle = angular_speed * (t1_r - t0_r)
			move.angular.z = 0
			pub.publish(move)
			rotate = 0
			isRotated = 1

		if isRotated :
			move_distance = 1.3 + distance_y
			calc_time = move_distance / 0.1
			time_m = rospy.Time.now().to_sec()
			current_time = 0
			total_time = calc_time + time_m
			move.linear.x = 0.1
			pub.publish(move)
			while(total_time > current_time):
				current_time = rospy.Time.now().to_sec()
			move.linear.x = 0
			pub.publish(move)
			isRotated = 0
			isExitedInDoor = 1

		if isExitedInDoor :
			rotate_angle = 0

			if door_number == 2 :
				rotate_angle = 1.5608
				
			elif door_number == 3 :
				rotate_angle = 3.1428
			elif door_number == 4 :
				rotate_angle = 4.7142
			
			parking_t1 = rospy.Time.now().to_sec()
			current_rot_angle = 0
			move.angular.z = -abs(angular_speed)
			pub.publish(move)
			while(current_rot_angle < rotate_angle):
				parking_t2 = rospy.Time.now().to_sec()
				current_rot_angle = angular_speed * (parking_t2 - parking_t1)
			move.angular.z = 0
			pub.publish(move)
			print "Robot exited in door :", door_number
			print "Task Completed"
			isExitedInDoor = 0

def calcDistance(val):
	global odom_status, distance_x, distance_y
	distance_x = val.pose.pose.position.x
	distance_y = val.pose.pose.position.y
	if odom_status :
		print "Distance x axis :", distance_x
		print "Distance y axis :", distance_y
	odom_status = 0
	return

rospy.init_node('assignment')

rospy.sleep(3)
t_start = rospy.Time.now().to_sec()
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
move = Twist()
odm = rospy.Subscriber('/odom', Odometry, calcDistance)
rospy.spin()
