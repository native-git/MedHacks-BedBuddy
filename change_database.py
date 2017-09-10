#!/usr/bin/env python

from time import sleep
from datetime import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://medhack-6e40c.firebaseio.com/', None)

states = ["left","back","right"]

def get_time():
	raw_time = str(datetime.utcnow()).split()
	ymd = raw_time[0]
	hms = raw_time[1].split('.')[0]
	return ymd + "T" + hms + "Z"

while True:
	for i in states:
		firebase.put('/patients/0','status',i)
		firebase.put('/patients/0','lastRolled',get_time())
		sleep(10)