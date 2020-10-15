'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial
import requests
from time import sleep
import subprocess
import os
import sys
import json
from threading import Timer
import paho.mqtt.client as mqtt
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import flask
import json
import command
import time
from flask import *
from flask import Flask, jsonify
from multiprocessing import Process, Value

'''f=open("New.txt",'r')
a=f.read()
if (a!=" "):
    subprocess.call(["sudo","kill",a])
f=open("New.txt",'w')
f.write("")
f.close()'''
global Listupdate 
#f= open("New.txt",'w')
#f.write(str(os.getpid()))
#f.close()
global ListStatusOnline
ListStatusOnline=[0,0,0,0]
global NOTYFI_DOOR_OPEN
global NOTIFY_STARTUP
global SETUP_NODE
global TOKEN
global FW_UpdateNode
global RES_SENSOR

NOTYFI_DOOR_OPEN = command.NOTYFI_DOOR_OPEN
NOTIFY_STARTUP = command.NOTIFY_STARTUP
CHECK_NODE_ONLINE_RESPONSE = command.CHECK_NODE_ONLINE_RESPONSE
SETUP_NODE = command.SETUP_NODE
CHECK_NODE_ONLINE = command.CHECK_NODE_ONLINE
TOKEN= command.TOKEN
RES_SENSOR = command.RES_SENSOR
FW_UpdateNode = command.FW_UpdateNode
ser = serial.Serial ("/dev/ttyS0", 9600,timeout=0.03)    #Open port with baud rate
UPDATE_SENSOR = 0


def token(key):
    TOKEN[2]=key
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("NODE_SETTING")
def FW_Update(firmWareName):
    f = open(firmWareName,'r')
    codeString = f.read()
    codeName   = f.name
    ser.write(b'&')
    ser.write(codeName.encode())
    ser.flush()
    ser.write(b'@')
    ser.flush()
    for c in codeString:
        ser.write(c.encode())
        ser.flush
        time.sleep(0.01)
        
    for c in range(0,700):
        ser.write(b' ')
        ser.flush
        time.sleep(0.01)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    objData = json.loads(msg.payload)
    if(objData['opcode']==command.opcode[6] or objData['opcode']==command.opcode[8]):
        if (objData['opcode']==command.opcode[6]):
            SETUP_NODE[1] = command.opcode[6]
            SETUP_NODE[4] = objData['doorId']
            SETUP_NODE[6] = objData['duration'] % 256
            SETUP_NODE[5] = 0
    #time = objData['duration']
            if(objData['duration'] > 256):
                SETUP_NODE[5] = int(objData['duration'] / 256)
                print(bin(objData['duration']))
            SETUP_NODE[7] = objData['enableAlarm']
        if (objData['opcode']==command.opcode[8]):
            SETUP_NODE[1] = command.opcode[8]
            SETUP_NODE[4] = objData['doorId']
            SETUP_NODE[7] = objData['speaker']
        ser.write(SETUP_NODE)
        ser.flush()
    if(objData['opcode']==command.opcode[1]):
        url = "http://10.116.226.36:5000/api/dooropens"
        payload = "{\r\n  \"doorId\":"
        payload += str(objData['doorId'])
        payload += ",\r\n  \"status\": "
        payload += str(ListStatusOnline[objData['doorId']])
        '''response = requests.request("POST", url, headers=headers, data = payload)

        print('Response is: ')
        print(response.text.encode('utf8'))'''
    if(objData['opcode']==command.opcode[1]):
        if (objData['doorId']!=command.doorID[0]):
            FW_UpdateNode[1] = objData['opcode']
            FW_UpdateNode[4] = objData['doorId']
            ser.write(FW_UpdateNode)
            ser.flush()
        FW_Update(objData)

    return

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
cors = CORS(app)
@app.route('/api/updateSensor',methods=['POST'])
def update():
    global Listupdate
    global SETUP_NODE
    #if(request.method == "POST"):
    #print(request.form['enableSpearker'])
    doorId = int(request.form['doorId'])
    timeout = int(request.form['timeout'])
    enableAlarm = int(request.form['enableAlarm'])
    enablespeaker  = int(request.form['enablespeaker'])
    print(request.form['doorId'])
    print(request.form['timeout'])
    print(request.form['enableAlarm'])
    print(request.form['enablespeaker'])
    print(int(timeout % 256))
    SETUP_NODE[1] = 6
    SETUP_NODE[4] = doorId
    SETUP_NODE[6] = int(timeout % 256)
    if(timeout > 256):
        SETUP_NODE[5] = int(timeout / 256)
    SETUP_NODE[7] = enableAlarm
    SETUP_NODE[8] = enablespeaker
    SETUP_NODE[2] = 1
    print(SETUP_NODE)
    for i in range(0,2):
        ser.write(SETUP_NODE)
        print(i,"\n")
        print(SETUP_NODE)
        time.sleep(1)
    ser.flush()
    return "UpdateSensorDone"
