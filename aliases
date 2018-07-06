#!/usr/bin/python3

import os

HOME = os.path.expanduser('~')

aliases = [
	"alias php='/opt/php7.1/bin/php'",
	"alias node='{}/bin/nodejs/bin/node'".format(HOME),
	"alias npm='{}/bin/nodejs/bin/npm'".format(HOME),
	"export PATH=$PATH:{}/bin/nodejs/bin".format(HOME)
]

bash_files = ['.bash_profile', '.bashrc']

for file in bash_files:
	with open(os.path.join(HOME, file), 'w') as f:
		f.writelines(["{}\n".format(x) for x in aliases])
		
print('Profile aliases was upated!')
