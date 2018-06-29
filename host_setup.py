#!/usr/bin/python3
import os

try:
	current_dir = 'HOME_DIR'
	production_dir = os.path.join(current_dir, 'production')
	
	directories = os.listdir(current_dir)
	projects = os.listdir(production_dir)
	
	def filter_directories(item):
	  dir_path = os.path.join(current_dir, item)
	
	  if os.path.isdir(dir_path):
	    if item[0] != '.' and item not in ['production', 'bin']:
	      return True
	
	  return False
	
	directories = list(filter(filter_directories, directories))
	
	print("--- Projects ---")
	for index, item in enumerate(projects):
	  print("[{}] {}".format(index, item))
	project_id = int(input("\nSelect project repository to link >>> "))
	
	print("--- Hosts ---")
	for index, item in enumerate(directories):
	  print("[{}] {}".format(index, item))
	host_id = int(input("\nSelect host to link '{}' project >>> ".format(projects[project_id])))
	
	source = os.path.join(production_dir, projects[project_id])
	destination = os.path.join(current_dir, directories[host_id])
	
	try:
	  www_root = os.path.join(destination, 'public_html')
	  if os.path.isdir(www_root):
	    os.remove(www_root)  
	
	  os.symlink(source, www_root, target_is_directory=True)
	  print("\n\nProject was initialized!")
	except Exception:
	  print('Some error!')

except KeyboardInterrupt:
	print('\n\nBye!')
