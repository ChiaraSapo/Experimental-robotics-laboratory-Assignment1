#!/usr/bin/python2.7

import numpy as np
import random

# takes as input a raw RGB image
# analyzes it to find person and gesture
# outputs person_and_gesture


class coordinates_from_picture:
    def __init__(self, name):
        self.person_pos = [0, 0]
        self.gesture_pos = [0, 0]

    def add_data(self, img_person_pos, img_gesture_pos):
        self.person_pos = img_person_pos
        self.gesture_pos = img_gesture_pos


def user_does():
    output = coordinates_from_picture('img1')
    person_pos = [random.randrange(0, 11), random.randrange(0, 11)]
    gesture_pos = [random.randrange(0, 11), random.randrange(0, 11)]
    output.add_data(person_pos, gesture_pos)
    return output


def main():
    c = user_does()
    print(c.gesture_pos)


if __name__ == "__main__":
    main()
