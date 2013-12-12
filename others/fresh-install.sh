#!/bin/bash

echo "Starting installation of complete wifination backend server"
apt-get update
apt-get install -y freeradius freeradius-mysql mysql-server python-pip apache2 nmap git libapache2-mod-wsgi
pip install flask

clear

echo "Downloading frontend and configuring apache"
#install apache2 and webserver stuff
cd ~/
git clone https://github.com/ibaguio/wifination-server
mkdir ~/wifination-server/http
mkdir ~/wifination-server/logs

cp ~/wifination-server/others/sites-available-wifination /etc/apache2/sites-available/wifination
ln -s /etc/apache2/sites-available/wifination /etc/apache2/sites-enabled/wifination
rm /etc/apache2/sites-available/default*

a2dissite default
a2ensite wifination
a2enmod wsgi
adduser wifination
passwd -d wifination
echo "Restarting apache"
service apache2 restart

#configure FreeRADIUS server below
echo "Configuring FreeRADIUS server"