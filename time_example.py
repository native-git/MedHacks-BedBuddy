#!/usr/bin/env python

from datetime import datetime
from time import sleep

def get_time():
	raw_time = str(datetime.now()).split()
	ymd = raw_time[0]
	hms = raw_time[1].split('.')[0]
	return ymd + "T" + hms + "Z"

for i in range(4):
	print get_time()
	sleep(1)

