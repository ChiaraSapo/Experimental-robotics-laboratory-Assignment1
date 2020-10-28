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

    stringc = str(data.data)

    # to be done in different node and passed as msg
    #str = 'go_home'
    #str = 'go_rand'
    #str = 'go to 7 8'

    my_command = [int(s) for s in stringc.split() if s.isdigit()]
    if my_command:
        stringc = my_command
        upos_command = pos_command("go_to")
        upos_command.add_data(my_command[0], my_command[1])

    else:
        upos_command = pos_command(stringc)

    if upos_command.name == "go_home":
        target_pos = [rospy.get_param(
            'home_posx'), rospy.get_param('home_posy')]
    elif upos_command.name == "go_rand":
        target_pos = [random.randrange(10), random.randrange(10)]
    elif upos_command.name == "go_to":
        target_pos = [upos_command.x, upos_command.y]
    pos_to_send = Int64MultiArray()
    pos_to_send.data = []
    pos_to_send.data = target_pos
    pub.publish(pos_to_send)


def geometry_grounding():
    rospy.init_node('geometry_grounding', anonymous=True)

    rospy.Subscriber("command", String, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    try:
        geometry_grounding()
    except rospy.ROSInterruptException:
        pass
