# slacksible
Its like Ansible, but way worse!
---

## Installation
```
# Install git, pip 
sudo apt-get install -y git python-pip
#OR
sudo ./bootstrap.sh

# Get slacksible
git clone https://github.com/KingOfPoptart/slackchallenge

#Install with pip
cd slackchallenge/part2/slacksible
pip install .

# slacksible will now be on your PATH
```

---

## Running
```
# To provision your machine:
slacksible --conf configuration.yml --apply

# To de-provision your machine
slacksible --conf ./phpapp.yml --destroy
```

---
## Example configuration yml is included at phpapp.yml
This will provision the "Hello World" PHP Apache2 server
```
# To provision your machine:
slacksible --conf slackchallenge/part2/phpapp.yml --apply

# To de-provision your machine
slacksible --conf slackchallenge/part2/phpapp.yml --destroy
```

---
## To create a new provisioning configuration
Example configuration can be found at `slackchallenge/part2/phpapp.yml`

### Installing a package
```
- package:
    name: "package_name_to_install"
```
* name - package to install with apt-get

### Adding a file
```
- file:
    location: "/path/to/file"
    permissions: "644"
    owner: "root"
    group: "root"
    content: |
      <?php
      header("Content-Type: text/plain");
      echo "Hello, world!\n";
      ?>
    restarts: ["apache2"]
```
* location - where to place the file
* permissions - numeric permission to set file
* owner - owner of file
* group - group of file
* content - content of file, supports multiline (as shown above)
* restarts - Restarts the listed services IFF the file is created or changed in any way

### Removing a file
```
- fileremove:
    location: "/var/www/html/index.html"
```
* location - path of file to remove

