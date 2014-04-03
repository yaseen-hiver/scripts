#!/usr/bin/python

#Author: Garfield Carneiro
#Date: 4 April 2014
#Note: Python 2.6.X compatible
#Description: This script checks and logs the disk space as per threshold.

# TIP: Run this script using Cron. Turn on Syslog Option 
# If Splunk monitors  and alerts for syslog, look for pattern like below
# Feb  2 18:44:07 linuxbox.domain.com DISKSPACE.PY[4062]: /home is  above threshold of 90. Currently at 93%

# Usage: python diskSpaceChecker.py --warning 85 --syslog 


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

parser.add_option("-t","--warning", action="store", dest="warning", help="Threshold Limit after which alert should be generated", type="int", default=90)
parser.add_option("-c","--critical", action="store", dest="critical", help="Critical Limit after which alert should be generated", type="int")
parser.add_option("-f","--logfile", action="store", dest="logfile", help="File to be logged in, if not StdOut.")
parser.add_option("-s","--syslog", action="store_true", dest="syslog", help="Log to Syslog.", default=False)
parser.add_option("-d","--debug", action="store_true", dest="debug", help="Turn on Debugging.", default=False)

(opts, args) = parser.parse_args()


"""Calculate Critical"""

if opts.critical != None:
  critical = opts.critical
elif (int(opts.warning) + 5 <= 100):
  critical =  int(opts.warning) + 5
elif (int(opts.warning) + 5 > 100):
  critical = 100
  
dprint("Critical is", critical)
  
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
    
  def logger(self, message):
    
    if opts.logfile == None:
      dprint("No Log file given. Printing to StdOut")
      logfile = sys.stdout
    else:
        try:
          logfile = open(opts.logfile,'a')
          dprint(logfile)
        except Exception:
            print "Cannot open %s log file for I/O" % (opts.logfile)
          
    dprint("Logfile is" , logfile)
    logfile.write(message)
    
    """Write to Syslog if true"""
    if opts.syslog:
      syslog.syslog(message)
    
    
  
  def logToSyslog(self,message):
    """Log to Syslog if only the --syslog option is passed"""
    dprint("Logging to Syslog")
    # syslog.openlog(ident=sys.argv[0].upper(), logoption=syslog.LOG_PID, facility=syslog.LOG_ALERT)
    syslog.syslog(message)
    
  def checkCriticalLimit(self, fs):
    if (dictOccupiedSpace[fs] >= critical):
      return True
    
      
  def checkWarningLimit(self, fs):
    if (dictOccupiedSpace[fs] >= int(opts.warning)):
      return True
    else:
      return False
  
  
  def checkFileSystemAndLog(self, dictCurrentStatus, warning=90):
    """Check each filesystem and log as ALERT or INFO (if debug mode is enabled) depending upon warning"""
    
    for fs in dictCurrentStatus.keys():
      
      if self.checkCriticalLimit(fs):
        logmessage = '[' + time.ctime() + "] " +  "[Disk Space CRITICAL] Disk Space: " + fs + ' is  above critical threshold of ' + str(critical) +  \
        ". Currently at " + str(dictCurrentStatus[fs]) + "%\n"
        self.logger(logmessage)
        
        
      elif self.checkWarningLimit(fs):
        
        logmessage =   '[' + time.ctime() + "] " + "[Disk Space WARNING] : " + fs + ' is  above warning threshold of ' + str(warning) + \
        ". Currently at " + str(dictCurrentStatus[fs]) + "%\n"
        self.logger(logmessage)
        
          
      elif not self.checkWarningLimit(fs):
        dprint("INFO: " + fs + " is at " + str(dictCurrentStatus[fs]) + "%")
        
    

dObj = DiskSpaceChecker()
listDfOutPut = dObj.getDFOutput()
dprint(listDfOutPut)

dictOccupiedSpace = dObj.getFileSystemStatus(listDfOutPut)


dObj.checkFileSystemAndLog(dictOccupiedSpace, warning=int(opts.warning))

      
#if 'fh' in locals():
#  dprint("Closing openfile " + opts.logfile)
#  fh.close()
      
