#!/usr/bin/python2.7

import numpy as np
import random
import rospy
import numpy as np
from std_msgs.msg import Int64MultiArray

# takes as input the next position to reach (x_target, y_target)
# calulates trajectory
# sends trajectory as output

pub = rospy.Publisher('trajectory', Int64MultiArray, queue_size=10)
# rate = rospy.Rate(10)  # 10hz
trajectory_to_send = Int64MultiArray()
trajectory_to_send.data = []


def callback(data):
    # receive target_pos and current_pos

    target_pos = data.data
    target_x = target_pos[0]
    target_y = target_pos[1]
    current_x = rospy.get_param('current_posx')
    current_y = rospy.get_param('current_posy')

    next_x = []
    next_y = []

    while current_x != target_x:
        current_x = current_x+(target_x - current_x)/abs(target_x - current_x)
        next_x.append(current_x)
        next_y.append(current_y)

    while current_y != target_y:
        current_y = current_y+(target_y - current_y)/abs(target_y - current_y)
        next_x.append(current_x)
        next_y.append(current_y)

    trajectory = np.concatenate((next_x, next_y), axis=0)

    trajectory_to_send.data = trajectory
    pub.publish(trajectory_to_send)


def planner():
    rospy.init_node('planner', anonymous=True)
    

    rospy.Subscriber("target_pos", Int64MultiArray, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    planner()
