from setuptools import setup

setup(name='slacksible',
  version='0.1',
  description='Like Ansible, just way worse',
  url='https://github.com/KingOfPoptart/slackchallenge/',
  author='RD',
  packages=['slacksible'],
  zip_safe=False,
  entry_points = {
    'console_scripts': ['slacksible=slacksible.commandline:main'],
  },
  install_requires=[
    'click', 'pyyaml'
  ],)
