# Experimental robotics laboratory Assignments

## Introduction
The package Exp_Lab_Assignments simulates a robotic dog moving on a gridded plane. He can either sleep in his kennel, wander around or play with a simulated user. In order to play with the robot the user has to say "Hey buddy" or "Play". If he says so, the dog approaches the person and waits for a command such as "go to 1 2", or for a pointing gesture in a direction. It then goes to the desired location and comes back. After a while it again starts wandering around around. 
The project is implemented in python and run on ROS. 

## Software architecture and state diagrams
The architecture is composed of four nodes. One of them, the state_manager,  implements a finite state machine with 3 different states. The nodes are the following:

### State_manager:

This node publishes on the command topic. It has a finite state machine composed of three different states:

<p align="center">
  <img height="500" width="500" src="https://github.com/andreabradpitto/SofAr-project/blob/master/Images%20and%20multimedia/Image.jpeg?raw=true "Title"">
</p>

The states are hereby described:
- SLEEP: The state publishes the "go home" command, waits a few seconds to simulate Miro's nap, then outputs the "normal command" to transition to the normal state.
- NORMAL: The state enters in a loop. At each iteration it listens to the user: if the user says "Hey buddy" or "Play", it outputs the "play command" to transition to the play state. It the user says nothing, the state publishes the command "go rand" and waits a few seconds to wait for the execution of the command. It could also randomly send the "sleep command" to transition to sleep state, in case Miro feels sleepy. At the end of the loop, if nothing has changes, the state outputs the "sleep command".
- PLAY: The state enters in a loop and looks at the user to get its position and publishes. It waits a few seconds for the execution of the command then listens to the user: if the user says "Go to posx posy" (where posx and posy are two random x and y positions inside the grid where Miro moves), this command is published. If the user again says "Hey buddy" or "Play", Miro waits. If the user says nothing, Miro looks at his gestures and publishes the position indicated by the user hand. At the end of the loop, the "normal command" is set as output of the stata.
The user action is simulated through two functions: "user says" and "user does", respectively implementing speech commands and postion/gesture commadns.


### Geometry_grounding:

It subscribes to the command topic and analyzes the the command it receives: 
- if it is a "go to posx posy" command, it estrapolates the coordinates from the command string 
- if it is a "go home" command, it sets the home coordinates, which are saved in the ros parameter server.
- if it is a "go rand" command, it computes random coordinates
It publishes the coordinates on the "target pos" topic

### Planner:

It subscribes to the "target pos" topic and computes a simple trajectory to get from the current position (read from the ros param server) to the target position (read from the topic). It first reaches the x coordinate and then the y coordinate. It publishes the trajectory on the "trajectory" topic.

### Robot motion controller:

It subscribes to the "trajectory topic" and should control the robots actuators in order to make it move. In practice it waits 2 seconds and then updates the current position and calls the function to plot the grid and the robot motion.

## How to run the code:
Download the package in your_catkin_ws/src.
```sh
cd "Your catkin workspace"/src/Exp_Lab_Assignments
./launcher.sh
```
This will install the package and launch the nodes and the launch file.
