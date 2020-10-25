#!/usr/bin/python2.7

import numpy as np
import random

# takes as input a signal go_home, go_rand, 'go to n1 n2'
# translates signals in (x_target, y_target)
# sends in output (x_target, y_target)


class pos_command:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def add_data(self, x, y):
        self.x = x
        self.y = y


def geometry_grounding(upos_command):
    if upos_command.name == 'go_home':
        output = (4, 4)
    elif upos_command.name == 'go_rand':
        output = (random.randrange(10), random.randrange(10))
    elif upos_command.name == 'go_to':
        output = (upos_command.x, upos_command.y)

    return output


def main():
    # to be done in different node and passed as msg
    #str = 'go_home'
    #str = 'go_rand'
    str = 'go to 1 2'
    current_pos = [0, 0]

    my_command = [int(s) for s in str.split() if s.isdigit()]
    if my_command:  # check was made in previous step
        str = my_command
        upos_command = pos_command('go_to')
        upos_command.add_data(my_command[0], my_command[1])

    else:
        upos_command = pos_command(str)

    target_pos = geometry_grounding(upos_command)
    print(pos)
    # then send current_pos as target_pos msg
    pass


if __name__ == "__main__":
    main()
