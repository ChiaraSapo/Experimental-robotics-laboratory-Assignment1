#!/usr/bin/python2.7

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
# takes as input the trajectory
# waits 5 seconds
# sends goto_finished

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


curr_x = 0
curr_y = 0
theta = 0


def EuclidianDistance(x_goal, y_goal, x_real, y_real):
    return math.sqrt(math.pow((x_goal-x_real), 2) +
                     math.pow((y_goal-y_real), 2))


def odom_callback(data):
    global curr_x
    global curr_y
    global theta
    curr_x = data.pose.pose.position.x
    curr_y = data.pose.pose.position.y

    rot_q = data.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])


def traj_callback(data):
    global curr_x
    global curr_y
    global theta

    target_pos = data.data
    target_x = target_pos[0]
    target_y = target_pos[1]

    vel = Twist()
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 0

    rospy.logerr('I want to go to %d %d', target_x, target_y)

    while EuclidianDistance(target_x, target_y, curr_x, curr_y) >= 0.2:

        rospy.Subscriber('odom', Odometry, odom_callback)
        rospy.logerr('I see we are in %f %f', curr_x, curr_y)

        # omni
        vel.linear.x = (target_x-curr_x)
        vel.linear.y = (target_y-curr_y)

        # diff
        #vel.linear.x = EuclidianDistance(target_x, target_y, curr_x, curr_y)
        #vel.angular.z = theta

        pub.publish(vel)

    # omni
    vel.linear.x = 0
    vel.linear.y = 0

    # diff
    #vel.linear.x = 0
    #vel.angular.z = 0

    pub.publish(vel)
    time.sleep(2)



def robot_motion_controller():

    rospy.init_node('robot_motion_controlller', anonymous=True)

    rospy.Subscriber("target_pos", Int64MultiArray, traj_callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    robot_motion_controller()
