#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler

rospy.init_node('assignment', anonymous=True)
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
rospy.sleep(3)

initpose_msg = PoseWithCovarianceStamped()

initpose_msg.header.frame_id = "map"

initpose_msg.pose.pose.position.x = 0.0
initpose_msg.pose.pose.position.y = 0.0
initpose_msg.pose.pose.position.z = 0.0
 
[x,y,z,w]=quaternion_from_euler(0.0,0.0,0.0)
initpose_msg.pose.pose.orientation.x = x
initpose_msg.pose.pose.orientation.y = y
initpose_msg.pose.pose.orientation.z = z
initpose_msg.pose.pose.orientation.w = 1.0

rate = rospy.Rate(10) #10hz

while not rospy.is_shutdown():
	print initpose_msg
	pub.publish(initpose_msg)
	rate.sleep()

