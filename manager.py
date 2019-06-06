#!/usr/bin/python3
import os
import sys

# Configuration values
SETTINGS = {
    'HOME': os.path.expanduser('~'),
    'PRODUCTION_DIR': 'production',
    'PROJECTS': {},
    'HOSTS': {},
    'EXCLUDED_HOSTS': ['node', 'production']
}


def scan_projects():
    """
    Scans active projects in the production directory
    :return:
    """
    projects = os.listdir(SETTINGS['PRODUCTION_DIR'])

    projects = {project: os.path.join(SETTINGS['PRODUCTION_DIR'], project) for project in projects}

    return projects


def scan_hosts():
    """
    Scans available hosts in the base user directory
    :return:
    """
    directories = os.listdir(SETTINGS['HOME'])
    directories = filter(lambda x: x[0] != '.', directories)

    hosts = {}

    for directory in directories:
        if directory not in SETTINGS['EXCLUDED_HOSTS']:
            path = os.path.join(SETTINGS['HOME'], directory)

            if os.path.isdir(path):
                hosts[directory] = path

    if len(hosts) < 1:
        print("No hosts found")
        exit()

    return hosts


def select_path(directory_type: str):
    """
    Helps choose host full path by user input
    :param directory_type: <hosts | projects> which path necessary
    :return:
    """
    directory_type = directory_type.upper()

    print(f"\n{directory_type}: \n")
    selector = list(SETTINGS[directory_type].keys())

    for idx, directory in enumerate(selector, start=1):
        print(f"#{idx}. {directory}")

    selected_path = SETTINGS[directory_type][selector[int(input("\nEnter the row number >>> ")) - 1]]

    return selected_path


def init():
    """
    Script configuration initializing
    :return:
    """
    SETTINGS['PRODUCTION_DIR'] = os.path.join(SETTINGS['HOME'], SETTINGS['PRODUCTION_DIR'])

    if not os.path.isdir(SETTINGS['PRODUCTION_DIR']):
        os.mkdir(SETTINGS['PRODUCTION_DIR'])

    SETTINGS['HOSTS'] = scan_hosts()
    SETTINGS['PROJECTS'] = scan_projects()


def show_help():
    """
    "How to use" help message
    :return:
    """
    message = "TimeWeb Deploy Manager v2\n"
    message += "Available commands: \n\n"

    for command, data in COMMANDS.items():
        message += f"{command} - {data['desc']}\n"

    print(message)


def init_node():
    """
    Installs Node.js and writes aliases into current user profile bash file
    Help: https://timeweb.com/ru/help/pages/viewpage.action?pageId=8781927
    :return:
    """

    action_sequence = [
        'wget https://nodejs.org/dist/v10.14.1/node-v10.14.1-linux-x64.tar.gz',
        'tar xf node-v10.14.1-linux-x64.tar.gz',
        'mv node-v10.14.1-linux-x64.tar.gz node'
    ]

    aliases = [
        f"alias node ='{SETTINGS['HOME']}/node/bin/node'",
        f"alias npm ='{SETTINGS['HOME']}/node/bin/npm'",
        f"export PATH=$PATH:{SETTINGS['HOME']}/node/bin/"
    ]

    for command in action_sequence:
        os.system(command)

    bash_files = ['.bash_profile', '.bashrc']

    for file in bash_files:
        with open(os.path.join(SETTINGS['HOME'], file), 'w') as f:
            f.writelines([f"{x}\n" for x in aliases])

    print('NodeJS installed successfully')


def clone_project():
    """
    Clones Github project to the "production" directory
    :return:
    """
    git = input("Repository name (ex: 'manchenkov/project-name') >>> ")
    project = input("Project directory (ex: 'my-project') >>> ")

    source = f"https://github.com/{git}.git"
    path = os.path.join(SETTINGS['PRODUCTION_DIR'], project)

    if not os.path.isdir(path):
        os.mkdir(path)

    git_clone_command = f"git clone {source} {path}"

    if input("Are You sure? [y/n] >>> ").lower().startswith('y'):
        os.system(git_clone_command)
        print("Project was cloned successfully!\n")

        if input("Do You want to link this project? [y/n] >>> ").lower().startswith('y'):
            link_project()
        else:
            print("Good Bye!\n")
    else:
        print("Rollback...")


def update_project():
    """
    Pulls updates from remote Github repository for selected project
    :return:
    """
    selected_project = select_path('projects')

    git_actions = [
        'git fetch',
        'git pull'
    ]

    os.chdir(selected_project)

    for command in git_actions:
        os.system(command)


def link_project():
    """
    Setups a symlink to the selected project into public directory
    :return:
    """
    selected_project = select_path('projects')
    selected_host = select_path('hosts')

    if input("Are You sure? [y/n] >>> ").lower().startswith('y'):
        path = os.path.join(selected_host, 'public_html')

        if os.path.islink(path):
            os.unlink(path)
        else:
            os.rename(path, f"{path}_old")

        os.symlink(selected_project, path, True, )

        print("Symlink to the project was created")


# Commands list to execute
COMMANDS = {
    'help': {
        'desc': 'Show this message',
        'callback': show_help
    },
    'node': {
        'desc': 'Initialize bash profile aliases (php, npm)',
        'callback': init_node
    },
    'clone': {
        'desc': 'Clones a project from Github into production directory',
        'callback': clone_project
    },
    'link': {
        'desc': 'Creates a symlink to the production project in the public host',
        'callback': link_project
    },
    'update': {
        'desc': 'Get the last updates from Github for the selected project',
        'callback': update_project
    },
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    else:
        action = sys.argv[1]

        try:
            if action in COMMANDS:
                if action != 'help':
                    init()

                COMMANDS[action]['callback']()
            else:
                show_help()
        except KeyboardInterrupt:
            print("\nGood Bye!")
