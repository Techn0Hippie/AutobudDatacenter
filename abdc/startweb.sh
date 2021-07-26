#Comment/Uncomment based on what server needs to be started at bootup
#Note: you must change the paths to the below directories based on where they are located 
#WEB
sudo node-red -u /node-red-1881 -p 1881 -s /home/pi/abdc/web/settings.js /home/pi/abdc/web/flows_web.json
