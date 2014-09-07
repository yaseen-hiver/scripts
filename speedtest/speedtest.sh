#!/bin/bash

MAILTO=""
LOG_DIR="/var/log/speedtest"


LOGFILE_DATE=$(date "+%d-%b-%Y")
LOGTIME=$(date "+%d%b%Y-%H%M%S")
#LOGFILE=$LOG_DIR/speedtest-$LOGFILE_DATE.log #Use this if you are not using logrotate
LOGFILE=$LOG_DIR/speedtest.log

#echo "Log File is $LOGFILE"

if [ ! -d $LOG_DIR ] ; then
    mkdir $LOG_DIR
fi

echo -n "$LOGTIME|"  >> $LOGFILE
/usr/local/bin/speedtest --server 4064 | egrep  'Upload:|Download:' | tr '\n' '|'  >> $LOGFILE
echo "" >> $LOGFILE

exit
