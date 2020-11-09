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


class pos_command:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def add_data(self, x, y):
        self.x = x
        self.y = y


def callback(data):

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
    rospy.init_node('geometry_grounding', anonymous=True)
    print('geom')

    rospy.Subscriber("command", String, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    try:
        geometry_grounding()
    except rospy.ROSInterruptException:
        pass
