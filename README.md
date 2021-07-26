# AutobudDatacenter
Application that was designed to run on a raspberry Pi which hosts an API, Database, and Web front end to track and analyze grow data.

# Installation:

**Update and upgrade:** 

sudo apt-get update

sudo apt-get upgrade

**Install Nginx:** sudo apt-get install nginx

**Configure nginx:**

sudo cp default /etc/nginx/sites-enabled/default

Reload nginx: sudo service nginx reload

**Install Mariadb:** sudo apt install mariadb-server

**Configure DB:**

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf

Change bind address line: bind-address = 0.0.0.0

Sudo service mysql restart

**Setup the abadmin user:**

Sudo mysql 

CREATE DATABASE autobud;

CREATE USER  'abadmin'@'localhost' IDENTIFIED BY 'SOMETHINGSECURE';

GRANT ALL PRIVILEGES ON *.* TO 'abadmin'@'%' IDENTIFIED BY 'SOMETHINGSECURE' WITH GRANT OPTION;

grant all privileges on *.* to abadmin@localhost identified by 'SOMETHINGSECURE';

FLUSH PRIVILEGES;

EXIT;

Restart mysql once more: sudo service mysql restart

Load the default empty autobud database: sudo mysqldump autobud > autobudbak.sql

sudo mysql autobud < autobudbak.sql

**Install php-fpm** 

sudo apt install php-fpm

**Install node red:** bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

**Install node red packages:**
For API

cd /node-red-1880

sudo npm install node-red-dashboard

sudo npm i node-red-node-mysql

sudo npm i node-red-node-email

For Web

cd /node-red-1881

sudo npm install node-red-dashboard

sudo npm i node-red-node-mysql

sudo npm install node-red-contrib-moment

sudo npm install node-red-node-ui-table

**Install image to base64 converter** 

sudo apt-get install python3-pip

pip3 install mysql-connector-python-rf

From git pulled abdc directory: sudo cp upload.php /var/www/html/upload.php

From git pulled abdc directory: sudo cp -r uploads /var/www/html/uploads

cd /var/www/html/uploads

sudo chmod +x imguploader.py

If you changed the database user or password, edit the imguploader.py file with the new credentials

# Usage and Features:
Autobud datacenter is a data collection program that is built to run on a raspberry pi. It consists of 3 parts:
 - An API to listen for events
 - A mysql database to save event data and log the time of each event (based on when it is posted to the API
 - A basic web front end to display the data

The program is written in Node-red as it is a lightweight node.js system commonly run on raspberry pis. It can also be deployed on larger servers, but at this point (pre-beta) it is not scalable.


## Needed fixes:
The program also has a small PHP program that will accept .jpg files. When the listener is hit, a .jpg must be sent to the php app (http://[IP]/uploads/) and a post node red API endpoint (http://[IP]:1800/imgupload). Once the post is sent to node red, it exicuts a small python script that converts the .jpg into bas64, writes it to the DB, and deletes the image. 
An ideal fix would be having these 3 parts of the program written in 3 separate languages, all in the PHP program. I needed a solution quickly and this was a fast and interesting way to use 3 programming languages to complete a task.

## Needed adds:
A full CRUD interface built to manage grows in the database

Better chart reporting

Basic UI improvements

Other next obvious steps would be a series of python programs that will run locally on the Pi to allow full grow control from the device. I started working on these before I ported the control functions to my ESP based microcontroller. I will work on getting some of this cleaned up and added.

## API Info:
Autobud Datacenter hosts the following API endpoints:

/imgupload 
(from https://RandomNerdTutorials.com/esp32-cam-post-image-photo-server/)
Listener that accepts the image information from an image post. 
Note: You can also run the code from this tutorial on a ESP32 cam to set up a camera to watch your plants. 

/upload 
Listener to accept grow day data from controller. 
This API should probably be replaced as it listens for the controller to write to the database when it boots up. This will be developed more and is only applicable to Autobud controllers.

/log
Listener that accepts post data from controller about lighting and watering events
Water Event:
Arduino: String postdata = "Id=" + IDx + "&msg=" + 3 + "&amt=" + watertimeN;
Id = ID of the grow
Msg = 3 The value of 3 indicates a water event 
Amt = amount in oz that was watered during this event

The accepted format looks like (from postman)





/data
Listener that writes sensor data to the database. This endpoint accepts the ID of the listener, Temperature, Humidity, and Soil Moisture information. Once the data is received it is written to the database with the time of the post

Arduino example: String httpRequestData = "Id=" + ID + "&msg=" + soilmoisture + "&Temp=" + temp + "&Hum=" + hum;  

The accepted format looks like (from postman)


/emailalert
Listener that accepts information Posted to the API and convets it into an email. You must configure the Email node with server information to allow for the sending of email. This can be done with a basic email address.

The accepted format looks like (from postman)



Ardunio: String postdata = "Id=" + IDx + "&to=" + email + "&ip=" + emailmsg;
Id = ID of grow
To = email address to send to
Ip = Email Message text


##To start Autobud Datacenter run:

1880: APIs
sudo node-red -u /node-red-1880 -p 1880 -s /home/pi/abdc/api/settings.js /home/pi/abdc/api/flows_api.json

1881: Web front end 
sudo node-red -u /node-red-1881 -p 1881 -s /home/pi/abdc/web/settings.js /home/pi/abdc/web/flows_web.json



