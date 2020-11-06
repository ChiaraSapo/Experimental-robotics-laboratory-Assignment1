#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String
import matplotlib.pyplot as plt


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


def user_says(stateCalling):
    """!
    Simulates the user's voice commands. 
    @param stateCalling: which state the robot is in
    @return userVoice: user command
    """
    # to test the code: give input. The user will never say
    # # play in play or go to to in normal:
    # done to save time in testing phase!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #userVoice = random.choice(['go to 3 7', 'play', ''])
    if stateCalling == 0:  # normal
        userVoice = random.choice(['play', ''])
    if stateCalling == 1:  # play
        userVoice = random.choice(['go to 5 5', 'go to 7 7' ''])  # odd to test
    return userVoice


def user_does():
    """!
    Simulates the user's voice position and gesture. 
    @return userBody: user position and gesture
    """
    userBody = coordinates_from_picture('img1')
    # person_posx = random.randrange(0, 11)
    # person_posy = random.randrange(0, 11)
    # gesture_posx = random.randrange(0, 11)
    # gesture_posy = random.randrange(0, 11)
    person_posx = 2
    person_posy = 2
    gesture_posx = 4
    gesture_posy = 4
    userBody.add_data(person_posx, person_posy, gesture_posx,
                      gesture_posy)                                    # even to test
    #userBody.add_data(5, 5, 5, 5)
    return userBody


pub = rospy.Publisher('command', String, queue_size=10)


class MIRO_Sleep(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        """!
        Smach machine state sleep: 
        Publishes "go home" command, waits ("sleeps") and outputs command to enter normal state
        @return c: command to switch between states.
        """
        rospy.loginfo('---> The current state is: %s', 'Sleep')
        # Set state parameter
        rospy.set_param('state', 'SLEEP STATE')
        # Give command home
        sleep_command = 'go_home'
        time.sleep(3)

        # Set command parameter
        rospy.set_param('command', sleep_command)
        time.sleep(3)

        # Publish sleep command
        pub.publish(sleep_command)

        time.sleep(6)

        # Change state
        c = 'normal_command'
        return c


class MIRO_Normal(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['sleep_command', 'play_command'])

    def execute(self, userdata):
        """!
        Smach machine state normal: 
        Listens to user: if user says "Play" or "Hey buddy" it outputs command to enter play state.
        If user says nothing, it goes to random positions for a while (5 loops) then outputs command to enter sleep state.
        @return c: command to switch between states.
        """
        rospy.loginfo('---> The current state is: %s', 'Normal')

        # Set state parameter
        rospy.set_param('state', 'NORMAL')

        for i in range(0, 5):
            # Checks if user is speaking
            user_command = user_says(0)
            # If user is calling MIRO, enter play state
            if user_command == 'hey buddy' or user_command == 'play':
                rospy.loginfo(
                    'The command is: %s', 'Pass from normal to Play command')
                c = 'play_command'
                return c

            # Else wander around
            else:
                normal_command = 'go_rand'
                time.sleep(3)
                # Set command parameter
                rospy.set_param('command', normal_command)
                rospy.loginfo(
                    'The command is: %s', normal_command)
                time.sleep(3)
                # Publish sleep command
                pub.publish(normal_command)

                time.sleep(3)

                # Randomly decide to sleep, enter sleep state
            if random.randrange(0, 5) == 1:
                c = 'sleep_command'
                return c
        return 'sleep_command'


class MIRO_Play(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['normal_command'])

    def execute(self, userdata):
        """!
        Smach machine state play: 
        Looks at user, saves his coordinates as next position, publishes them (goes toward the human).
        It then listens to the user. If user says "go to posx posy", publishes the coordinates (goes to the point).
        If user says "Hey buddy" or "Play" it waits. If user says nothing, it looks for the user gesture to go somewhere, 
        and publishes the coordinate he receives (goes to the point).
        This repeates for a while (5 loops) then the robot enters normal state again.
        @return c: command to switch between states.
        """
        rospy.loginfo('---> The current state is: %s', 'Play')
        # Set state parameter
        rospy.set_param('state', 'PLAY STATE')

        for i in range(0, 5):

            # Check where user is (assumption:he is there, since he called MIRO)
            user_camera = user_does()
            # Save user position
            user_position = "go to %d %d" % (
                user_camera.person_posx, user_camera.person_posy)

            # Set user position parameter
            #rospy.set_param('person_posx', user_camera.person_posx)
            #rospy.set_param('person_posy', user_camera.person_posy)

            # Set command parameter
            time.sleep(3)
            rospy.set_param('command', user_position)
            rospy.loginfo(
                'The current person position is: %d %d', user_camera.person_posx, user_camera.person_posy)
            rospy.loginfo(
                'So the command is: %s', user_position)
            time.sleep(3)
            # Go to user
            pub.publish(user_position)

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
                # Set command parameter
                time.sleep(3)
                rospy.loginfo(
                    'The command is: %s', user_command)
                rospy.set_param('command', user_command)
                time.sleep(3)
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

                # Set command parameter
                time.sleep(3)
                rospy.set_param('command', user_command)
                rospy.loginfo(
                    'The command is: %s', user_command)
                # Go to position
                pub.publish(user_command)

                time.sleep(3)

        c = 'normal_command'
        return c


def main():
    rospy.init_node('state_manager')

    # Set parameters
    # init current pos
    rospy.set_param('current_posx', 0)
    rospy.set_param('current_posy', 0)
    # home pos
    rospy.set_param('home_posx', 3)
    rospy.set_param('home_posy', 3)

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
