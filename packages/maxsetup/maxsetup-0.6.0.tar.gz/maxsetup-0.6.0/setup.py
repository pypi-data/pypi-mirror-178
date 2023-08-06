# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxsetup']
install_requires = \
['loguru>=0.6.0,<0.7.0',
 'max-yaml>=0.1.0,<0.2.0',
 'maxcolor>=1.0.0,<2.0.0',
 'maxconsole>=0.4.0,<0.5.0',
 'maxprogress>=0.4.0,<0.5.0',
 'rich>=12.6.0,<13.0.0',
 'ujson>=5.5.0,<6.0.0']

entry_points = \
{'console_scripts': ['maxconsole = maxconsole:main']}

setup_kwargs = {
    'name': 'maxsetup',
    'version': '0.6.0',
    'description': 'This is a module that automates the file structure and settings of a new project.',
    'long_description': '---\nTitle: README.md\nPath: README.md\nAuthor: Max Ludden\nDate: 2022-11-22\nCSS: static/style.css\n...\n\n# MaxSetup 0.6.0\n\n## Version 0.6.0 Updates\n\nUpdated MaxSetup so the when you call the function `new_run()` it preforms the following:\n\n- Checks to make sure that `run.txt` file exists in the <span style="color:#7700ff;">Current Working Directory (<code>CWD</code>)</span>\'s log directory.\n  - If it doesn\'t exist, MaxSetup will:\n    -  Read the <span style="color:#7700ff;"><code>CWD</code></span>\'s `pyproject.toml` and `poetry.lock` into active memory.\n    -  <span style="color:red;">Delete the files and directories in the</span>\xa0<span style="color:#7700ff;"><code>CWD</code></span><span style="color:red;">.</span>\n    -  <span style="color:#00b000;">Copy the default file structure and files from the template directory into CWD.</span>\n    -  Rewrite the `pyproject.toml` and `poetry.lock` back into the <span style="color:#7700ff;"><code>CWD</code></span>.\n- After ensuring that `run.txt` exists, it will:\n  - Read what the last run was from the file.\n  - Increment the last run to determine the current run.\n  - Write the current run to disk\n  - Setup up the loguru sinks and add the current run to the log\'s extra dictionary.\n  - Clear the console.\n  - Print a white horizontal rule to the console with a gradient Run title.\n  - Return the configured log and its sinks to what called it.\n\n## Changes in 0.5.0\n\n~~Changed setup to return only "log"~~ (These changes were overwritten as they caused confusion.)\n\n## Purpose\n\nThis is a module that automates the file structure and settings of a new project.\n\n## Changes from v0.3.0\n\nUpdated module configuration.\n\n## Installation\n\n#### Install from Pip\n\n```Python\npip install maxsetup\n```\n\n#### Install from Pipx\n\n```Python\npipx install maxsetup\n```\n\n\n#### Install from Pipx\n\n```Python\npython add maxsetup\n```\n\n\n## Usage\n\nAll you need from `maxsetup` is the following:\n\n\n```python\nfrom maxsetup import new_run\n\nlog = new_run()\n```\n\nMaxSetup keeps track of the current run and logs all output to the console and to loguru sinks.\n\nIn addition it creates a file structure for the project that looks like this:\n\n<pre style="background-color:#000000;border:1px solid white;border-radius:1%;padding:10px;">\n<h2 style="text-align:center;font-size:2em;">Max Setup File Structure</h2>\n<span style="color:cyan;">.</span> <span style="color:cyan;font-size:.8em;">(Current working directory)</span>\n<span style="color:white;">│\xa0</span>\n<span style="color:white;">├── .env</span>\n<span style="color:white;">├──</span> <span style="color:grey;">.gitignore</span>\n<span style="color:white;">├──</span> <span style="color:cyan;">.vscode</span>\n<span style="color:white;">│\xa0\xa0 ├──</span> <span style="color:gold;">launch.json</span>\n<span style="color:white;">│\xa0\xa0 ├──</span> <span style="color:gold;">settings.json</span>\n<span style="color:white;">│\xa0\xa0 └──</span> <span style="color:gold;">tasks.json</span>\n<span style="color:white;">├──</span> <span style="color:yellow;">LICENSE</span>\n<span style="color:white;">├──</span> <span style="color:cyan;">logs</span>\n<span style="color:white;">│\xa0\xa0 ├──</span> <span style="color:#00ff00;">log.log</span>\n<span style="color:white;">│\xa0\xa0 ├── run.txt</span>\n<span style="color:white;">│\xa0\xa0 └──</span> <span style="color:#00ff00;">verbose.log</span>\n<span style="color:white;">└──</span> <span style="color:cyan;">static</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Century Gothic Bold.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Century Gothic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Bold Italic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Bold.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Italic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Regular.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Black.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-BlackItalic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Italic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Light.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-LightItalic.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Regular.ttf</span>\n    <span style="color:white;">├──</span> <span style="color:orange;">White Modesty.ttf</span>\n    <span style="color:white;">└──</span> <span style="color:magenta">style.css\n</pre>',
    'author': 'Max Ludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
