#!/usr/bin/python2.7

import numpy as np
import random
import rospy
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Int64MultiArray


pub = rospy.Publisher('target_pos', Int64MultiArray, queue_size=10)
pos_to_send = Int64MultiArray()
pos_to_send.data = []


def callback(data):
    """!
    Callback function that computes the command to send to the planner
    """

    stringc = str(data.data)
    # Save positions in the command, if any
    my_command = [int(s) for s in stringc.split() if s.isdigit()]

    # If command is a "go to" command
    if my_command:
        pos_to_send.data = [my_command[0], my_command[1]]

    # If command is a "go home" command
    elif stringc == "go_home":
        pos_to_send.data = [rospy.get_param(
            'home_posx'), rospy.get_param('home_posy')]

    # If command is a "go rand" command
    elif stringc == "go_rand":
        pos_to_send.data = [random.randrange(10), random.randrange(10)]

    pub.publish(pos_to_send)


def geometry_grounding():
    """!
    Ros node that subscribes to the command topic and publishes on the target_pos topic.
    """
    rospy.init_node('geometry_grounding', anonymous=True)

    rospy.Subscriber("command", String, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    try:
        geometry_grounding()
    except rospy.ROSInterruptException:
        pass
