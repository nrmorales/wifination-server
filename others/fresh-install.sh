#!/bin/bash

echo "Starting installation of complete wifination backend server"
apt-get update
apt-get install -y freeradius freeradius-mysql mysql-server python-pip apache2 nmap git
pip install flask

clear

echo "Downloading frontend and configuring apache"
#install apache2 and webserver stuff
cd ~/
git clone https://github.com/ibaguio/wifination-server
cp ~/wifination-server/others/sites-available-wifination /etc/apache2/sites-available/wifination
ln -l /etc/apache2/sites-available/wifination-server /etc/apache2/sites-enabled/wifination-server
rm /etc/apache2/sites-available/default*

a2dissite default
a2ensite wifination
echo "Restarting apache"
service apache2 restart

#configure FreeRADIUS server below
echo "Configuring FreeRADIUS server"
