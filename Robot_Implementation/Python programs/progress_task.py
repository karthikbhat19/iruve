'''
* Team Id : 226
* Author List : Vishwas, 
* Filename: progress_task
* Theme: Ant Bot
* Functions: run_bot, get_sims, move_to_node, move, turn, talk_to_arduino 
* Global Variables: serial_communication, bot_position, bot_direction, 
*                   resolution, camera, raw_capture, arena_map, immediate_node
*                   ah_list, block_list 
'''

'''
* Function Name:
* Input:
* Output:
* Logic:
*
* Example Call:
'''

# Import packages
import serial
#import detection
import time
#from picamera import PiCamera 
#from picamera.array import PiRGBArray

# Initialise serial communication between Arduino and Pi
serial_communication = serial.Serial('/dev/ttyUSB0',9600)

# Set initial position and direction of the bot
bot_position = -1
bot_direction = 0

# Setup the PiCamera
resolution = (608, 368)         # resolution for the frame
camera = PiCamera()             # To initialize the PiCamera
camera.resolution = resolution  # set the resolution of the camera
camera.rotation = 180           # to rotate the frames by 180 degrees
camera.framerate = 16           # Set the frame rate
raw_capture = PiRGBArray(camera, size=resolution)

'''
# arena_map : This is a representation of the complete eyantra arena. The nodes
*             are numbered from 0 to 14 and the box pickup/service zones are numbered from -16 to -1.
*             Numbering of the nodes are shown in "arena.png" file presen in the "Images" folder.
*             
*             This variable is a dictionary that contains a node number and a list of 4 sets
*             as the key-value pair. Each of the 4 sets represent the directions in which other nodes
*             are present in the order North, East, South and West. An empty set represents that the
*             node does not have a path in that diresction.
* 
*             Note that 
'''
arena_map = {
    -16: 2,-15: 3,-14: 1,-13: 3,-12: 1,-11: 3,-10: 1,-9: 3,-8: 1,-7: 0,-6: 0,-5: 0,-4: 0,-3: 0,-2: 0,-1: 0,
        0: [{-16,-15,-14,-13,-12,-11,-10,-9,-8,1,2,9,10,11,12,13,14},{-7,-6,-5,6,7,8},{-1},{-4,-3,-2,3,4,5}],
        1: [{-16,2},{-13,-12,-11,-10,12,13},{-7,-6,-5,-4,-3,-2,-1,0,3,4,5,6,7,8},{-15,-14,-9,-8,9,11,14}],
        2: [{-16},set(),{-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,3,4,5,6,7,8,9,10,11,12,13,14},set()],
        3: [set(),{-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-1,0,1,2,6,7,8,9,10,11,12,13,14},{-2},{-4,-3,4,5}],
        4: [set(),{-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-2,-1,0,1,2,3,6,7,8,9,10,11,12,13,14},{-3},{-4,5}],
        5: [set(),{-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-3,-2,-1,0,1,2,3,4,6,7,8,9,10,11,12,13,14},{-4},set()],
        6: [set(),{-7,-6,7,8},{-5},{-16,-15,-14,-13,-12,-11,-10,-9,-8,-4,-3,-2,-1,0,1,2,3,4,5,9,10,11,12,13,14}],
        7: [set(),{-7,8},{-6},{-16,-15,-14,-13,-12,-11,-10,-9,-8,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,9,10,11,12,13,14}],
        8: [set(),set(),{-7},{-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,9,10,11,12,13,14}],
        9: [{-9,-8,11},{-16,-13,-12,-11,-10,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,10,12,13},{-15,-14,14},set()],
        10: [{-11,-10,12},set(),{-13,-12,13},{-16,-15,-14,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,11,14}],
        11: [set(),{-9},{-16,-15,-14,-13,-12,-11,-10,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,12,13,14},{-8}],
        12: [set(),{-11},{-16,-15,-14,-13,-12,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,13,14},{-10}],
        13: [{-16,-15,-14,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,14},{-13},set(),{-12}],
        14: [{-16,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13},{-15},set(),{-14}],
}

immediate_node = [
    2,14,14,13,13,12,12,11,11,8,7,6,5,4,3,0,
    [1,6,-1,3],
    [2,10,0,9],
    [-16,None,1,None],
    [None,0,-1,4],
    [None,3,-3,5],
    [None,4,-4,None],
    [None,7,-5,0],
    [None,8,-6,6],
    [None,None,-7,7],
    [11,1,14,None],
    [12,None,13,1],
    [None,-9,9,-8],
    [None,-11,10,-10],
    [10,-13,None,-12],
    [9,-15,None,-14],
]

ah_list = []
block_list = []

def run_bot():

    get_sims()
    #move_to_node(5,2)
    
    #talk_to_arduino("P") #Pick Block

def get_sims():
    global camera,raw_capture
    talk_to_arduino("O")
    time.spleep(2)
    talk_to_arduino("T45")
    camera.capture("1.png")
    
    time.sleep(2)
    talk_to_arduino("T80")
    camera.capture("2.png")
    time.sleep(2)
    talk_to_arduino("T80")
    camera.capture("3.png")
    time.sleep(2)
    talk_to_arduino("T90")
    camera.capture("0.png")
    time.sleep(2)
    talk_to_arduino("T40")

def move_to_node(node,direction=None):
    global bot_position, arena_map

    while bot_position != node:
        if bot_position<0:
            move(arena_map[bot_position])
        else:
            for i in range(4):
                if node in arena_map[bot_position][i]:
                    move(i)
                    break

    if(direction is not None):
        turn_angle = get_turn_angle(direction)
        turn(turn_angle)

def move(direction, distance = 0):

    global bot_position

    turn_angle = get_turn_angle(direction)
    turn(turn_angle)

    position = immediate_node[bot_position][direction] if bot_position>=0 else immediate_node[bot_position]
    print("Moving to node",position)
    talk_to_arduino("M",str(distance))

def turn(angle):
    global bot_direction

    bot_direction = (bot_direction + angle/90)%4
    print("Turning",angle,"degrees")
    print("Now facing",bot_direction)
    #encoded_angle = ((angle+180)*8)//360
    talk_to_arduino("T",str(angle))

def get_turn_angle(direction):
    global bot_direction

    turn_angle = min(abs(direction - bot_direction),abs(direction-bot_direction+4))*90
    sign = -1 if bot_direction+2<direction else 1
    return turn_angle*sign


def talk_to_arduino(action, value=None):
    global serial_communication

    while(1):
        if(serial_communication.in_waiting>0):
            response = serial_communication.readline()
        if response == "1":
            break
        time.sleep(1)
    
    serial_communication.write(action.encode())
    
    if(value is not None):
        serial_communication.write(value.encode())

if __name__ == "__main__":
    run_bot()