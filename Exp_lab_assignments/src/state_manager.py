#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String
import matplotlib.pyplot as plt

# INSTALLATION
# - move this file to the 'ML_ass/scr' folder and give running permissions to it with
#          $ chmod +x state_manager.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun ML_ass state_manager.py
# - install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py

pub = rospy.Publisher('command', String, queue_size=10)


class MIRO_Sleep(smach.State):
    # send go_home to geometry grounding
    # wait for goto_finished from robot motion controller
    # wait 10 sec -> exit

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        sleep_command = 'go_home'
        # publish(sleep_command)
        # request a goto_finished
        # time.sleep(10)
        print('S')
        pub.publish(sleep_command)
        time.sleep(6)

        c = 'normal_command'
        return c


class MIRO_Normal(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['sleep_command', 'play_command'])

    def execute(self, userdata):
        # Loop:
        # request_to_play? from dialog manager
        #   if yes return it and exit.
        #   else:
        #       send go_rand to geometry grounding
        #       wait for goto_finished from robot motion controller
        #       wait 5 sec
        normal_command = 'go_rand'
        pub.publish(normal_command)
        time.sleep(6)

        print('N')
        c = random.choice(['sleep_command', 'play_command'])
        return c


class MIRO_Play(smach.State):
    # while(playful):
    # request_to_go? from dialog manager
    # wait 5 sec for responce
    # if no responce
    #   playful=0
    # else:
    #   send person_and_gesture to geometry grounding

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        play_command = random.choice(
            ['go to 5 4', 'go to 3 7', 'go to 5 9', 'go to 6 3', 'go to 9 6'])
        pub.publish(play_command)
        time.sleep(6)
        print('P')
        c = 'normal_command'
        return c


def main():
    rospy.init_node('state_manager')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEP', MIRO_Sleep(),
                               transitions={'normal_command': 'NORMAL'})
        smach.StateMachine.add('NORMAL', MIRO_Normal(),
                               transitions={'sleep_command': 'SLEEP',
                                            'play_command': 'PLAY'})
        smach.StateMachine.add('PLAY', MIRO_Play(),
                               transitions={'normal_command': 'NORMAL'})

    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
