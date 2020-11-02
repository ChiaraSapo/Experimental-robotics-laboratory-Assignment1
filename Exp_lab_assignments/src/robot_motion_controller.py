#!/usr/bin/python2.7

import numpy as np
import random
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import Int64MultiArray
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
vel = Twist()

curr_x = 0
curr_y = 0
theta = 0


def EuclidianDistance(x_goal, y_goal, x_real, y_real):
    return math.sqrt(math.pow((x_goal-x_real), 2) +
                     math.pow((y_goal-y_real), 2))


# def show_grid(target_x, target_y):

#     fig = plt.figure()
#     plt.axis([0, 10, 0, 10])
#     plt.xticks(np.arange(0, 10))
#     plt.yticks(np.arange(0, 10))

#     rospy.logerr(target_x)
#     rospy.logerr(target_y)

#     plt.scatter(target_x, target_y, c=cm.hot(np.arange(0, len(target_x))))
#     plt.text(4, 4, 'home')
#     target_x = np.array(target_x)
#     target_y = np.array(target_y)
#     plt.text(target_x[0], target_y[0], 'start')
#     plt.text(target_x[len(target_x)-1], target_y[len(target_y)-1], 'end')
#     plt.grid()

#     plt.show(block=False)
#     plt.pause(4)
#     plt.close()


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

    target_pos = data.data
    target_x = target_pos[0]
    target_y = target_pos[1]
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 0

    while EuclidianDistance(target_x, target_y, curr_x, curr_y) >= 0.2:

        rospy.Subscriber('base_pose_ground_truth', Odometry, odom_callback)

        vel.linear.x = (target_x-curr_x)
        vel.linear.y = (target_y-curr_y)
        #vel.linear.x = EuclidianDistance(target_x, target_y, curr_x, curr_y)
        #vel.angular.z = theta
        pub.publish(vel)

    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(1)

    # while curr_x != target_x:
    #     vel.linear.x = (target_x - curr_x)/abs(target_x - curr_x)
    #     vel.linear.y = 0
    #     pub.publish(vel)

    # while curr_y != target_y:
    #     vel.linear.y = (target_y - curr_y)/abs(target_y - curr_y)
    #     vel.linear.x = 0
    #     pub.publish(vel)

    rospy.set_param('current_posx', curr_x)
    rospy.set_param('current_posy', curr_y)
    rospy.set_param('arrived', 1)
    rospy.logerr('current pos %f %f:', curr_x, curr_y)

    # show_grid(target_x, target_y)


def robot_motion_controller():

    rospy.init_node('robot_motion_controlller', anonymous=True)

    rospy.Subscriber("target_pos", Int64MultiArray, traj_callback)

    rospy.spin()
    pass


if __name__ == '__main__':
    robot_motion_controller()
