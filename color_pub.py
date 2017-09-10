#!/usr/bin/env python

import rospy
from std_msgs.msg import ColorRGBA

rospy.init_node("color_pub")

pub = rospy.Publisher('/chatter2', ColorRGBA, queue_size=10)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	for i in range(25):
		msg = ColorRGBA()
		msg.r = 255-(i*10)
		pub.publish(msg)
		rate.sleep()
	for i in range(25):
		msg = ColorRGBA()
		msg.r = 0
		msg.b = 0 + (i*10)
		pub.publish(msg)
		rate.sleep()