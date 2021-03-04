#!/usr/bin/env python


# @file robot_motion_controller.py
# @brief This node allows to move the robot from the current to the target position.


import numpy as np
import random
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Bool
from matplotlib import cm
from geometry_msgs.msg import Twist
import sys
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
vel = Twist()
vel.linear.x = 0
vel.linear.y = 0
vel.linear.z = 0
vel.angular.x = 0
vel.angular.y = 0
vel.angular.z = 0

number = 1
curr_x = 0
curr_y = 0

# Calculates the euclidean distance between two given points


def EuclidianDistance(x_goal, y_goal, x_real, y_real):
    euclidean_dist = math.sqrt(
        math.pow((x_goal-x_real), 2) + math.pow((y_goal-y_real), 2))

    return euclidean_dist

# Callback function for the robot position.


def odom_callback(data):

    global curr_x
    global curr_y

    curr_x = data.pose.pose.position.x
    curr_y = data.pose.pose.position.y

# Callback function for the target position.
# It computes the velocity to send to the cmd_vel topic, by considering an omniwheel robot.
# when the robot has arrived at desired position, publishes vel=0 and sets the "arrived" and
# current robot position parameters.


def traj_callback(data):

    global curr_x
    global curr_y
    global number

    target_pos = data.data
    target_x = target_pos[0]
    target_y = target_pos[1]

    while EuclidianDistance(target_x, target_y, curr_x, curr_y) >= 0.001:

        # omniwheel robot
        vel.linear.x = (target_x-curr_x)
        vel.linear.y = (target_y-curr_y)

        # Publish
        pub.publish(vel)

    # omniwheel robot
    vel.linear.x = 0
    vel.linear.y = 0

    # Publish
    pub.publish(vel)

    # Set command parameter
    rospy.set_param('all', [target_x, target_y, curr_x, curr_y, number])
    rospy.set_param('arrived', 1)

    number = number+1

    time.sleep(2)

# Ros node that subscribes to the target_pos and odom topic and publishes on the cmd_vel topic.


def robot_motion_controller():

    rospy.init_node('robot_motion_controlller', anonymous=True)

    rospy.Subscriber("target_pos", Int64MultiArray, traj_callback)

    rospy.Subscriber('odom', Odometry, odom_callback)

    rospy.spin()

    pass


if __name__ == '__main__':
    robot_motion_controller()
