#!/usr/bin/python2.7

import numpy as np

# takes as input the next position to reach (x_target, y_target)
# calulates trajectory
# sends trajectory as output


def main():
    # receive target_pos and current_pos
    target_pos = [4, 4]
    current_pos = [6, 5]

    target_x = target_pos[0]
    target_y = target_pos[1]
    current_x = current_pos[0]
    current_y = current_pos[1]

    next_x = []
    next_y = []

    while current_x != target_x:
        current_x = current_x+(target_x - current_x)/abs(target_x - current_x)
        next_x.append(current_x)
        next_y.append(current_y)

    while current_y != target_y:
        current_y = current_y+(target_y - current_y)/abs(target_y - current_y)
        next_x.append(current_x)
        next_y.append(current_y)
    
    trajectory = np.array([next_x, next_y])
    print(trajectory)
    # send (next_x, next_y)

    pass


if __name__ == "__main__":
    main()
