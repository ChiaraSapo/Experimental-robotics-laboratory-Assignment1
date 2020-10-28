#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String
import matplotlib.pyplot as plt

# random.choice(['go to 5 4', 'go to 3 7', 'go to 5 9', 'go to 6 3', 'go to 9 6'])

# to test the code: give input. then REMOVE IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def user_says(blabla):
    # var = random.choice(['go to 3 7', 'play', ''])
    if blabla == 0:
        var = 'play'
    if blabla == 1:
        var = random.choice(['go to 3 3', ''])
    return var

# INSTALLATION
# - move this file to the 'ML_ass/scr' folder and give running permissions to it with
#          $ chmod +x state_manager.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun ML_ass state_manager.py
# - install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py


class coordinates_from_picture:
    def __init__(self, name):
        self.person_posx = 0
        self.person_posy = 0
        self.gesture_posx = 0
        self.gesture_posx = 0

    def add_data(self, img_person_posx, img_person_posy, img_gesture_posx, img_gesture_posy):
        self.person_posx = img_person_posx
        self.person_posy = img_person_posy
        self.gesture_posx = img_gesture_posx
        self.gesture_posy = img_gesture_posy


def user_does():
    output = coordinates_from_picture('img1')
    person_posx = random.randrange(0, 11)
    person_posy = random.randrange(0, 11)
    gesture_posx = random.randrange(0, 11)
    gesture_posy = random.randrange(0, 11)
    output.add_data(person_posx, person_posy, gesture_posx, gesture_posy)
    return output


pub = rospy.Publisher('command', String, queue_size=10)


class MIRO_Sleep(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):

        sleep_command = 'go_home'
        pub.publish(sleep_command)
        # request a goto_finished
        time.sleep(6)

        c = 'normal_command'
        return c


class MIRO_Normal(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['sleep_command', 'play_command'])

    def execute(self, userdata):
        for i in range(0, 3):
            user_command = user_says(0)
            if user_command == 'hey buddy' or user_command == 'play':
                c = 'play_command'
                return c
            else:
                normal_command = 'go_rand'
                pub.publish(normal_command)
                # request goto_finished
                time.sleep(5)
                if random.randrange(0, 5) == 1:
                    c = 'sleep_command'
                    return c
        return 'sleep_command'


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
        user_camera = user_does()
        user_position = "go to %d %d" % (
            user_camera.person_posx, user_camera.person_posy)
        for i in range(0, 4):
            pub.publish(user_position)
            # wait goto_finish
            time.sleep(5)
            user_command = user_says(1)
            if 'go' in user_command and 'to' in user_command:
                check_int = [int(s)
                             for s in user_command.split() if s.isdigit()]
                if len(check_int) != 2:
                    print('error')  # .......
                pub.publish(user_command)
                time.sleep(6)
            elif user_command == 'hey buddy' or user_command == 'play':
                time.sleep(2)
            else:
                user_gesture = user_does()
                user_command = "go to %d %d" % (
                    user_camera.gesture_posx, user_camera.gesture_posy)
                pub.publish(user_command)
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
