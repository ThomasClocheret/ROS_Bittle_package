#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo('Received message: %s', data.data)

def receiver():
    # Initialize the ROS node and subscriber
    rospy.init_node('receiver')
    rospy.Subscriber('bittle', String, callback)  # Replace with the desired topic name

    # Spin until the node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        receiver()
    except rospy.ROSInterruptException:
        pass