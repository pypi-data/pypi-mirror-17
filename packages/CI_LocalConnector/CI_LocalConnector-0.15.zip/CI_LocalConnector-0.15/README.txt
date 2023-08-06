Local Connector Python
-----------------------------
Created by Idop - 21.6.2016

reads Modbuc TCP tags and send to web service using OAuth authentication
Runs on Python 2.7.9 and tested on raspberi Pi3 - debian Jesi OS

How to Operate:
------------------------------
After installing correctly all componenets you can run
sudo python CI_LocalConnector.py help
This will show all operating options

after testing is done you can operate application in production mode using

sudo python CI_LocalConnector.py MainLoop



Install Instructions
------------------------------
run the next commands to install pymodbus module ("no module error")
pip install pymodbus
sudo pip install pymodbus

run the next commands to install etherNetIP module ("no module error")
sudo pip install cpppo


To run script on machine startup :


edit startupscript
sudo nano /etc/init.d/idopStartUp.sh

sudo chmod 755 /etc/init.d/idopStartUp.sh


sudo update-rc.d idopStartUp.sh defaults



to remove from startup

sudo update-rc.d -f idopStartUp.sh remove



inside this file we just call another shell

idopStartUp.sh

-------------
#! /bin/sh

# /etc/init.d/idopStartUp.sh

bash /home/pi/CI_Projects/launcher.sh &



#!/bin/sh

# launcher.sh

#navigate home than to this directory then back home


cd /

cd /home/pi/CI_Projects
export PATH="$PATH:/usr/lib/python2.7:/usr/lib/python2.7/plat-arm-linux-gnueabihf:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/home/pi/.local/lib/python2.7/site-packages:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PILcompat:/usr/lib/python2.7/dist-packages/gtk-2.0:/usr/lib/pymodules/python2.7"

sudo python CI_LocalConnector.py MainLoop


cd /

Prepare Setup
------------------------
python setup.py sdist upload

pypi account : user=idopeles password=ContelDb2016