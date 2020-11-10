#!/usr/bin/python2.7

import numpy as np
import random
import rospy
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Int64MultiArray

# takes as input a signal go_home, go_rand, 'go to n1 n2'
# translates signals in (x_target, y_target)
# sends in output (x_target, y_target)

pub = rospy.Publisher('target_pos', Int64MultiArray, queue_size=10)


def callback(data):
    '''
    Callback function for the user command. 
    If the command is a "go to x y" command, it sets the target position as x,y.
    If the command is a "go home" command, it sets the target postion as home_posx,home_posy.
    If the command is a "go rand" command, it sets the target position as random coordinates.
    It then publishes the target position.
    '''
    pos_to_send = Int64MultiArray()
    pos_to_send.data = []

    stringc = str(data.data)

    # Save positions in the command, if any
    my_command = [int(s) for s in stringc.split() if s.isdigit()]

    # If command is a "go to" command
    if my_command:

        pos_to_send.data = [my_command[0], my_command[1]]

    elif stringc == "go_home":
        pos_to_send.data = [rospy.get_param(
            'home_posx'), rospy.get_param('home_posy')]

    elif stringc == "go_rand":
        pos_to_send.data = [random.randrange(10), random.randrange(10)]

    pub.publish(pos_to_send)


def geometry_grounding():
    """!
    Ros node that subscribes to the targcommand topic and publishes on the target_pos topic.
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
