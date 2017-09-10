#!/usr/bin/env python

from datetime import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://medhack-6e40c.firebaseio.com/', None)

def get_time():
	raw_time = str(datetime.utcnow()).split()
	ymd = raw_time[0]
	hms = raw_time[1].split('.')[0]
	return ymd + "T" + hms + "Z"

while True:
	test = raw_input("Press Enter to log in...")
	firebase.put('/patients/3','lastProvider',"0079")
	firebase.put('/patients/3','checkInTime',get_time())
	test = raw_input("Press Enter to check out...")
	firebase.put('/patients/3','checkOutTime',get_time())


