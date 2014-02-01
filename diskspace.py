#!/usr/bin/python

#Author: Garfield Carneiro
#Date: 1 Feb 2014
#Note: Python 2.6.X compatible
#Description: This script checks and logs the disk space as per threshold.


import commands
import optparse
import sys
import time
import logging
import logging.handlers

parser = optparse.OptionParser()

parser.add_option("-t","--threshold", action="store", dest="threshold", help="Threshold limit after which alert should be generated.", type="int", default=90 )
parser.add_option("-f","--logfile", action="store", dest="logfile", help="File to be logged in, if not stdout.")
parser.add_option("-s","--syslog", action="store_true", dest="syslog", help="Log to syslog", default=False)

(opts, args) = parser.parse_args()
#print type(opts.logfile)
#print args
#print opts[threshold]


class  DiskSpaceAlert:
    
  def getDFOutput(self):
    dfOutput  = commands.getstatusoutput \
    ("df -h  2>/dev/null | grep -vE '^Filesystem|tmpfs|cdrom|udev|none'")[1].split('\n')
    return dfOutput
    
    
  def getFileSystemStatus(self, listCurrentDF):
      dictFSOccupied = {}
      for line in range(0,len(listCurrentDF)):
          dictFSOccupied[listCurrentDF[line].split()[5]] = int(listCurrentDF[line].split()[4].split('%')[0])
      
      return dictFSOccupied
  
  def logToSyslog(self,message):
    my_logger = logging.getLogger(sys.argv[0])
    my_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    my_logger.addHandler(handler)
    my_logger.critical(sys.argv[0] + " " +  message)
    
  
  def checkFileSystemAndLog(self, dictCurrentStatus, threshold=90, logFile=sys.stdout):
    for fs in dictCurrentStatus.keys():
      #print "Checking if", key, "is above", threshold, dictCurrentStatus[key]
      if dictCurrentStatus[fs] >= threshold :
        logmessage = '[' + time.ctime() + "] " + fs + ' is  above threshold of ' + str(threshold) + ". Currently at " + str(dictCurrentStatus[fs]) + "%\n"
        logFile.write(logmessage)
        if opts.syslog:
          print "Logging to Syslog"
          self.logToSyslog(logmessage)
        
        #print logmessage
    



dobj = DiskSpaceAlert()
dfOutPut = dobj.getDFOutput()
#print dfOutPut
#print dir(dobj)
occupiedspace = dobj.getFileSystemStatus(dfOutPut)
print occupiedspace



if opts.logfile == None:
  #fh = open(opts.logfile, 'a') 
  dobj.checkFileSystemAndLog(occupiedspace, threshold=int(opts.threshold))
else:
    try:
      fh = open(opts.logfile,'a')
      dobj.checkFileSystemAndLog(occupiedspace, threshold=int(opts.threshold), logfile=fh)
    except Exception:
      print "Cannot open log file for I/O"
      
    
#fh.close()
