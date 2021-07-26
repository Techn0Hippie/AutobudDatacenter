#Comment/Uncomment based on what server needs to be started at bootup
#Note: you must change the paths to the below directories based on where they are located 
#API
sudo node-red -u /node-red-1880 -p 1880 -s /home/pi/abdc/api/settings.js /home/pi/abdc/api/flows_api.json
