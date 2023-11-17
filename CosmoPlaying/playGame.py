import cozmo
import socket
import errno
from socket import error as socket_error
from readCards import lookForCards

#need to get movement info
from cozmo.util import degrees, distance_mm, speed_mmps


def cozmo_program(robot: cozmo.robot.Robot):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket_error as msg:
        robot.say_text("socket failed" + msg).wait_for_completed()
    ip = "10.0.1.10"
    port = 5000
    
    try:
        s.connect((ip, port))
    except socket_error as msg:
        robot.say_text("socket failed to bind").wait_for_completed()
    cont = True
    
    robot.say_text("ready").wait_for_completed()    
    
    #SET COZMO's NAME
    myName = 'Dylan'
    card_num = 1
    
    while cont:
        bytedata = s.recv(4048)
        #NOTE: casting bytedata as a string just returns "b'string'" which was not the goal!  
        #data = str(bytedata)
        #we need to decode the byte data to get the contents of the message
        data = bytedata.decode('utf-8')
        if not data:
            cont = False
            s.close()
            quit()
        else:
            #---------------------------------------------------------
            #This is where you need to adjust the program
            #---------------------------------------------------------
            print(data)
            instructions = data.split(';')
            

cozmo.run_program(cozmo_program)