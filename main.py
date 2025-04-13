import serial.tools.list_ports
import cv2
from PIL import Image
from util import get_limits
import time

yellow = [0, 255, 0]  #BGR colorspace
cap = cv2.VideoCapture(0)
#CAMERA RESOLUTION IS 640x480 (X*Y)

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

#COMMANDS
right = "right"
left = "left"
forward = "forward"
up = "up"
down = "down"

while True:
    """command = input("Arduino Command (right/left/forward/off): ")
    serialInst.write(command.encode('utf-8'))"""

    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        if((x2+x1)/2 > 426):
            print((x2+x1)/2 - 320, " PIXELS TO THE RIGHT")
            serialInst.write(right.encode('utf-8'))
            time.sleep(1)

        elif((x2+x1)/2 < 214):
            print(320 - (x2+x1)/2, " PIXELS TO THE LEFT")            
            serialInst.write(left.encode('utf-8'))
            time.sleep(1)

        elif((x2+x1)/2 >= 214 and (x2+x1)/2 <= 426):
            print("HOROZANTALLY CENTERED")            
            serialInst.write(forward.encode('utf-8'))
            time.sleep(1)

        '''else:
            serialInst.write(forward.encode('utf-8'))
            time.sleep(1)'''
        
        if((y2+y1)/2 < 160):
            print(240 - (y2+y1)/2, " PIXELS UPWARDS")
            serialInst.write(up.encode('utf-8'))
            time.sleep(1)

        elif((y2+y1)/2 > 320):
            print((y2+y1)/2 - 240, " PIXELS DOWNWARDS")
            serialInst.write(down.encode('utf-8'))
            time.sleep(1)
            
        elif((y2+y1)/2 >= 160 and (x2+x1)/2 <= 320):
            print("VERTICALLY CENTERED")
            
        '''else:
            print("VERTICALLY CENTERED")
            serialInst.write(forward.encode('utf-8'))'''

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        serialInst.write(forward.encode('utf-8'))
        cap.release()
        cv2.destroyAllWindows()
        exit()