import os
import textwrap


def get_project_dir():
    directory_location = os.path.expanduser(input('Where you do you want to put the project folder? '))
    project_directory = os.path.join(directory_location, repo_slug)
    if not os.path.exists(directory_location):
        raise FileNotFoundError(f'Project location ({directory_location}) must be an existing location!')

    if os.path.exists(project_directory):
        raise FileExistsError(f'Project directory {project_directory} already exists!')

    print(f'Creating project directory \'{project_directory}\'...')
    os.mkdir(project_directory)
    return project_directory


def write_to_file(filepath, content):
    global project_dir
    full_path = os.path.join(project_dir, filepath)

    with open(full_path, 'w') as file_to_write:
        file_to_write.write(textwrap.dedent(content))


def create_requirements():
    req_content = """\
        flask
        xmlrunner
        coverage
        pynput
    """

    write_to_file('requirements.txt', req_content)


def create_gitignore():
    gitignore_content = """\
        venv/
        .idea/
        .cache/
        **/test-reports/*
        .coverage
        coverage.xml
        htmlcov
        *.pyc
        *.iml
        *.db
        *.log
    """

    write_to_file('.gitignore', gitignore_content)


# Base information
project_name = input('Project name: ')
repo_slug = project_name.lower().replace(' ', '-')
project_dir = get_project_dir()
create_requirements()
create_gitignore()

print(f'Creating project \'{project_name}\'...')
