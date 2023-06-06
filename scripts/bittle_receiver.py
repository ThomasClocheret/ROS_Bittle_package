#!/usr/bin/env python3

import rospy
import serial
from std_msgs.msg import String

def callback(data, port):
    rospy.loginfo('Received message: %s', data.data)
    # Send the received message to the serial port
    with serial.Serial(port=port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1) as ser:
        ser.write(data.data.encode())

def receiver():
    # Initialize the ROS node and subscriber
    rospy.init_node('receiver')
    
    # Get the serial port from the parameter server
    port = '/dev/ttyS0'
    
    # Pass the port to the callback function using a lambda function
    rospy.Subscriber('bittle', String, lambda data: callback(data, port))

    # Spin until the node is stopped
    rospy.spin()

if __name__ == '__main__':
    receiver()
