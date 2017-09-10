#!/usr/bin/env python

from firebase import firebase
from time import sleep
firebase = firebase.FirebaseApplication('https://medhack-6e40c.firebaseio.com/', None)
result = firebase.get('/patients', None)

for i in result[1]:
	j = list(i)
	if j[0] == "-":
		print i
		firebase.delete('/patients/1',i)
