#!/bin/bash

# Install Apache web services
apt install apache2

# Download the Meraki sample click-through excap code
git clone https://github.com/meraki/js-splash.git

# Copy the excap code to the Apache directory
mv js-splash/public/* /var/www/html/

# Restart Apache so the new files are processed
service apache2 restart
