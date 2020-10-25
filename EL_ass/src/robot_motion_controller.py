#!/usr/bin/python2.7

import numpy as np
import random
import matplotlib.pyplot as plt
import time


# takes as input the trajectory
# waits 5 seconds
# sends goto_finished


def show_grid(pos_x, pos_y):
    fig = plt.figure()
    plt.axis([0, 10, 0, 10])
    plt.xticks(np.arange(0, 10))
    plt.yticks(np.arange(0, 10))

    plt.scatter(pos_x, pos_y)
    plt.grid()
    plt.show()


def main():
    # receive this as msgs
    trajectory = np.array([[1, 2, 3], [2, 4, 6]])

    # ... actuate motors...
    time.sleep(2)

    current_pos = trajectory[:, -1]

    # plot
    pos_x = trajectory[0, :]
    pos_y = trajectory[1, :]

    show_grid(pos_x, pos_y)

    # send goto_finished, current_pos

    pass


if __name__ == "__main__":
    main()
