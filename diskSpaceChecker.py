#!/usr/bin/python

#Author: Garfield Carneiro
#Date: 1 Feb 2014
#Note: Python 2.6.X compatible
#Description: This script checks and logs the disk space as per threshold.

# TIP: Run this script using Cron. Turn on Syslog Option 
# If Splunk monitors  and alerts for syslog, look for pattern like below
# Feb  2 18:44:07 linuxbox.domain.com DISKSPACE.PY[4062]: /home is  above threshold of 90. Currently at 93%

# Usage: python diskSpaceChecker.py --threshold 85 --syslog 


import commands
import optparse
import sys
import time
import syslog


def dprint(*message):
  if opts.debug:
    print(message)

parser = optparse.OptionParser()

parser.add_option("-t","--threshold", action="store", dest="threshold", help="Threshold Limit after which alert should be generated", type="int", default=90 )
parser.add_option("-f","--logfile", action="store", dest="logfile", help="File to be logged in, if not StdOut.")
parser.add_option("-s","--syslog", action="store_true", dest="syslog", help="Log to Syslog.", default=False)
parser.add_option("-d","--debug", action="store_true", dest="debug", help="Turn on Debugging.", default=False)

(opts, args) = parser.parse_args()

dprint("Options are", opts)
dprint("Arguments are", args)

class  DiskSpaceChecker:
    
  def getDFOutput(self):
    dfOutput  = commands.getstatusoutput \
    ("/bin/df -Ph  2>/dev/null | grep -vE '^Filesystem|tmpfs|cdrom|udev|none'")[1].split('\n')
    return dfOutput
    
    
  def getFileSystemStatus(self, listCurrentDF):
      dictFSOccupied = {}
      for line in range(0,len(listCurrentDF)):
          dictFSOccupied[listCurrentDF[line].split()[5]] = int(listCurrentDF[line].split()[4].split('%')[0])
      
      return dictFSOccupied
  
  def logToSyslog(self,message):
      dprint("Logging to Syslog")
      syslog.openlog(ident=sys.argv[0].upper(), logoption=syslog.LOG_PID, facility=syslog.LOG_ALERT,)
      syslog.syslog(message)
    
  
  def checkFileSystemAndLog(self, dictCurrentStatus, threshold=90, logFile=sys.stdout):
    for fs in dictCurrentStatus.keys():
      if (dictCurrentStatus[fs] >= threshold):
        logmessage =   "ALERT: " + fs + ' is  above threshold of ' + str(threshold) + ". Currently at " + str(dictCurrentStatus[fs]) + "%\n"
        logFile.write('[' + time.ctime() + "] " + logmessage)
        if opts.syslog:
          self.logToSyslog(logmessage)
      elif (dictCurrentStatus[fs] < threshold):
        dprint("INFO: " + fs + " is at " + str(dictCurrentStatus[fs]) + "%")
        
    



dObj = DiskSpaceChecker()
listDfOutPut = dObj.getDFOutput()
dprint(listDfOutPut)

dictOccupiedSpace = dObj.getFileSystemStatus(listDfOutPut)

if opts.logfile == None:
  dprint("No Log file given. Printing to StdOut")
  dObj.checkFileSystemAndLog(dictOccupiedSpace, threshold=int(opts.threshold))
else:
    try:
      fh = open(opts.logfile,'a')
      dprint(fh)
      dObj.checkFileSystemAndLog(dictOccupiedSpace, threshold=int(opts.threshold), logFile=fh)
    except Exception:
      print "Cannot open log file for I/O"
      
if 'fh' in locals():
  dprint("Closing openfile " + opts.logfile)
  fh.close()
      