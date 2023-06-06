#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def sender():
    # Initialize the ROS node and publisher
    rospy.init_node('sender')
    pub = rospy.Publisher('bittle', String, queue_size=10)  # Replace with the desired topic name

    # Send a message every second
    rate = rospy.Rate(1)  # 1 Hz
    while not rospy.is_shutdown():
        message = 'kbalance'
        rospy.loginfo('Sending message: %s', message)
        pub.publish(message)
        rate.sleep()

if __name__ == '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass