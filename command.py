NOTYFI_DOOR_OPEN = bytearray.fromhex("69 10 00 04 01 00 00 00 00")
NOTIFY_STARTUP = bytearray.fromhex("69 02 00 01 01 00 00 00 00")
CHECK_NODE_ONLINE_RESPONSE = bytearray.fromhex("69 02 00 00 00 00 00 00 00")
SETUP_NODE = bytearray.fromhex("69 01 00 00 00 00 00 00 00")
CHECK_NODE_ONLINE = bytearray.fromhex("69 05 00 00 00 00 00 00 00")
TOKEN=bytearray.fromhex("69 04 00 00 ")
RES_SENSOR = bytearray.fromhex("69 00 00 00 00 00 00 00 00")
FW_UpdateNode = bytearray.fromhex("69 00 00 00 00 00 00 00 00")
###############################################################
form=["signature","opcode","number1","number2","doorID","time1","time2","status","from"]
NOTIFY_DOOR = bytearray.fromhex("69 13 00 00 00 00 00 00 00")
RES_SENSOR = bytearray.fromhex("69 00 00 00 00 00 00 00 00")
RES_FW_Update = bytearray.fromhex("69 01 00 00 00 00 00 00 00")

form_resporn=["signature","opcode","status","from"]
RES_TOKEN = bytearray.fromhex("69 04 00 00 00 00 00 00 00")
RES_STATUS = bytearray.fromhex("69 11 01 00 00 00 00 00 00")
RES_STATUS_UPDATE = bytearray.fromhex("69 11 00 00 00 00 00 00 00")
RES_NODE_ONLINE   = bytearray.fromhex("69 02 00 00 00 00 00 00 00")
stop=170
###############################################################
signature = 105
opcode    = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
doorID    = [0,1,2]
status    = [0,1]
fromnode  = [0,1,2]
OPEN   = 1
CLOSE  = 0
OPEN_TIMEOUT  = 2
timeOut = 10
timeOut_speaker = 3
TURN_ON = 0
TURN_OFF = 1
NumberPerson=0
statusDoor = CLOSE
enableAlarm = 1
speaker     = 1
start = 0
number_token = [0,1,2,3,4,5]


















