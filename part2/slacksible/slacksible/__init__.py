import click
import yaml
import os
import pwd
import grp
import subprocess
from stat import *


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

def pkg_exists(name):
  """Returns true if package is installed, false otherwise"""
  try:
     devnull = open(os.devnull, 'w')
     subprocess.check_call(["dpkg", "-l", name], stdout=devnull, stderr=devnull)
     return True
  except subprocess.CalledProcessError:
    return False

def restart_service(names):
  for name in names:
    subprocess.call(["sudo", "service", name, "restart"])

def install_pkg(config):
  if not pkg_exists(config["name"]):
    subprocess.call(["sudo", "apt-get", "install", "-y", config["name"]])

def destroy_pkg(config):
  if pkg_exists(config["name"]):
    subprocess.call(["sudo", "apt-get", "remove", "-y", config["name"]])

def file_needs_changing(config):
  #Check if file exists
  if not os.path.isfile(config["location"]):
    return True
  #Check file permissions
  if not oct(os.stat(config["location"])[ST_MODE])[-3:] == config["permissions"]:
    return True
  #Check owner
  if not pwd.getpwuid(os.stat(config["location"]).st_uid).pw_name == config["owner"]:
    return True
  #Check group
  if not pwd.getpwuid(os.stat(config["location"]).st_gid).pw_name == config["group"]:
    return True
  #Check content
  with open(config["location"], 'r') as toread:
    content = toread.read()
  if not content == config["content"]:
    return True

  return False

def install_file(config):
  if file_needs_changing(config):
    with open(config["location"], 'w') as f:
      f.write(config["content"])
    os.chown(config["location"], pwd.getpwnam(config["owner"]).pw_uid, 
             grp.getgrnam(config["group"]).gr_gid)
    if "restarts" in config:
      restart_service(config["restarts"])

def destroy_file(config):
  if os.path.isfile(config["location"]):
    os.remove(config["location"])

if __name__ == '__main__':
    entry()
