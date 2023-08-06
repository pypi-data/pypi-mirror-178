# Flexmin #

Flexmin is a web based system administration tool for those who don't have
time to remember all the different configuration files paths and commands
needed to to make the occasional configuration change.

Linux is a great operating system, but unless you are doing administration
tasks on a regular basis you find yourself having to remind yourself where
that configuration file is or what command you need to run to make the change
you need right now. Flexmin is the solution to this problem.

Flexmin is perfect for those who use Linux but don't want to be a full time 
Linux administrator; it makes common administration tasks easy. It is perfect
for web developers who want to use NGINX, uWSGI and Python based web tools as
it makes the set up and administration of these parts of a web stack easy.

If you have clients who need to run a server you can use Flexmin to give them
easy access to perform any common system administration tasks by themselves.

If you can create a BASH script to do a common task then you can easily link
this script to Flexmin, it is designed to present a user friendly web interface
to a BASH script or Python scripts.

Flexmin consists of a python based service (daemon) that runs as root and 
handles tasks sent to it my the web based GUI. More information here: 
[Creative Edge Digital](http://creativeedgedigital/flexmin/)

## Install ##

### Prerequisites ###

Flexmin requires the following:

- OpenSSL (openssl)
- Python 3 and Pip (python3 and python-pip or python3-pip)
- NGINX (nginx)
- uWSGI and uWSGI Python Plugins (uwsgi, uwsgi-plugin-python or uwsgi-plugin-python3)

> Debian based distros (Raspbian and Ubuntu for example) seem to need packages
> python3-pip and uwsg-plug-python3, they also require the use of the `pip3` 
> command instead of pip.

Python modules required (pip, or pip3 command for debian and ubuntu based distro):

- wheel (install first, needed for subsequent installs)
- pyyaml
- py4web
- click

Once the Prerequisites are all installed run these commands:

```bash
sudo pip install flexmin
sudo flexmin install
```

The first command should install the flexmin package, the second unpacks some 
associated files and folder and configures flexmin to run on your system. After
running these commands you should have a fully functioning web server and 
Flexmin web interface.

