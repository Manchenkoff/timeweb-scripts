#!/usr/bin/python3

import os

print("Github settings manager")

user = input("User login >>> ")
email = input("E-Mail address >>> ")

actions = [
	'git config --global user.name {}'.format(user),
	'git config --global user.email {}'.format(email),
	'git config --global color.ui auto',
]

for action in actions:
	os.system(action)
