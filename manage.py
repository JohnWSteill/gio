"""
A script that extracts variables from the JSON file and converts 
them into environment variables. Centralise all the management 
functions like starting/stopping the development server or managing 
database migrations. As in flask this is partially done by the 
command flask itself, for the time being I just need to wrap it 
providing suitable environment variables.
"""

#! /usr/bin/env python

import os
import json
import signal
import subprocess

import click


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


setenv("APPLICATION_CONFIG", "development")
# The only env value to specify, if you want testing or production. 
# Used to infer correct JSON:

# Read configuration from the relative JSON file
config_json_filename = os.getenv("APPLICATION_CONFIG") + ".json" 
with open(os.path.join("config", config_json_filename)) as f:
    config = json.load(f)

# Convert the config into a usable Python dictionary
config = dict((i["name"], i["value"]) for i in config)

for key, value in config.items():
    setenv(key, value)


@click.group()
def cli():
    pass

"""
wraps the command flask provided by Flask so that I can run 
./manage.py flask to run it using the configuration development or 
APPLICATION_CONFIG="foobar" ./manage.py flask to use the foobar one.
"""

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    cmdline = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


cli.add_command(flask)

if __name__ == "__main__":
    cli()
