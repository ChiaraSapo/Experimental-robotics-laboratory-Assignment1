#!/usr/bin/env python

import roslib
import rospy
import time


def printer():
    """!
    Prints the important parameters as loginfo: state, command, robot position
    """
    s = x = -1  # y not needed, comes together with x
    rospy.init_node('printer')

    while not rospy.is_shutdown():
        # Loginfo about state
        if rospy.has_param('state'):
            state = rospy.get_param('state')
            if state != s:
                rospy.loginfo('-->The current state is: %s', state)
                s = state

        # Loginfo about command and position
        if rospy.has_param('all'):
            all = rospy.get_param('all')
            state = rospy.get_param('state')
            if state != s:
                rospy.loginfo('-->The current state is: %s', state)
                s = state
            if all[4] != x:
                stringc = "Command was to go to %d %d" % (all[0], all[1])
                rospy.loginfo('%s', stringc)
                stringd = "Miro has arrived in %d %d" % (
                    round(all[2]), round(all[3]))
                rospy.loginfo('%s', stringd)
                x = all[4]


if __name__ == '__main__':
    try:
        printer()
    except rospy.ROSInterruptException:
        pass
