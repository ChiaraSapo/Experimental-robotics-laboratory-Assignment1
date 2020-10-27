#!/usr/bin/python2.7

import numpy as np
import random
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import Int64MultiArray

# takes as input the trajectory
# waits 5 seconds
# sends goto_finished


def show_grid(pos_x, pos_y):

    fig = plt.figure()
    plt.axis([0, 10, 0, 10])
    plt.xticks(np.arange(0, 10))
    plt.yticks(np.arange(0, 10))

    plt.scatter(pos_x, pos_y)
    plt.grid()

    plt.show(block=False)
    plt.pause(4)
    plt.close()


def callback(data):

    # receive this as msgs
    trajectory = data.data
    trajectory = np.reshape(trajectory, (2, len(trajectory)/2))

    # ... actuate motors...
    time.sleep(2)

    current_pos = trajectory[:, -1]

    # plot
    pos_x = trajectory[0, :]
    pos_y = trajectory[1, :]

    show_grid(pos_x, pos_y)

    # send goto_finished, current_pos


def robot_motion_controller():

    rospy.init_node('robot_motion_controlller', anonymous=True)

    rospy.Subscriber("trajectory", Int64MultiArray, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    robot_motion_controller()
