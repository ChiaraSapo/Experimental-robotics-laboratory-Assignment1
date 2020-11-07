# Experimental robotics laboratory Assignments

## Introduction
The package Exp_Lab_Assignments simulates a robot dog (hypothetically MIRo) moving on a gridded plane. He can either sleep in his kennel, wander around or play with a simulated user. In order to play with the robot, the user has to say "Hey buddy" or "Play". If he says so, the dog approaches the person and waits for a command such as "go to 1 2", or for a pointing gesture towars a direction. It then goes to the desired location and comes back. After a while it again starts wandering around around. 
The project is implemented with a ROS structure and written in Python.

## Software architecture and state diagrams
The architecture is composed of five nodes:
- State manager
- Geometry grounding
- Planner
- Robot motion controller
- Print Info
The nodes are described in the following part of the readme.

### State_manager:

This node publishes on the command topic. It has a finite state machine composed of three different states:

<p align="center">
  <img height="500" width="500" src="https://github.com/ChiaraSapo/Experimental-robotics-laboratory-Assignments/blob/master/Exp_lab_assignments/images/Screenshot%20from%202020-10-29%2008-36-49.png?raw=true "Title"">
</p>

The states are hereby described:
- SLEEP: The state publishes the "go home" command, waits a few seconds to simulate Miro's nap, then outputs the "normal command" to transition to the normal state.
- NORMAL: The state enters a loop. It listens to the user: 
    - if the user says "Hey buddy" or "Play", it outputs the "play command" to transition to the play state. 
    - If the user says nothing, the state publishes the command "go rand" and waits a few seconds to wait for the execution of the command. 
It could also randomly send the "sleep command" to transition to sleep state, in case Miro feels sleepy. At the end of the loop the state outputs the "sleep command".
- PLAY: The state enters a loop. At each iteration it first goes to the user (i.e. looks at the user to save his/her position and ppublishes the coordinates). Then it listens to the user: 
  - if the user says "Go to posx posy" (where posx and posy are two random x and y positions inside the grid where Miro moves), this command is published. 
  - if the user again says "Hey buddy" or "Play", Miro waits. 
  - if the user says nothing, Miro looks at his gestures and publishes the position indicated by the user hand. 

At the end of the loop, the "normal command" is set as output of the stata.
The user action is simulated through two functions: "user says" and "user does", respectively implementing speech commands and postion/gesture commands.


### Geometry_grounding:

It subscribes to the "command" topic and analyzes the the command it receives: 
- if it is a "go to posx posy" command, it estrapolates the coordinates from the command string 
- if it is a "go home" command, it sets the home coordinates, which are saved in the ros parameter server.
- if it is a "go rand" command, it computes random coordinates.
It publishes the coordinates on the "target pos" topic.

### Planner:

It subscribes to the "target pos" topic and computes a simple trajectory to get from the current position (read from the ros param server) to the target position. It first reaches the x coordinate and then the y coordinate. It publishes the trajectory on the "trajectory" topic.

### Robot motion controller:

It subscribes to the "trajectory" topic and should control the robots actuators in order to make it move. In practice it waits a few seconds, updates the current position and, if the see_plot parameter is set equal to 1, it calls the function to plot the grid and the robot motion.

### Print info:
Prints the package parameters on terminal through loginfo.

## Messages and parameters
The messages that are sent between the nodes are of two different types: 
- string for command topic
- Int64MultiArray for target_pos and trajectory topics

The parameters used are:
- state, which indicates the current state. It is set by the state manager.
- person_posx and person_posy, which indicates the current person position. It is set by the state manager.
- current_posx and current_posy, which represents the current position of the robot. It is initialized by the state manager, read by the planner, and updated by the robot_motion_controller. 
- command, which indicates the current command that MIRo has to follow. It is set by the state manager and by geometry grounding.
- see_plot, which is asked on the terminal before starting the whole package. If set, it allows to see a simple pyplot figure showing the successive robot positions.
All the parameters, except the see_plot, are printed on screen by the printInfo node.

## How to run the code:
Download the package in your_catkin_ws/src.
```sh
cd "Your catkin workspace"/src/Exp_Lab_Assignments
./Ass1.sh
```
This will install the package, then the user will be asked if he/she wants to see the robot trajectory as a simple pyplot figure. Finally all the nodes will be started.

## Working hypoteses
The user: 
- In order to play, the user must first call the robot by saying "Hey buddy" or "Play". Notice: I did not implement more complex commands since I don't know the level of confidence at which the robot understands human speech. I just chose a few simple words in order to increase the probability for the dog to hear them correctly.
- The desired location can be given by voice or by hand gesture. The robot first listens, then looks at the gesture, so the priority is given to speech commands.

The robot:
- The robot usually wanders around if nothing happens and, after a certain time (a number n of loops), it goes to sleep, in order to simulate the sleep wake cycle. However, it could also feel sleepy at random moments and go to the sleep.
- During play phase, the robot first approaches the human, goes to the position, comes back and so on. After a certain time (a number m of loops) it feels tired and goes back to wandering. However, it could also feel tired at random moments of the play phase and stop playing before the time is finished. The probability that this happens is half the one that this happens in normal state, since play time is supposedly engaging.

The grid:
- The grid on which the robot moves is limited, and the dog can't go outside of it.
- The human can move in the same grid, and has the same location limitations as the robot.
- The kennel's position is fixed in position 3,3.
- The initial position is fixed in position 0,0.

## System's limitations
- A simulation environment could be added.
- The code supports few user commands and understands "go to 1 2" but wouldn't understand "go to one two" for example
- The user can't interface with the robot via shell, for example, since commands are pre defined inside the code.

## Authors
Chiara Saporetti: chiara.saporetti@gmail.com
