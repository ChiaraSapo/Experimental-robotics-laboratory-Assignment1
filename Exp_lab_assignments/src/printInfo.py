#!/usr/bin/env python

import roslib
import rospy
import time


def printer():
    """!
    Prints the important parameters as loginfo: state, command, person position, robot position
    """
    s = x = c = p = -1  # y not needed, comes together with x
    rospy.init_node('printer')

    while not rospy.is_shutdown():

        if rospy.has_param('state'):
            state = rospy.get_param('state')
            if state != s:
                rospy.loginfo('-->The current state is: %s', state)
                s = state

        # if rospy.has_param('person_posx'):
        #     per_x = rospy.get_param('person_posx')
        #     per_y = rospy.get_param('person_posy')
        #     if per_x != p:
        #         rospy.loginfo(
        #             'The current person position is: %d %d', per_x, per_y)
        #         p = per_x

        if rospy.has_param('command'):
            command = rospy.get_param('command')
            # assumption: if go rand: prints once
            if command != c:
                rospy.loginfo(
                    'The received command is: %s', command)
                c = command
            if rospy.has_param('current_posx') and rospy.has_param('arrived'):
                if rospy.get_param('arrived') == 1:
                    curr_x = rospy.get_param('current_posx')
                    curr_y = rospy.get_param('current_posy')
                    if curr_x != x:
                        rospy.loginfo('The robot has just arrived in: %d %d',
                                      curr_x, curr_y)
                        x = curr_x


if __name__ == '__main__':
    try:
        printer()
    except rospy.ROSInterruptException:
        pass
