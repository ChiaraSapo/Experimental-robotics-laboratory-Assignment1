#!/usr/bin/env python

import roslib
import rospy
import time


def printer():
    s = x = c = p = -1  # y not needed, comes together with x
    rospy.init_node('printer')
    while not rospy.is_shutdown():

        if rospy.has_param('state'):
            state = rospy.get_param('state')
            if state != s:
                rospy.logwarn('The current state is: %s', state)
                s = state

        if rospy.has_param('person_posx'):
            per_x = rospy.get_param('person_posx')
            per_y = rospy.get_param('person_posy')
            if per_x != p:
                rospy.logwarn(
                    'The current person position is: %d %d', per_x, per_y)
                p = per_x

        if rospy.has_param('command'):
            command = rospy.get_param('command')
            # assumption: if go rand: prints once
            if command != c:
                rospy.logwarn(
                    'The user command is: %s', command)
                c = command

        if rospy.has_param('arrived'):
            if rospy.get_param('arrived') == 1:
                curr_x = rospy.get_param('current_posx')
                curr_y = rospy.get_param('current_posy')
                if curr_x != x:
                    rospy.logwarn('The robot has just arrived in: %d %d',
                                  curr_x, curr_y)
                    x = curr_x

            # rospy.logwarn(rospy.get_param('arrived'))


if __name__ == '__main__':
    try:
        printer()
    except rospy.ROSInterruptException:
        pass
