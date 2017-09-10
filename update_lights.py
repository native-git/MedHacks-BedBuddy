#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JoyFeedbackArray, JoyFeedback
from datetime import datetime
from firebase import firebase
from time import sleep
import threading


lights = [False]*5

firebase = firebase.FirebaseApplication('https://medhack-6e40c.firebaseio.com/', None)
rospy.init_node("update_wii_lights")

light_pub = rospy.Publisher('joy/set_feedback',JoyFeedbackArray, queue_size=10)

max_delay = 120 # time between movements in seconds

def get_interval():
	global max_delay
	while not rospy.is_shutdown():
		max_delay = int(firebase.get('/patients/1/interval',None))
		sleep(0.25)

def check_time():
	lastRolled = firebase.get('/patients/1/lastRolled',None)
	return lastRolled

def light_thread():
	global lights, max_delay
	on = True
	delay = 0.5
	all_blink = True
	while not rospy.is_shutdown():
		set_lights = lights[:-1]
		msg = JoyFeedbackArray()
		for i in range(4):
			unit_msg = JoyFeedback()
			unit_msg.type = 0
			unit_msg.id = i
			if set_lights[i] == True:
				unit_msg.intensity = 30.0
			if set_lights[i] == "blinking" and on:
				unit_msg.intensity = 30.0
			if set_lights[i] == False:
				unit_msg.intensity = 0.0
			if set_lights[i] == "blinking" and not on:
				unit_msg.intensity = 0.0
			msg.array.append(unit_msg)
		light_pub.publish(msg)
		sleep(delay)
		on = not on

threading0 = threading.Thread(target=get_interval)
threading0.daemon = True
threading0.start()

threading1 = threading.Thread(target=light_thread)
threading1.daemon = True
threading1.start()

while not rospy.is_shutdown():
	try:
		last_update = datetime.strptime(check_time(), '%Y-%m-%dT%H:%M:%SZ')
	except ValueError:
		test = check_time().split('+')[0]+'Z'
		last_update = datetime.strptime(test, '%Y-%m-%dT%H:%M:%SZ')
	current_time = datetime.utcnow()
	elapsed_time = current_time - last_update
	#print last_update
	time_since = elapsed_time.total_seconds()
	#print int(elapsed_time.total_seconds())
	if time_since < max_delay:
		for i in range(5):
			if max_delay - i*max_delay/5.0 >= time_since:
				lights[i] = True
			else:
				lights[i] = False
	last_light = 0
	for i in range(len(lights)):
		if lights[i] == True:
			last_light = i
	if last_light>=0:
		lights[last_light] = "blinking"
	if time_since >= max_delay:
		lights = ["blinking"]*5
		blinking = True
	#print lights[:-1]