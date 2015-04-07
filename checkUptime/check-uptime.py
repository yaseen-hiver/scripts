#!/usr/bin/env python2.7
import os
import argparse

#Declare critical and warning defaults
C_HOURS = 1
C_MINUTES = 15
W_HOURS = C_HOURS + 1
#W_MINUTES = 30 

#Nagios States and Return Codes
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
 
parser = argparse.ArgumentParser()
parser.add_argument("--chours",   "-ch", type=int, default=C_HOURS, action="store", help="Hours critical")
parser.add_argument("--cminutes", "-cm", type=int, default=C_MINUTES, action="store", help="Minutes critical")
parser.add_argument("--whours",   "-wh", type=int, default=W_HOURS, action="store", help="Hours warning")
#parser.add_argument("--wminutes", "-wm", type=int, default=W_MINUTES, action="store", help="Minutes warning")
argv = parser.parse_args()
#print argv

# Gives a human-readable  uptimeString
def uptime():
  try:
    f = open( "/proc/uptime" )
    contents = f.read().split()
    f.close()
  except:
    return "Cannot open uptime file: /proc/uptime"

  total_seconds = float(contents[0])
  #print total_seconds
    
  # Helper vars:
  MINUTE  = 60
  HOUR    = MINUTE * 60
  DAY     = HOUR * 24

  # Get the days, hours, etc:
  days    = int( total_seconds / DAY )
  hours   = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )

  # Build up the pretty uptimeString (like this: "N days, N hours, N minutes, N seconds")
  uptimeString = ""
   
  #print "DAYS = %s HOURS = %s, MINUTES = %s" % (days, hours, minutes)
  #print "CRITICAL: HOURS = %s, MINUTES = %s" % (argv.chours, argv.cminutes) 
  
  if days > 0:
    uptimeString += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
  if len(uptimeString) > 0 or hours > 0:
    uptimeString += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
  if len(uptimeString) > 0 or minutes > 0:
    uptimeString += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
    uptimeString += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
  
  #print uptimeString

  if ( days == 0 and hours == 0 and  minutes <= argv.cminutes ) :
    print "CRITICAL: Uptime is less than %s minutes. Currently %s" % ( argv.cminutes, uptimeString )
    return STATE_CRITICAL
  elif ( days == 0 and hours < argv.chours ) :
    print "CRITICAL: Uptime is less than %s hours. Currently %s" % ( argv.chours, uptimeString )
    return STATE_CRITICAL
  elif ( days == 0 and (( hours >= argv.chours ) and ( hours <= argv.whours)) ) :
    print "WARNING: Uptime is  %s hours. Currently %s" % ( argv.whours , uptimeString )
    return STATE_WARNING
  elif ( days >= 0 and ( hours > argv.whours ) ) :
    print "OK.  Uptime is %s " % (uptimeString)
    return STATE_OK

  #return uptimeString;

  #print "The system uptime is:", uptime() 
exitCode = uptime()
exit(exitCode)
