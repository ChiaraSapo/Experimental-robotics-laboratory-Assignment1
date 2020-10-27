#!/usr/bin/python2.7

# if "play" or "hey buddy":
#   output = request_to_play
# elseif "go to _number1 _number2"
#   output = "go to _number1 _number2"
# sends output in output

import random
from Exp_lab_assignments.srv import mic_on
import rospy


def user_says():
    var = random.choice(['go to 5 4', 'go to 3 7', 'hey buddy', 'play'])
    return var


def dialog_manager():
    woord_command = user_says()
    if word_command == 'hey buddy' or word_command == 'play':
        output = 'request_to_play'
    elif 'go' in word_command and 'to' in word_command:
        check_int = [int(s) for s in word_command.split() if s.isdigit()]
        if len(check_int) == 2:
            output = word_command
        else:
            return 0
    else:
        return 0
    return output


def mic_server():

    rospy.init_node('mic_server')
    s = rospy.Service('mic_server', mic_on, dialog_manager)
    rospy.spin()
    print(c)


if __name__ == "__main__":
    mic_server()
