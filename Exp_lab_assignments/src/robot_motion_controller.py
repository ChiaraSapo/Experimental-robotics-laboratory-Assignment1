#!/usr/bin/python2.7

import numpy as np
import random
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import Int64MultiArray
from matplotlib import cm
# takes as input the trajectory
# waits 5 seconds
# sends goto_finished


def show_grid(pos_x, pos_y):
    """!
    Plots the robot trajectory using pyplot.
    """

    fig = plt.figure()
    plt.axis([0, 10, 0, 10])
    plt.xticks(np.arange(0, 10))
    plt.yticks(np.arange(0, 10))

    plt.scatter(pos_x, pos_y, c=cm.hot(np.arange(0, len(pos_x))))
    plt.grid()

    plt.show(block=False)
    plt.pause(4)
    plt.close()


def callback(data):
    """!
    Callback data that simulates the actuation of the robot's motors.
    """

    # receive this as msgs
    trajectory = data.data

    if trajectory:

        trajectory = np.reshape(trajectory, (2, len(trajectory)/2))

        # ... actuate motors...
        time.sleep(2)

        #current_pos = trajectory[:, -1]
        rospy.set_param('current_posx', int(trajectory[0, -1]))
        rospy.set_param('current_posy', int(trajectory[1, -1]))

        # plot
        pos_x = trajectory[0, :]
        pos_y = trajectory[1, :]

        if rospy.get_param('see_plot') == 1:
            show_grid(pos_x, pos_y)


def robot_motion_controller():
    """!
    Ros node that subscribes to the trajectory topic.
    """

    rospy.init_node('robot_motion_controlller', anonymous=True)

    rospy.Subscriber("trajectory", Int64MultiArray, callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    robot_motion_controller()
