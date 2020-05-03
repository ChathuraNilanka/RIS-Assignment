#!/usr/bin/env python

import rospy 
import math
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from nav_msgs.msg import Odometry


odom_status = 0
line = 1
distance_x = 0
distance_y = 0
roll = pitch = yaw = 0.0
kp = 0.5
door_detected = 0
door_number = 0
rotate = 1
isRotated = 0
isExitedInDoor = 0
angular_speed = 0.1
target_rad = 0
target = 0


def callback(msg):
	global odom_status, line, door_detected, angular_speed, distance_x, distance_y, door_number, rotate, isRotated, isExitedInDoor, roll, pitch, yaw, target_rad, target

	if line :
		target = 0

		if not(math.isinf(msg.ranges[260])):
			print "Distance between robot and wall :", msg.ranges[270]
		
		if msg.ranges[270] < 1 and msg.ranges[90] > 2.5:
			move.angular.z = 0.5
			move.linear.x = 0.5

		if msg.ranges[270] > 1 and msg.ranges[90] < 2.5:
			move.angular.z = -0.5
			move.linear.x = 0.5

		if msg.ranges[270] > 1 and msg.ranges[90] > 2.5:
			target_rad = target * math.pi / 180
			move.angular.z = kp * (target_rad - yaw)
			move.linear.x = 0.5

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
			target = -90
			target_rad = target * math.pi / 180
			val = kp * (target_rad - yaw)
			move.angular.z = val
			pub.publish(move)

			if val > -0.01 and val < 0.01:
				rotate = 0
				isRotated = 1

		if isRotated :
			target = -90
			target_rad = target * math.pi / 180
			move_distance = 1.3 + distance_y
			calc_time = move_distance / 0.2
			time_m = rospy.Time.now().to_sec()
			current_time = 0
			total_time = calc_time + time_m
			move.linear.x = 0.2
			pub.publish(move)

			while(total_time > current_time):
				current_time = rospy.Time.now().to_sec()
				move.angular.z = kp * (target_rad - yaw)
				pub.publish(move)
			
			move.linear.x = 0
			move.angular.z = 0
			pub.publish(move)
			isRotated = 0
			isExitedInDoor = 1

		if isExitedInDoor :

			if door_number == 1 :
				print "Robot exited in door :", door_number
				print "Task Completed"
				isExitedInDoor = 0

			elif door_number == 2 :
				target = 180
				target_rad = target * math.pi / 180
				
			elif door_number == 3 :
				target = 90
				target_rad = target * math.pi / 180

			elif door_number == 4 :
				target = 0
				target_rad = target * math.pi / 180
			
			val2 = kp * (target_rad - yaw)
			move.angular.z = val2
			pub.publish(move)
			
			if val2 < 0.01 :
				print "Robot exited in door :", door_number
				print "Task Completed"
				isExitedInDoor = 0



def calcDistance(val):
	global odom_status, distance_x, distance_y, roll, pitch, yaw
	distance_x = val.pose.pose.position.x
	distance_y = val.pose.pose.position.y

	if odom_status :
		print "Distance x axis :", distance_x
		print "Distance y axis :", distance_y

	odom_status = 0

	orientation_q = val.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

	return



rospy.init_node('assignment')

rospy.sleep(3)
t_start = rospy.Time.now().to_sec()
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
move = Twist()
odm = rospy.Subscriber('/odom', Odometry, calcDistance)
rospy.spin()
