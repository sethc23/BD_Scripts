#!/bin/bash -l
################################################
# A SIMPLE SCHEDULE IP CHANGE SCRIPT FOR LINUX #
# MAKE SURE YOU HAVE RUN hma-udp-grabber.sh    #
################################################

ovpn_file=$1
process_to_run=$2
vpn_cfg_dir="/etc/openvpn/hma"

# Colors
red="\033[1;31m" green="\033[1;32m" yellow="\033[1;33m" white="\033[1;37m" normal="\033[0m"
# permissions
if [ $USER != root ]; then echo -e $red"ERROR:$normal You need root privileges to continue... (sudo)" ; exit 0; fi

function title () {
echo -e $green"====$yellow HMA-SCHEDULED-RUNNER$green ===="$normal; }
function show.progress () { i=0
while [ -r $TEMP ]; do clear; title
echo -e $yellow"elapsed time $i seconds"$normal
let i=i+1; sleep 1; done; }


cd "$vpn_cfg_dir"
while true
	do
		bash -l -i -c "openvpn --daemon --config $ovpn_file" # <<<< change the config file string to match your prefered server
		echo "openvpn --daemon --config $ovpn_file"
        echo "#####################"
		echo "Press CTRL+C to stop."
		echo "#####################"
		echo "Waiting 60 seconds for connection to be established"
        show.progress &
        sleep 60 # <<<< wait for connection to be established
		# do something here
        echo "Running Script"
        echo `ps | grep openvpn`
        bash -l -i -c $process_to_run
        bash -l -i -c "get_my_ip_ext"
        echo "Killing openVPN"
		killall openvpn # <<<< disconnect
        echo "Waiting 30 seconds to make sure that the openvpn has been properly disconnected"
		sleep 30 # <<<< wait a bit more to make sure that the openvpn has been properly disconnected 
        echo "DONE!"
        exit 1
    done
	#			----------- NOTE -----------				#
				# IT'S NOT ADVISABLE TO SWITCH THE IP FASTER THAN 4 - 5 MINUTES WHEN RUNNING	#
				# THIS SCRIPT ON TWO COMPUTERS AT THE SAME TIME; WHEN RUNNING ON A SINGLE	#
				# COMPUTER YOU CAN CHANGE THE IP AS FAST AS 2 MINUTES AND 30 SECONDS.		#
done
