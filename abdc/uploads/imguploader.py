#!/usr/bin/python
#Python program to convert uploaded image from camera to Base64 and upload
#in DB. ID is passed from nod-red and file name should match ID.

import sys
import time
import requests
import json
from datetime import datetime
import getopt
import os
from base64 import b64encode
import base64
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="abadmin",
  passwd="SOMETHINGSECURE",
  database="autobud"
)

mycursor = mydb.cursor()

# Get datetime of execution
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d')
sqldate = ("'" + formatted_date + "'")


def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         #timer = arg
        id = arg
        print(id)
        idi = str(id)
        #Open Image and enclode as Base64
        ENCODING = 'utf-8'
        IMAGE_NAME = '/var/www/html/uploads/'+ idi + '.jpg'
        JSON_NAME = 'output.json'
        
        with open(IMAGE_NAME, 'rb') as open_file:
          byte_content = open_file.read()

        base64_bytes = b64encode(byte_content)
        base64_string = base64_bytes.decode(ENCODING)
        json_data = json.dumps(base64_string, indent=2)
        json_datas = json_data.strip('\"')

        #Insert Data into MYSQL
        sql = "INSERT INTO ImgDir (Date, Id, img) VALUES (%s, %s, %s)"
        mycursor.execute(sql, [now, idi, json_datas])
        mydb.commit() 

        #payload = {'id': id, 'img': json_datas}
        #requests.post('http://localhost:1880/imguplaod', data=payload)
        os.remove(IMAGE_NAME)

        

if __name__ == "__main__":
   main(sys.argv[1:])

