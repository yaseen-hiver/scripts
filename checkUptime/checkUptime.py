#!/usr/bin/env python2.7
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--wminutes", "-wm", type=int, default=5, action="store", help="Minutes warning")
parser.add_argument("--cminutes", "-cm", type=int, default=2, action="store", help="Minutes critical")
parser.add_argument("--whours",   "-wh", type=int, default=0, action="store", help="Hours warning")
parser.add_argument("--chours",   "-ch", type=int, default=1, action="store", help="Hours critical")

argv = parser.parse_args()
print argv

 
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3 
 
#----------------------------------------
# Gives a human-readable uptime string
def uptime():
 
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"
 
     total_seconds = float(contents[0])
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;
 
#print "The system uptime is:", uptime()