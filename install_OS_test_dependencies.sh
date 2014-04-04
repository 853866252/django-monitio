#!/bin/bash
# remove chromium-browser
sudo mkdir -p /usr/share/desktop-directories
sudo apt-get remove chromium-browser
echo "installing browsers..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable firefox
sudo apt-get install -f
echo "downloading chromedriver..."
wget http://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
echo "adding execution permission to chromedriver binary file"
chmod +x chromedriver