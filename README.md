# Experimental robotics laboratory Assignments

## Introduction
The package Exp_Lab_Assignments simulates a robot dog (hypothetically MIRo) moving on a gridded plane. He can either sleep in his kennel, wander around or play with a simulated user. In order to play with the robot, the user has to say "Hey buddy" or "Play". If he says so, the dog approaches the person and waits for a command such as "go to 1 2", or for a pointing gesture towars a direction. It then goes to the desired location and comes back. After a while it again starts wandering around around. 
The project is implemented with a ROS structure, written in Python, and simulated through the ROS stage platform.

## Software architecture and state diagrams
The architecture is composed of four nodes:
- State manager
- Geometry grounding
- Robot motion controller
- Print Info
The nodes are described in the next section of the readme.

### State_manager:

This node publishes on the command topic. It has a finite state machine composed of three different states:

<p align="center">
  <img height="500" width="500" src="https://github.com/ChiaraSapo/Experimental-robotics-laboratory-Assignments/blob/master/Exp_lab_assignments/images/Screenshot%20from%202020-10-29%2008-36-49.png?raw=true "Title"">
</p>

The states are hereby described:
- SLEEP: The state publishes the "go home" command, waits a few seconds to simulate the robots's nap, then outputs the "normal command" to transition to the normal state.
- NORMAL: The state enters a loop. It listens to the user: 
    - if the user says "Hey buddy" or "Play", it outputs the "play command" to transition to the play state. 
    - If the user says nothing, the state publishes the command "go rand" and waits a few seconds to wait for the execution of the command. 
It could also randomly send the "sleep command" to transition to sleep state, in case the dig feels sleepy. At the end of the loop the state outputs the "sleep command".
- PLAY: The state enters a loop. At each iteration it first goes to the user (i.e. looks at the user to save his/her position and ppublishes the coordinates). Then it listens to the user: 
  - if the user says "Go to posx posy" (where posx and posy are two random x and y positions inside the grid where the dog moves), this command is published. 
  - if the user again says "Hey buddy" or "Play", the robot waits. 
  - if the user says nothing, the dog looks at his gestures and publishes the position indicated by the user hand. 

At the end of the loop, the "normal command" is set as output of the stata.
The user action is simulated through two functions: "user says" and "user does", respectively implementing speech commands and postion/gesture commands.


### Geometry_grounding:

It subscribes to the "command" topic and analyzes the the command it receives: 
- if it is a "go to posx posy" command, it estrapolates the coordinates from the command string 
- if it is a "go home" command, it sets the home coordinates, which are saved in the ros parameter server.
- if it is a "go rand" command, it computes random coordinates.
It publishes the coordinates on the "target pos" topic.


### Robot motion controller:

It subscribes to the "odom" topic from stage and to the "target_pos" topic. It calculates the successive positions of the robot from the current to the next postion. It then publishes the velocity on the "cmd_vel" topic of stage.


### Print info:
Prints the package parameters on terminal through loginfo.


## Messages and parameters
The messages that are sent between the nodes are of two different types: 
- string for command topic
- Int64MultiArray for target_pos and trajectory topics

The parameters used are:
- state, which indicates the current state. It is set by the state manager
- arrived, which indicates the availability of the robot to go to a new position. It is set in the launch file as 1 (available). Before publishing new target positions, the code always checks availability, waits until arrived=1 and then sets it back to arrived=0 and publishes the position.
- all, which comprehends current_posx and current_posy, which represents the current position of the robot, and command, whcih represents the successive positions the robot needs to go to, which may be new commands or the person position. It is initialized by the state manager and updated by the robot_motion_controller. 

All the parameters, are printed on screen by the printInfo node.

## The simulator
To simulate the dog I used ROS stage. This simulator allows to represent a robot (here it is just a simple green square) that moves on a grid. 

<p align="center">
  <img height="400"  src="https://github.com/ChiaraSapo/Experimental-robotics-laboratory-Assignments/blob/master/Exp_lab_assignments/images/Screenshot%20from%202020-11-11%2008-43-27.png?raw=true "Title"">
</p>

Specifications about robot position, appearance and mobility are specified in world/MIRO.world file. Here, for simplicity, I chose to let the robot have initial position in the origin, appear as a small green square and move as an omniwheel robot.  

## How to run the code:
Download the package in your_catkin_ws/src folder.
```sh
cd "Your catkin workspace"/src/Exp_Lab_Assignments
./Ass1.sh
```
This will install the package, and all the useful launch files and nodes will be started.

## Working hypoteses
The user: 
- In order to play, the user must first call the robot by saying "Hey buddy" or "Play". Notice: I did not implement more complex commands since I don't know the level of confidence at which the robot should human speech. I just chose a few simple words in order to increase the probability for the dog to hear them correctly.
- The desired location can be given by voice or by hand gesture. The robot first listens, then looks at the gesture, so the priority is given to speech commands.

The robot:
- Since a simple stage simulator was used, I considered the robot as an omniwheel one. In order to implement this project on a real robot, this fact should be taken into consideration. However, MIRO.world and robot_motion_controller.py are the only files that should be changed in order to have, for example, a differential drive robot.
- The robot usually wanders around if nothing happens and, after a certain time (a number n of loops), it goes to sleep, in order to simulate the sleep wake cycle. However, it could also feel sleepy at random moments and go to the sleep.
- During play phase, the robot first approaches the human, goes to the position, comes back and so on. After a certain time (a number m of loops) it feels tired and goes back to wandering. However, it could also feel tired at random moments of the play phase and stop playing before the time is finished. The probability that this happens is half the one that this happens in normal state, since play time is supposedly engaging.

The grid:
- The grid on which the robot moves is limited to 10x10 on the code
- The human can move in the same grid, and has the same location limitations as the robot.
- The kennel's position is fixed in position 3,3.
- The initial position is fixed in position 0,0.

## System's limitations
- Sometimes the node that prints
- The code supports few user commands and understands "go to 1 2" but wouldn't understand "go to one two" for example.
- The user can't interface with the robot via shell, for example, since commands are pre defined inside the code.
- The grid is limited.
- The simulator is very simple and assumes an omniwheel robot.

## Authors
Chiara Saporetti: chiara.saporetti@gmail.com
