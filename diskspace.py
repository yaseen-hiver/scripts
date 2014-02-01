#!/usr/bin/python

#Author: Garfield Carneiro
#Date: 1 Feb 2014
#Note: Python 2.6.X compatible
#Description: This script checks and logs the disk space as per threshold.


import commands
import optparse
import sys
import time

parser = optparse.OptionParser()

parser.add_option("-t","--threshold", action="store", dest="threshold", help="Threshold limit after which alert should be generated.", type="int", default=90 )
parser.add_option("-f","--logfile", action="store", dest="logfile", help="File to be logged in, if not stdout.", default=sys.stdout)

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
  
  def checkFileSystemAndLog(self, dictCurrentStatus, threshold=90, logFile=sys.stdout):
    for fs in dictCurrentStatus.keys():
      #print "Checking if", key, "is above", threshold, dictCurrentStatus[key]
      if dictCurrentStatus[fs] >= threshold :
        logmessage = '[' + time.ctime() + "] " + fs + ' is  above threshold of ' + str(threshold) + ". Currently at " + str(dictCurrentStatus[fs]) + "\n"
        logFile.write(logmessage)
        #print logmessage
    



dobj = DiskSpaceAlert()
dfOutPut = dobj.getDFOutput()
#print dfOutPut
#print dir(dobj)
occupiedspace = dobj.getFileSystemStatus(dfOutPut)
print occupiedspace




fh = open(str(opts.logfile), 'a') 
dobj.checkFileSystemAndLog(occupiedspace, logFile=fh, threshold=int(opts.threshold))
fh.close()
