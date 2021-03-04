#!/bin/bash

# files to run
gnome-terminal -x sh -c "roscore; bash"
#gnome-terminal -x sh -c "rosrun smach_viewer smach_viewer.py; bash"

gnome-terminal -x sh -c "rosrun stage_ros stageros $(rospack find Exp_lab_assignments)/world/MIRO.world; bash"
#echo "Starting state machine"
gnome-terminal -x sh -c "rosrun Exp_lab_assignments state_manager.py; bash"
gnome-terminal -x sh -c "rosrun Exp_lab_assignments printInfo.py; bash"

roslaunch --wait Exp_lab_assignments launch_all.launch



kill $(ps aux | grep "sh -c rosrun" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roslaunch" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roscore" | tr -s ' '| cut -d ' ' -f 2)

