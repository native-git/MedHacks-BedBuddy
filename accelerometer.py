#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from numpy import sign
from firebase import firebase
import threading
from time import sleep
from datetime import datetime

firebase = firebase.FirebaseApplication('https://medhack-6e40c.firebaseio.com/', None)
update = True
pos = "back"
stored_pos = "back"

def check_database():
	global stored_pos
	while True:
		stored_pos = firebase.get('/patients/2/status',None)
		#print stored_pos
		sleep(0.5)

def get_time():
	raw_time = str(datetime.utcnow()).split()
	ymd = raw_time[0]
	hms = raw_time[1].split('.')[0]
	return ymd + "T" + hms + "Z"

def update_status():
	global update, pos, stored_pos, firebase
	while True:
		if stored_pos != pos:
			#print "updating: " + str(pos)
			#firebase.put('/patients/1','status',pos,'lastRolled',get_time())
			firebase.put('/patients/2','status',pos)
			firebase.put('/patients/2','lastRolled',get_time())
			update = False
			stored_pos = pos

threading1 = threading.Thread(target=update_status)
threading1.daemon = True
threading1.start()

threading2 = threading.Thread(target=check_database)
threading2.daemon = True
threading2.start()

x_prev = 0
y_prev = 0
z_prev = 0

old_pos = "back"

def callback(msg):
	global x_prev, y_prev, z_prev, old_pos, update, pos, stored_pos
	#print "---"
	#print update
	data = msg.linear_acceleration
	x = data.x
	y = data.y
	z = data.z
	threshold = 0.1
	if abs(x_prev - x) > threshold or abs(y_prev-y)>threshold or abs(z_prev-z)>threshold:
		status = "Moving"
	else:
		status = "Stationary"
	turn = False
	if data.x < -4:
		#print "Patient on left -- Status: " + status
		pos = "left"
		turn = True
		right = True
	if data.x > 4:
		#print "Patient on right -- Status: " + status
		pos = "right"
		turn = True
	if data.z > 4 and not turn:
		pos = "back"
		#print "Patient on back -- Status: " + status
	
	if pos != old_pos:
		update = True
	#print "cur_pos: " + pos + " stored_pos: " + stored_pos
	old_pos = pos

	x_prev = x
	y_prev = y
	z_prev = z
	#print "x: " + str(sign(data.x))
	#print "y: " + str(sign(data.y))
	#print "z: " + str(sign(data.z))

def accel_listener():

	rospy.init_node("android_imu_firebase")
	#rospy.Subscriber("/phone2/android/imu", Imu, callback)
	rospy.Subscriber("/phone2/android/imu", Imu, callback)
	rospy.spin()

accel_listener()