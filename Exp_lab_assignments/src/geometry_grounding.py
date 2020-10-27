#!/usr/bin/python2.7

import numpy as np
import random
import rospy
import numpy as np
from std_msgs.msg import Int64MultiArray

# takes as input a signal go_home, go_rand, 'go to n1 n2'
# translates signals in (x_target, y_target)
# sends in output (x_target, y_target)


class pos_command:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def add_data(self, x, y):
        self.x = x
        self.y = y


def geometry_grounding():
    pub = rospy.Publisher('target_pos', Int64MultiArray, queue_size=10)
    rospy.init_node('geometry_grounding', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    pos_to_send = Int64MultiArray()
    pos_to_send.data = []
    while not rospy.is_shutdown():
        # to be done in different node and passed as msg
        #str = 'go_home'
        #str = 'go_rand'
        str = 'go to 7 8'
        current_pos=[0,0]

        my_command = [int(s) for s in str.split() if s.isdigit()]
        if my_command:  # check was made in previous step
            str = my_command
            upos_command = pos_command('go_to')
            upos_command.add_data(my_command[0], my_command[1])

        else:
            upos_command = pos_command(str)

        if upos_command.name == 'go_home':
            target_pos = [4, 4]  
        elif upos_command.name == 'go_rand':
            target_pos = [random.randrange(10), random.randrange(10)]
        elif upos_command.name == 'go_to':
            target_pos = [upos_command.x, upos_command.y]


        pos_to_send.data = np.concatenate((target_pos, current_pos), axis=0)

        pub.publish(pos_to_send)
        rate.sleep()

    pass


if __name__ == '__main__':
    try:
        geometry_grounding()
    except rospy.ROSInterruptException:
        pass
