#!/usr/bin/python2.7

# if "play" or "hey buddy":
#   output = request_to_play
# elseif "go to _number1 _number2"
#   output = "go to _number1 _number2"
# sends output in output

import random


def user_says():
    var = random.randrange(1, 4)
    var = 1
    if var == 1:
        str = 'go to 1 2'
    elif var == 2:
        str = 'hey buddy'
    elif var == 3:
        str = 'play'
    return str


def dialog_manager(word_command):
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


def main():
    rvar = random.randrange(0, 2)
    if rvar == 0:
        str = user_says()
        c = dialog_manager(str)
        print(c)
    pass


if __name__ == "__main__":
    main()
