#!/usr/bin/python3

import sys
import os

HOME = '/home/m/manchenko7'
PRODUCTION = os.path.join(HOME, 'production')

def get_projects_dict():
	"""Returns projects list {project: path}"""
	names = os.listdir(PRODUCTION)
	
	if len(names) < 1:
		print('Projects not found!')
		exit()
	
	paths = [os.path.join(PRODUCTION, x) for x in names]
	
	return dict(zip(names, paths))

def get_hosts_dict():
	"""Returns hosts list {host: path}"""
	names = os.listdir(HOME)
	
	def filter_hosts(item):
		if item[0] != '.' and item not in ['production', 'bin']:
			if os.path.isdir(os.path.join(HOME, item)):
				return True
		return False
	
	names = list(filter(filter_hosts, names))
	paths = [os.path.join(HOME, x) for x in names]
	
	return dict(zip(names, paths))
	
def select_directory(dir_type):
	"""Selects specific directory to work"""
	if dir_type == 'project':
		print('--- PROJECTS LIST ---\n')
		
		items = get_projects_dict()
		names = list(items)
	elif dir_type == 'host':
		print('--- HOSTS LIST ---\n')
		
		items = get_hosts_dict()
		names = list(items)
	
	for index, item in enumerate(names):
		print("[{}] {}".format(index, item))
	
	try:
		idx = int(input("\nSelect ID >>> "))
		
		if idx >= len(names) or idx < 0:
			print('\nID is out of range...')
			exit()
		else:
			return items[names[idx]]
			
	except:
		print('\nInvalid ID, try again...')
		exit()

def action_create():
	"""Creates a new project from Github repository"""
	print("Creating new project...\n")
	
	repository = input("Repository name [Example: repository/project] >>> ")
	project_name = input("Project name >>> ")
	
	source = "https://github.com/{}.git".format(repository)
	dest = os.path.join(PRODUCTION, project_name)
	
	if not os.path.exists(PRODUCTION):
		os.mkdir(PRODUCTION)
	
	command = "git clone {} {}".format(source, dest)
	os.system(command)
	
	print('\nProject was created!')
	
def action_update():
	"""Downloads all updates of project from Github"""
	project = select_directory('project')
	
	try:
		os.chdir(project)
		actions = [
			'git fetch',
			'git pull'
		]
		
		for x in actions:
			os.system(x)
			
	except Exception as error:
		print(error)
		
	print('\nProject was updated!')
	
def action_link():
	"""Sets up a link to redirect host requests to project"""
	project = select_directory('project')
	host = select_directory('host')
	
	try:
		dest = os.path.join(host, 'public_html')
		
		if os.path.exists(dest):
			if os.path.islink(dest) or os.path.isfile(dest):
				os.remove(dest)
			elif os.path.isdir(dest):
				import shutil
				shutil.rmtree(dest)
				
		os.symlink(project, dest, target_is_directory=True)
	except:
		print("Can't create a symlink")
		
	print('\nProject linked!')
	
def action_help():
	"""Shows help message with actions description"""
	print('\nYou can use follow actions:\n')
	
	for item, value in sorted(actions.items()):
		print("{} \t- {}".format(item, value['info']))
		
	print()
	
def invalid_action():
	print('Action name is invalid, check the help below...')
	action_help()

actions = {
	'create' : {'info': 'Create a new project from Github repository', 'callback': action_create},
	'update' : {'info': 'Update a project with Github repository', 'callback': action_update},
	'link' : {'info': 'Create a link to project into a host directory', 'callback': action_link},
	'help' : {'info': 'Show current message', 'callback': action_help}
}

# Start programm with one argument
if len(sys.argv) < 2:
	action_help()
else:
	cmd = sys.argv[1]
	try:
		if cmd in actions:
			actions[cmd]['callback']()
		else:
			invalid_action()
	except KeyboardInterrupt:
		print('\nBye!')
