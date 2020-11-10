#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String
import matplotlib.pyplot as plt
import numpy as np

pub = rospy.Publisher('command', String, queue_size=10)

LOOPS = 3


class coordinates_from_picture:
    '''
    Simulates a camera frame and the information it contains.
    '''

    def __init__(self, name):
        '''
        Init function for coordinates_from_picture class.
        '''
        self.person_posx = 0
        self.person_posy = 0
        self.gesture_posx = 0
        self.gesture_posx = 0

    def add_data(self, img_person_posx, img_person_posy, img_gesture_posx, img_gesture_posy):
        '''
        Add data function for coordinates_from_picture class.
        '''
        self.person_posx = img_person_posx
        self.person_posy = img_person_posy
        self.gesture_posx = img_gesture_posx
        self.gesture_posy = img_gesture_posy


def user_says(stateCalling):
    """!
    Simulates the user's voice commands. 
    @param stateCalling: which state the robot is in
    @return userVoice: user command
    """

    # to test the code: give input. The user will never say
    # # play in play or go to to in normal:
    # done to save time in testing phase

    comm = "go to %d %d" % (random.randrange(0, 11), random.randrange(0, 11))
    if stateCalling == 0:  # normal
        userVoice = random.choice(['play', '', 'hey buddy'])
    if stateCalling == 1:  # play
        userVoice = comm
    return userVoice


def user_does():
    """!
    Simulates the user's voice position and gesture. 
    @return userBody: user position and gesture
    """
    userBody = coordinates_from_picture('img1')
    person_posx = random.randrange(0, 11)
    person_posy = random.randrange(0, 11)
    gesture_posx = random.randrange(0, 11)
    gesture_posy = random.randrange(0, 11)
    userBody = np.array([person_posx, person_posy, gesture_posx,
                         gesture_posy])

    return userBody


class MIRO_Sleep(smach.State):
    '''
    Sleep state of the smach machine.
    '''

    def __init__(self):
        '''
        Init function for smach machine sleep state.
        '''
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        """!
        Smach machine state sleep actions: 
        Publishes "go home" command, waits ("sleeps") and outputs command to enter normal state
        @return c: command to switch between states.
        """

        # Set state parameter
        rospy.set_param('state', 'SLEEP STATE')

        while rospy.get_param('arrived') == 0:
            time.sleep(1)

        # Give command home
        sleep_command = 'go_home'
        # time.sleep(3)
        rospy.set_param('arrived', 0)

        # Publish sleep command
        pub.publish(sleep_command)
        time.sleep(4)

        # Change state
        c = 'normal_command'
        return c


class MIRO_Normal(smach.State):
    '''
    Normal state of the smach machine.
    '''

    def __init__(self):
        '''
        Init function for smach machine normal state.
        '''
        smach.State.__init__(self,
                             outcomes=['sleep_command', 'play_command'])

    def execute(self, userdata):
        """!
        Smach machine state normal actions: 
        Listens to user: if user says "Play" or "Hey buddy" it outputs command to enter play state.
        If user says nothing, it goes to random positions for a while (n loops) then outputs command to enter sleep state.
        @return c: command to switch between states.
        """

        # Set state parameter
        rospy.set_param('state', 'NORMAL')

        for i in range(0, LOOPS):

            # Checks if user is speaking
            user_command = user_says(0)

            # If user is calling MIRO, enter play state
            if user_command == 'hey buddy' or user_command == 'play':
                c = 'play_command'
                return c

            # Else wander around
            else:
                while rospy.get_param('arrived') == 0:
                    time.sleep(1)

                normal_command = 'go_rand'

                # time.sleep(3)
                rospy.set_param('arrived', 0)
                # Publish sleep command
                pub.publish(normal_command)
                time.sleep(3)

            # Randomly decide to sleep, enter sleep state
            if random.randrange(0, 5) == 1:
                c = 'sleep_command'
                return c

        return 'sleep_command'


class MIRO_Play(smach.State):
    '''
    Play state of the smach machine.
    '''

    def __init__(self):
        '''
        Init function for smach machine play state.
        '''
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        """!
        Smach machine state play actions: 
        Looks at user, saves his coordinates as next position, publishes them (goes toward the human).
        It then listens to the user. If user says "go to posx posy", publishes the coordinates (goes to the point).
        If user says "Hey buddy" or "Play" it waits. If user says nothing, it looks for the user gesture to go somewhere, 
        and publishes the coordinate he receives (goes to the point).
        This repeates for a while (n loops) then the robot enters normal state again.
        @return c: command to switch between states.
        """

        # Set state parameter
        rospy.set_param('state', 'PLAY STATE')

        for i in range(0, LOOPS):

            # Check where user is (assumption:he is there, since he called MIRO)
            user_camera = user_does()
            # Save user position
            user_position = "go to %d %d" % (
                user_camera[0], user_camera[1])

            while rospy.get_param('arrived') == 0:
                time.sleep(1)

            rospy.set_param('arrived', 0)
            # Go to user
            pub.publish(user_position)
            time.sleep(3)

            # Listen to user
            user_command = user_says(1)

            # If user says to go somewhere...
            if 'go' in user_command and 'to' in user_command:
                check_int = [int(s)
                             for s in user_command.split() if s.isdigit()]
                # ... and he actually gives you two coordinates...

                if len(check_int) != 2:
                    rospy.logerr('Wrong command')
                    break

                while rospy.get_param('arrived') == 0:
                    time.sleep(1)

                rospy.set_param('arrived', 0)

                # ...Go to position
                pub.publish(user_command)
                time.sleep(3)

            # If user says he wants to play: wait
            elif user_command == 'hey buddy' or user_command == 'play':
                time.sleep(2)

            # If user sayes nothing
            else:
                # Look at user gesture
                user_gesture = user_does()
                user_command = "go to %d %d" % (
                    user_camera.gesture_posx, user_camera.gesture_posy)

                while rospy.get_param('arrived') == 0:
                    time.sleep(1)
                rospy.set_param('arrived', 0)
                # Go to position
                pub.publish(user_command)
                time.sleep(3)

        c = 'normal_command'
        return c


def main():
    """!
    Ros node that implements a state machine with three states: sleep, play, normal.
    It also initializes the home postion and the arrival parameters.
    """

    rospy.init_node('state_manager')

    # Set parameters
    # home pos
    rospy.set_param('home_posx', 3)
    rospy.set_param('home_posy', 3)

    rospy.set_param('arrived', 1)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])

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
