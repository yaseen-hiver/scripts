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
  """Print only when Debug option is passed"""
  if opts.debug:
    print(message)

parser = optparse.OptionParser()

parser.add_option("-t","--threshold", action="store", dest="threshold", help="Threshold Limit after which alert should be generated", type="int", default=90 )
parser.add_option("-c","--critical", action="store", dest="critical", help="Critical Logging Limit")
parser.add_option("-f","--logfile", action="store", dest="logfile", help="File to be logged in, if not StdOut.")
parser.add_option("-s","--syslog", action="store_true", dest="syslog", help="Log to Syslog.", default=False)
parser.add_option("-d","--debug", action="store_true", dest="debug", help="Turn on Debugging.", default=False)

(opts, args) = parser.parse_args()


"""Calculate critical limit"""

if opts.critical != None:
  critical = opts.critical
elif (int(opts.threshold) + 5 <= 100):
  critical =  int(opts.threshold) + 5
elif (int(opts.threshold) + 5 > 100):
  critical = 100


msgCritical = '[CRITICAL]'
msgWarning = '[WARNING]'  
  

dprint("Options are", opts)
dprint("Arguments are", args)

class  DiskSpaceChecker:
    
  def getDFOutput(self):
    """Run df and get all filesystem status including NFS"""
    dfOutput  = commands.getstatusoutput \
    ("/bin/df -Ph  2>/dev/null | grep -vE '^Filesystem|tmpfs|cdrom|udev|none'")[1].split('\n')
    return dfOutput
    
    
  def getFileSystemStatus(self, listCurrentDF):
    """Parses output from getDFOutput() and outputs a dictionary containing Filesystem usage"""
    dictFSOccupied = {}
    for line in range(0,len(listCurrentDF)):
        dictFSOccupied[listCurrentDF[line].split()[5]] = int(listCurrentDF[line].split()[4].split('%')[0])
      
    return dictFSOccupied
  
  def logToSyslog(self,message):
    """Log to Syslog if only the --syslog option is passed"""
    dprint("Logging to Syslog")
    # syslog.openlog(ident=sys.argv[0].upper(), logoption=syslog.LOG_PID, facility=syslog.LOG_ALERT)
    syslog.syslog(message)
    
  
  def checkFileSystemAndLog(self, dictFSStatus, threshold=90, logFile=sys.stdout):
    """Check each filesystem and log as ALERT or INFO (if debug mode is enabled) depending upon threshold"""
    
    dprint("Critical is", critical)
    dprint(dictFSStatus.keys())
    
    for fs in dictFSStatus.keys(): 
      dprint("Checking, ", fs)
      if (dictFSStatus[fs] >= critical):
        logmessage =   "[CRITICAL] Disk Space Alert: " + fs + ' is  above threshold of ' + str(threshold) + ". Currently at " + str(dictFSStatus[fs]) + "%\n"
        logFile.write('[' + time.ctime() + "] " + logmessage)
      elif (dictFSStatus[fs] >= threshold):
        logmessage =   "[WARNING] Disk Space Alert: " + fs + ' is  above threshold of ' + str(threshold) + ". Currently at " + str(dictFSStatus[fs]) + "%\n"
      if opts.syslog:
          self.logToSyslog(logmessage)
      elif (dictFSStatus[fs] < critical):
          dprint("INFO: " + fs + " is at " + str(dictFSStatus[fs]) + "%")
        
    

dObj = DiskSpaceChecker()
listDfOutPut = dObj.getDFOutput()
dprint(listDfOutPut)

dictOccupiedSpace = dObj.getFileSystemStatus(listDfOutPut)
dprint(dictOccupiedSpace)

if opts.logfile == None:
  dprint("No Log file given. Printing to StdOut")
  dprint(dictOccupiedSpace)
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
      
