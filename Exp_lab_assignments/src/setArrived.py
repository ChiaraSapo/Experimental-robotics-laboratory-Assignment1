#!/usr/bin/python2.7

import numpy as np
import random
import matplotlib.pyplot as plt
import time
import rospy
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Bool

pub_arr = rospy.Publisher('/arrived', Bool, queue_size=10)



def robot_motion_controller():

    rospy.init_node('setArrived', anonymous=True)

    pub_arr.publish(1)

    rospy.spin()
    pass


if __name__ == '__main__':
    robot_motion_controller()