##############################################
@app.route('/api/updateFirmware',methods=['POST'])
@cross_origin()
def upload():
    if(request.method == "POST"):
        if request.files:
            f=open("/home/pi/Desktop/code_version2/New.txt",'w')
            f.write(" ")
            f.close()
            firmWare = request.files["updateFirmwareNode"]
            target = os.path.join(APP_ROOT,'')
            firmWareName = firmWare.filename
            destination = "/".join([target,firmWareName])
            firmWare.save(destination)
            print("Receive firmWare")
            name = "/home/pi/Desktop/code_version2" +"/"+ firmWareName
            #if (int(request.form['doorId']) == 0):
            '''print("center")
            f= open("New.txt",'w')
            f.write(str(os.getpid()))
            f.close()
            f=open("mess.txt",'w')
            f.write(firmWareName)
            f.close()
            f=open("doorId.txt",'w')
            f.write(str((request.form['doorId'])))
            f.close()
            #exec(open(name).read())
            #subprocess.call(["python3",name])
            return  "UpdateFirmWareDone" '''
            
            #sys.exit()
            #else:
            FW_UpdateNode[1] = command.opcode[1]
            FW_UpdateNode[4] = int(request.form['doorId'])
            f=open("/home/pi/Desktop/code_version2/mess.txt",'w')
            f.write(name)
            f.close()
            f=open("/home/pi/Desktop/code_version2/doorId.txt",'w')
            f.write(str((request.form['doorId'])))
            f.close()
            start =time.time()
            while 1 :
                f=open("/home/pi/Desktop/code_version2/New.txt",'r')
                a=f.read()
                if (a =='105'):
                    f=open("/home/pi/Desktop/code_version2/New.txt",'w')
                    f.write(" ")
                    f.close()
                    return  "UpdateFirmWareDone"
                    break
                else:
                    if((time.time() - start) > 500):
                        f=open("/home/pi/Desktop/code_version2/New.txt",'w')
                        f.write(" ")
                        f.close()
                        return  "UpdateFirmWareError"
                        break
                        
        #read serial port
       
             
####################################################
        
def receiveNotifyStartup(data):
    print("Node startup!\r")
    print("Door ID is: ")
    print(data[4])
    print("\r\n")
    
    
def checkNodeOnlineResponse(data):
    print("Node online!\r")
    print("Door ID is: ")
    print(data[4])
    print("\r\n")
def getSensor(dataMessenger):
    global ListStatusOnline
    ListStatusOnline[dataMessenger[4]]=1
        
    time = int(dataMessenger[5])
    time = time << 8
    time += int(dataMessenger[6])
    print("Open the door!\r")
    print("Door ID is: ")
    print(dataMessenger[4])
    print("\r")
    print("time is: ")
    print(time)
    print("\r")

    url = "http://10.116.226.36:5000/api/dooropens"

    payload = "{\r\n  \"doorId\":"
    payload += str(dataMessenger[4])
    if ( dataMessenger[2]==command.opcode[5]):
        payload += ",\r\n  \"currentTimeout\": "
        payload += str(time)
        payload += ",\r\n  \"enableAlarm\": "
    if (dataMessenger[2]==command.opcode[8]):
        payload += ",\r\n  \"enablespeaker\": "
    if(dataMessenger[7] == 1):
        print("timeOut true")
        payload += 'true'
    else:
        print("timeOut false")
        payload += 'false'    
    payload += "\r\n}\r\n"

#     payload = "{\r\n  \"doorId\":1,\r\n  \"duration\": 4,\r\n  \"isOverTimeOut\": true\r\n}\r\n"
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    print('url is: ')
    print(url)
    print('data is: ')
    print(payload)
    
    '''response = requests.request("POST", url, headers=headers, data = payload)

    print('Response is: ')
    print(response.text.encode('utf8'))
    return'''
    
def notifyDoor(dataMessenger):
    global ListStatusOnline
    '''if (dataMessenger[4] ==1):
         ListStatusOnline[1]=1
    else:
         ListStatusOnline[2]=1
    print(ListStatusOnline)'''
    print("id door", dataMessenger[4])
    ListStatusOnline[dataMessenger[4]]=1
    print(ListStatusOnline)
    time = int(dataMessenger[5])
    time = time << 8
    time += int(dataMessenger[6])
    
    number = int(dataMessenger[2])
    mumber = number << 8
    number += int(dataMessenger[3])
    print("Open the door!\r")
    print("Door ID is: ")
    print(dataMessenger[4])
    print("\r")
    print("time is: ")
    print(time)
    print("\r")
    url = "http://10.116.227.96:8000/update/openedDoor"
    #url = "https://5f6d590760cf97001641ab93.mockapi.io/iot1"

