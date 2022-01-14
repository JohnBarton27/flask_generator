import os
from pathlib import Path
import shlex
import subprocess
import random
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


def run_cmd(command):
    subprocess.call(shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_requirements():
    req_content = """\
        flask
        xmlrunner
        coverage
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


def create_readme(description):
    global project_name
    global repo_slug
    global port

    readme_content = f"""\
        # {project_name}
        {description}
    
        ## Setup
        ### Requirements
        * Python 3
        
        ### Running
        1. Clone this repository
        1. Run `pip install -r requirements.txt` from the root directory of the repository.
        \t1.This only needs to be run the first time you are starting the application.
        1. Run `cd {repo_slug}; python main.py` from the root directory of this repository.
        \t1. {project_name} will now be accessible in your browser of choice at `localhost:{port}`.
        
        ### Unit Tests
        1. Run `python tests/run_tests.py` from the root directory of the repository.
    """

    return write_to_file('README.md', readme_content)


def create_main():
    global project_name
    global port
    global repo_slug

    main_content = f"""\
        import logging
        import os
        import sqlite3 as sl
        from urllib.request import pathname2url

        from flask import Flask, render_template, request

        app = Flask(__name__, template_folder=os.path.abspath('static'))
        
        @app.route('/')
        def index():
            return render_template('index.html')
            
        def connect_to_database():
            db_name = '{repo_slug}.db'
            try:
                dburi = 'file:{{}}?mode=rw'.format(pathname2url(db_name))
                conn = sl.connect(dburi, uri=True)
                logging.info('Found existing database.')
            except sl.OperationalError:
                # handle missing database case
                logging.warning('Could not find database - will initialize an empty one!')
                conn = sl.connect(db_name)

            
        if __name__ == '__main__':
            # Setup Logging
            logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
            logging.info('Starting {project_name}...')
        
            # Connect to database
            logging.info('About to connect to database...')
            connect_to_database()
            logging.info('Successfully connected to database.')
        
            app.run(port={port}, debug=False, use_reloader=False)
    """

    write_to_file(os.path.join(repo_slug, 'main.py'), main_content)


def create_static_structure():
    global project_name
    global source_root

    static_dir = os.path.join(source_root, 'static')
    os.mkdir(static_dir)

    # CSS
    css_dir = os.path.join(static_dir, 'css')
    os.mkdir(css_dir)
    Path(os.path.join(css_dir, '.gitkeep')).touch()

    # JavaScript
    js_dir = os.path.join(static_dir, 'js')
    os.mkdir(js_dir)
    Path(os.path.join(js_dir, '.gitkeep')).touch()

    # index.html
    index_content = f"""\
        <html>
        <head>
        \t<title>{project_name}</title>
        </head>
        <body>
        \t<h1>{project_name}</h1>
        </body>
        </html>
    """

    write_to_file(os.path.join(static_dir, 'index.html'), index_content)


def setup_unit_tests():
    global project_dir
    global repo_slug

    # Make 'tests' directory
    tests_dir = os.path.join(project_dir, 'tests')
    os.mkdir(tests_dir)
    Path(os.path.join(tests_dir, '__init__.py')).touch()

    # run_tests.py file
    run_tests_content = f"""\
        import pathlib
        import sys
        import unittest
        import xmlrunner
        
        # Set PYTHONPATH
        sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute().parent.absolute().joinpath('tests')))
        sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute().parent.absolute().joinpath('{repo_slug}')))
        
        test_dir = pathlib.Path(__file__).parent.absolute()
        loader = unittest.TestLoader()
        suite = loader.discover(test_dir)
        
        runner = xmlrunner.XMLTestRunner("test-reports")
        results = runner.run(suite)
        if results.errors or results.failures:
            raise Exception('Found unit test failures!')
    """

    write_to_file(os.path.join(tests_dir, 'run_tests.py'), run_tests_content)


def setup_git():
    global project_dir

    os.chdir(project_dir)

    run_cmd('git init')
    run_cmd('git add -A')
    run_cmd('git commit -m "Initial Commit"')

    # Setup github Repo
    # curl -H "Authorization: token ACCESS_TOKEN" --data '{"name":"NEW_REPO_NAME"}' https://api.github.com/orgs/ORGANIZATION_NAME/repos


# Base information
project_name = input('Project name: ')
print(f'Creating project \'{project_name}\'...')

repo_slug = project_name.lower().replace(' ', '-')
project_dir = get_project_dir()
Path(os.path.join(project_dir, '__init__.py')).touch()

create_requirements()
create_gitignore()

port = random.randrange(1024, 9999)

description = input("Project description: ")
create_readme(description)

# Make 'main' source directory
source_root = os.path.join(project_dir, repo_slug)
os.mkdir(source_root)
create_main()
create_static_structure()

# Unit Tests
setup_unit_tests()

# Git setup
setup_git()