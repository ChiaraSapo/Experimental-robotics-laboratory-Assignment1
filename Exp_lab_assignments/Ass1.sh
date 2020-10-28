#!/bin/bash

#preparation of the enviroment
cd ../..
source devel/setup.bash
d=1
c=0
term=2
a=$(catkin_make | grep 100% )
test -z "$a" && b=0 || b=1

while [ "$b" -lt "$d" ] 
do 
	a=$(catkin_make | grep 100% )
	test -z "$a" && b=0 || b=1
	if [ "$c" -eq "$term" ] 
	then
		break
	fi
	c=$(($c+$d))
done
if [ $c -eq $term ]
then
	catkin_make
fi 

#installation
path2=$(find . -name Exp_lab_assignments -print 2>/dev/null | grep 'src/Exp_lab_assignments')
cd $path2
#activation of all sh scripts

a=$(find "$(pwd)" -name '*.sh' )
chmod +x $a
echo "All .sh files activated!"
#activation of all py scripts
a=$(find "$(pwd)" -name  *.py ) 
chmod +x $a
echo "All .py files activated!"

# files to run
gnome-terminal -x sh -c "roscore; bash"
gnome-terminal -x sh -c "rosrun smach_viewer smach_viewer.py; bash"

echo "Starting state machine"
gnome-terminal -x sh -c "rosrun Exp_lab_assignments state_manager.py; bash"

roslaunch --wait Exp_lab_assignments launch_all.launch

kill $(ps aux | grep "sh -c rosrun" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roslaunch" | tr -s ' '| cut -d ' ' -f 2)
kill $(ps aux | grep "sh -c roscore" | tr -s ' '| cut -d ' ' -f 2)

