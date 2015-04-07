#!/usr/bin/env python2.7
import os
import argparse

#Declare critical and warning defaults
C_HOURS = 1
C_MINUTES = 15
W_HOURS = 2
W_MINUTES = 30 

#Nagios States and Return Codes
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
 
parser = argparse.ArgumentParser()
parser.add_argument("--chours",   "-ch", type=int, default=C_HOURS, action="store", help="Hours critical")
parser.add_argument("--cminutes", "-cm", type=int, default=C_MINUTES, action="store", help="Minutes critical")
parser.add_argument("--whours",   "-wh", type=int, default=W_HOURS, action="store", help="Hours warning")
parser.add_argument("--wminutes", "-wm", type=int, default=W_MINUTES, action="store", help="Minutes warning")
argv = parser.parse_args()
print argv

#----------------------------------------
# Gives a human-readable uptime string
def uptime():
 
  try:
    f = open( "./procuptime" )
    contents = f.read().split()
    f.close()
  except:
    return "Cannot open uptime file: /proc/uptime"

  total_seconds = float(contents[0])
  print total_seconds
    
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
   
  print "ARGUMENT CHOURS = %s, HOURS = %s, DAYS = %s" % (argv.chours, hours, days)
   
  if ( days == 0 and argv.chours == 0 and  minutes <= argv.cminutes ) :
    print "CRITICAL: Uptime is less than %s minutes" % ( argv.cminutes )
    return STATE_CRITICAL
  elif ( days == 0 and hours >= argv.chours ) :
    print "CRITICAL: Uptime is less than %s hours" % ( argv.chours )
    return STATE_CRITICAL
  elif ( days == 0 and argv.chours < 1 and  minutes <= argv.wminutes ) :
    print "WARNING: Uptime is less than %s minutes" % ( argv.wminutes )
    return STATE_WARNING
  elif ( days == 0 and hours >= argv.whours ) :
    print "WARNING: Uptime is less than %s hours" % ( argv.whours )
    return STATE_WARNING

  if days > 0:
    string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
    string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

  return string;

  #print "The system uptime is:", uptime()
  print uptime()
