import click
import yaml
from subprocess import call

@click.command()
@click.option("--conf", help="Config file to read in", required=True)
@click.option('--apply/--destroy', help="Whether to apply or destroy changes", required=True)
def entry(conf, apply):
  """Configure/Deconfigure your infrastructure."""
  config = yaml.load(file(conf, 'r'))
  
  for step in config:
    if apply:
      if step.keys()[0] == 'package':
        install_pkg(step.values()[0])
      elif step.keys()[0] == 'file':
        install_file(step.values()[0])
    elif not apply:
      if step.keys()[0] == 'package':
        destroy_pkg(step.values()[0])
      elif step.keys()[0] == 'file':
        destroy_file(step.values()[0])

def check_pkg_exists(name):
  call(["apt", "-qq", "list", "nano"])

def install_pkg(config):
  call(["sudo", "apt-get", "install", "-y", config["name"]])

def destroy_pkg(config):
  call(["sudo", "apt-get", "remove", "-y", config["name"]])

def install_file(config):
  print "install file"

def destroy_file(config):
  print "destroy file"

if __name__ == '__main__':
    entry()
