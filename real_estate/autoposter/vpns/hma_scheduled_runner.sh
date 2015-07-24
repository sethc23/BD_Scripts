#!/bin/bash
################################################
# A SIMPLE SCHEDULE IP CHANGE SCRIPT FOR LINUX #
# MAKE SURE YOU HAVE RUN hma-udp-grabber.sh    #
################################################

ovpn_file=$1
process_to_run=$2


cd /etc/openvpn/hma/
while true
	do
		openvpn --daemon --config $ovpn_file # <<<< change the config file string to match your prefered server
		echo "#####################"
		echo "Press CTRL+C to stop."
		echo "#####################"
		sleep 60 # <<<< wait for connection to be established
		# do something here
        $process_to_run
		killall openvpn # <<<< disconnect
		sleep 30 # <<<< wait a bit more to make sure that the openvpn has been properly disconnected 
    done
	#			----------- NOTE -----------				#
				# IT'S NOT ADVISABLE TO SWITCH THE IP FASTER THAN 4 - 5 MINUTES WHEN RUNNING	#
				# THIS SCRIPT ON TWO COMPUTERS AT THE SAME TIME; WHEN RUNNING ON A SINGLE	#
				# COMPUTER YOU CAN CHANGE THE IP AS FAST AS 2 MINUTES AND 30 SECONDS.		#
done
