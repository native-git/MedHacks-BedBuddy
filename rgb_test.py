#!/usr/bin/env python

import rospy
from std_msgs.msg import ColorRGBA

rospy.init_node('color_publisher')

pub = rospy.Publisher('/chatter2', ColorRGBA, queue_size=10)

rate = rospy.Rate(10)

for r in range(0,255,50):
	msg = ColorRGBA()
	for g in range(0,255,50):
		for b in range(0,255,50):
			msg.r = r
			msg.g = g
			msg.b = b
			pub.publish(msg)
			rate.sleep()