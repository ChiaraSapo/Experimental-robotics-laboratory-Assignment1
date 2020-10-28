#!/bin/bash

gnome-terminal -x sh -c "roscore; bash"

echo "Starting state machine"
gnome-terminal -x sh -c "rosrun Exp_lab_assignments state_manager.py; bash"


roslaunch --wait Exp_lab_assignments launch_all.launch






kill $(ps aux | grep "sh -c rosrun" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roslaunch" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roscore" | tr -s ' '| cut -d ' ' -f 2)

