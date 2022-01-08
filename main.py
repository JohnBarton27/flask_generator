import os
from pathlib import Path
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


# Base information
project_name = input('Project name: ')
repo_slug = project_name.lower().replace(' ', '-')
project_dir = get_project_dir()
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

print(f'Creating project \'{project_name}\'...')