#     url = "http://10.116.226.36:5000/api/dooropens"
   # url="https://5f6d590760cf97001641ab93.mockapi.io/iot1"
    payload = "{\r\n  \"doorId\":"
    payload += str(dataMessenger[4])
    payload += ",\r\n  \"duration\": "
    payload += str(time)
    payload += ",\r\n  \"NumberPerson\": "
    payload += str(number)
    payload += ",\r\n  \"isOverTimeout\": "
    if(dataMessenger[7] == 1):
        print("timeOut true")
        payload += str(1)
    else:
        print("timeOut false")
        payload += str(0)    
    payload += "\r\n}\r\n"

#     payload = "{\r\n  \"doorId\":1,\r\n  \"duration\": 4,\r\n  \"isOverTimeOut\": true\r\n}\r\n"
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    print('url is: ')
    print(url)
    print('data is: ')
    print(payload)

    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    #sreturn
    
def Auto_Status_Node():
    url = "http://10.116.227.96:8000/update/doorOnlineStatus"
    #url = "https://5f6d590760cf97001641ab93.mockapi.io/iot1"

#     url = "http://10.116.226.36:5000/api/dooropens"
   # url="https://5f6d590760cf97001641ab93.mockapi.io/iot1"
    key=1
    token(key)
    ser.write(TOKEN)
    ser.flush()
    global ListStatusOnline
    print(ListStatusOnline)
    #payload = [{"doorId":1,"online":ListStatusOnline[1] },{"doorId":2,"online": ListStatusOnline[2]}]
    payload = "["
    payload += "{\r\n  \"doorId\":"
    payload += str(command.doorID[1])
    payload += ",\r\n  \"status\": "
    payload += str(ListStatusOnline[1])
    payload += "\r\n}\r\n"
    payload += ",{\r\n  \"doorId\":"
    payload += str(command.doorID[2])
    payload += ",\r\n  \"status\": "
    payload += str(ListStatusOnline[2])
    payload += "\r\n}\r\n"
    payload += "]"

    headers = {
      'Content-Type': 'application/json'
    }
    print('url is: ')
    print(url)
    print('data is: ')
    print(payload)
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    Timer(10,Auto_Status_Node).start()
def main():
    global Listupdate
    global key
    global SETUP_NODE
    global ListStatusOnline
    key=1
    Timer(60,Auto_Status_Node).start()
    while True:
        
        time.sleep(0.5)
        f=open("/home/pi/Desktop/code_version2/mess.txt",'r')
        fileName=f.read()        
        f=open("/home/pi/Desktop/code_version2/doorId.txt",'r')
        doorId = f.read()
        f=open("/home/pi/Desktop/code_version2/mess.txt",'w')
        f.write(" ")
        f.close()
        f=open("/home/pi/Desktop/code_version2/doorId.txt",'w')
        f.write(" ")
        f.close()
        print(doorId,"             ",fileName)
        if (doorId=='1' or doorId=='2'):
            FW_UpdateNode[1] = command.opcode[1]
            FW_UpdateNode[4] = int(doorId)
            print(FW_UpdateNode)
            for i in range(0,1):
                ser.write(FW_UpdateNode)
                ser.flush()
                time.sleep(1)
            length = os.path.getsize(fileName)
            length=str(length)
            print(length)
            ser.write(length.encode())
            ser.flush()
            time.sleep(1)
            FW_Update(fileName)
            time.sleep(50)
            '''f=open("/home/pi/Desktop/code_version2/New.txt",'w')
            f.write(str(105))
            f.close()'''
        else:
            token(key)
            ser.write(TOKEN)
            ser.flush()
            
        #print(1)
        #time.sleep(0.5)
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print("DATA",received_data)
        '''global received_data
        received_data = ser.read()
        while(not received_data):
            received_data = ser.read()
            continue'''
        #received_data = ser.inWaiting()
        
        #read serial port
        if(received_data):
            if((received_data[0]==command.signature and received_data[1] == command.opcode[4] and received_data[2]==command.status[0] ) or (received_data[0]==command.signature and received_data[1] == command.opcode[17] and received_data[2]==command.status[1])):
                key=key+1
                print("vao 1")
                if (key>2):
                    key=1
                token(key)
                print("TOKEN",TOKEN)
                #ser.flush()
            if (received_data[0]==command.signature and received_data[1] == command.opcode[19]):
                ListStatusOnline[received_data[4]]=1
                notifyDoor(received_data)
                print("vao 1")
            if (received_data[0]==command.signature and received_data[1] == command.opcode[5]):
                getSensor(received_data)
            if (received_data[0]==command.signature and received_data[1] == command.opcode[7]):
                getSensor(received_data)
            if (received_data[0]==command.signature and received_data[1] == command.opcode[1]):
                f=open("/home/pi/Desktop/code_version2/New.txt",'w')
                f.write(str(received_data[0]))
                f.close()
                print("update done")
            ###################################################
            

                          
      
#Timer(10,main).start() 

if __name__ == "__main__":
    p = Process(target=main)
    p.start()
    #Timer(10,main).start() 
    #thread.start_new_thread(main,())
    #app.run( debug = False,host='0.0.0.0')
    app.run(host ='10.116.227.78',port =5000, debug=False)
    p.join()