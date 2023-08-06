---
Title: README.md
Path: README.md
Author: Max Ludden
Date: 2022-11-22
CSS: static/style.css
...

# MaxSetup 0.6.0

## Version 0.6.0 Updates

Updated MaxSetup so the when you call the function `new_run()` it preforms the following:

- Checks to make sure that `run.txt` file exists in the <span style="color:#7700ff;">Current Working Directory (<code>CWD</code>)</span>'s log directory.
  - If it doesn't exist, MaxSetup will:
    -  Read the <span style="color:#7700ff;"><code>CWD</code></span>'s `pyproject.toml` and `poetry.lock` into active memory.
    -  <span style="color:red;">Delete the files and directories in the</span> <span style="color:#7700ff;"><code>CWD</code></span><span style="color:red;">.</span>
    -  <span style="color:#00b000;">Copy the default file structure and files from the template directory into CWD.</span>
    -  Rewrite the `pyproject.toml` and `poetry.lock` back into the <span style="color:#7700ff;"><code>CWD</code></span>.
- After ensuring that `run.txt` exists, it will:
  - Read what the last run was from the file.
  - Increment the last run to determine the current run.
  - Write the current run to disk
  - Setup up the loguru sinks and add the current run to the log's extra dictionary.
  - Clear the console.
  - Print a white horizontal rule to the console with a gradient Run title.
  - Return the configured log and its sinks to what called it.

## Changes in 0.5.0

~~Changed setup to return only "log"~~ (These changes were overwritten as they caused confusion.)

## Purpose

This is a module that automates the file structure and settings of a new project.

## Changes from v0.3.0

Updated module configuration.

## Installation

#### Install from Pip

```Python
pip install maxsetup
```

#### Install from Pipx

```Python
pipx install maxsetup
```


#### Install from Pipx

```Python
python add maxsetup
```


## Usage

All you need from `maxsetup` is the following:


```python
from maxsetup import new_run

log = new_run()
```

MaxSetup keeps track of the current run and logs all output to the console and to loguru sinks.

In addition it creates a file structure for the project that looks like this:

<pre style="background-color:#000000;border:1px solid white;border-radius:1%;padding:10px;">
<h2 style="text-align:center;font-size:2em;">Max Setup File Structure</h2>
<span style="color:cyan;">.</span> <span style="color:cyan;font-size:.8em;">(Current working directory)</span>
<span style="color:white;">│ </span>
<span style="color:white;">├── .env</span>
<span style="color:white;">├──</span> <span style="color:grey;">.gitignore</span>
<span style="color:white;">├──</span> <span style="color:cyan;">.vscode</span>
<span style="color:white;">│   ├──</span> <span style="color:gold;">launch.json</span>
<span style="color:white;">│   ├──</span> <span style="color:gold;">settings.json</span>
<span style="color:white;">│   └──</span> <span style="color:gold;">tasks.json</span>
<span style="color:white;">├──</span> <span style="color:yellow;">LICENSE</span>
<span style="color:white;">├──</span> <span style="color:cyan;">logs</span>
<span style="color:white;">│   ├──</span> <span style="color:#00ff00;">log.log</span>
<span style="color:white;">│   ├── run.txt</span>
<span style="color:white;">│   └──</span> <span style="color:#00ff00;">verbose.log</span>
<span style="color:white;">└──</span> <span style="color:cyan;">static</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Century Gothic Bold.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Century Gothic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Bold Italic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Bold.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Italic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">MesloLGS NF Regular.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Black.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-BlackItalic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Italic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Light.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-LightItalic.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">Urbanist-Regular.ttf</span>
    <span style="color:white;">├──</span> <span style="color:orange;">White Modesty.ttf</span>
    <span style="color:white;">└──</span> <span style="color:magenta">style.css
</pre>