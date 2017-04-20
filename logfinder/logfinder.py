#!/usr/bin/env python2.7

import commands
import argparse
import re
import os
import yaml
import datetime
import time

'''
__author__ = Garfield Carneiro

This is a Nagios Check for looking at dmesg logs
This can be customized for any log patterns and any command that will generate logs

# TODO : Date parsing can be more generic

[user@server ~]$ ./log_finder.py -p dmesg.yml -t 96 -T 48  -d
Tue Apr 11 03:49:06 2017 Namespace(debug_flag=True, pattern_file='dmesg.yml', time_crit='48', time_warn='96')
Tue Apr 11 03:49:06 2017 Lets validate our arguments.
Tue Apr 11 03:49:06 2017 Access to pattern file dmesg.yml is fine.
Tue Apr 11 03:49:06 2017 We are removing first key called log_src_command to get command.
Tue Apr 11 03:49:06 2017 Log generating command : /bin/dmesg
Tue Apr 11 03:49:06 2017 Regex Patterns we got : {'nic': {'warn': ['NIC Link is Up'], 'crit': ['NIC Link is Down', 'bonding: bond0: enslaving eth0 as a backup interface with a down link']}, 'disk': {'warn': ['NOHZ: local_softirq_pending 100', 'megaraid_sas.*Battery has failed'], 'crit': ['status: { DRDY ERR }', 'error: { UNC }', 'ata2.00: failed command: READ FPDMA QUEUED']}, 'kernel_trace': {'warn': ['Call Trace:']}}
Tue Apr 11 03:49:06 2017 Seperating warn from all Regex Patterns
Tue Apr 11 03:49:06 2017 Warning Regexes look like : {'nic': ['NIC Link is Up'], 'disk': ['NOHZ: local_softirq_pending 100', 'megaraid_sas.*Battery has failed'], 'kernel_trace': ['Call Trace:']}
Tue Apr 11 03:49:06 2017 Seperating crit from all Regex Patterns
Tue Apr 11 03:49:06 2017 No regexes found for priority crit
Tue Apr 11 03:49:06 2017 Critical Regexes look like : {'nic': ['NIC Link is Up'], 'disk': ['NOHZ: local_softirq_pending 100', 'megaraid_sas.*Battery has failed'], 'kernel_trace': ['Call Trace:']}
Tue Apr 11 03:49:06 2017 Return code for /bin/dmesg is 0
Tue Apr 11 03:49:06 2017 Returning command output with 1676 lines
Tue Apr 11 03:49:06 2017 Looking for regexes in key called nic
Tue Apr 11 03:49:06 2017 Looking for -->> .*?NIC Link is Down.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for -->> .*?bonding: bond0: enslaving eth0 as a backup interface with a down link.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for regexes in key called disk
Tue Apr 11 03:49:06 2017 Looking for -->> .*?status: { DRDY ERR }.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for -->> .*?error: { UNC }.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for -->> .*?ata2.00: failed command: READ FPDMA QUEUED.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for regexes in key called nic
Tue Apr 11 03:49:06 2017 Looking for -->> .*?NIC Link is Up.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Found Regex NIC Link is Up
Tue Apr 11 03:49:06 2017 Looking for regexes in key called disk
Tue Apr 11 03:49:06 2017 Looking for -->> .*?NOHZ: local_softirq_pending 100.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Looking for -->> .*?megaraid_sas.*Battery has failed.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Found Regex megaraid_sas.*Battery has failed
Tue Apr 11 03:49:06 2017 Looking for regexes in key called kernel_trace
Tue Apr 11 03:49:06 2017 Looking for -->> .*?Call Trace:.*? <<-- in cmd_output
Tue Apr 11 03:49:06 2017 Found Regex Call Trace:
Tue Apr 11 03:49:06 2017 Time right now is Tue Apr 11 03:49:06 2017
Tue Apr 11 03:49:06 2017 System Uptime in Epoch notation 1484200572.45
Tue Apr 11 03:49:06 2017 System Uptime in Human Readable format is Thu Jan 12 00:56:12 2017
Tue Apr 11 03:49:06 2017
Critcal Regex we found {} in cmd_output
Tue Apr 11 03:49:06 2017
Warning Regex we found {'nic': {'NIC Link is Up': 'ixgbe 0000:04:00.1: eth3: NIC Link is Up'}, 'disk': {'megaraid_sas.*Battery has failed': '[7425818.867172] megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed'}, 'kernel_trace': {'Call Trace:': '[407492.581909] Call Trace:'}} in cmd_output
Tue Apr 11 03:49:06 2017 After Parsing Critical Logs look like {}
Tue Apr 11 03:49:06 2017 After Parsing Warning Logs look like {1484608065.029768: ' Call Trace:', 1491626391.315031: ' megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed'}
Tue Apr 11 03:49:06 2017 Calculating Critical and Warning Time Window
Tue Apr 11 03:49:06 2017 Looking for Logs in 48 hours Window i.e. upto Sun Apr  9 03:49:06 2017
Tue Apr 11 03:49:06 2017 Parsed Logs {}
Tue Apr 11 03:49:06 2017 Calculating Critical and Warning Time Window
Tue Apr 11 03:49:06 2017 Looking for Logs in 96 hours Window i.e. upto Fri Apr  7 03:49:06 2017
Tue Apr 11 03:49:06 2017 Parsed Logs {1484608065.029768: ' Call Trace:', 1491626391.315031: ' megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed'}
Tue Apr 11 03:49:06 2017 ____________________________________________________________________________________________________
Tue Apr 11 03:49:06 2017 | Dmesg Human Timestamp = Mon Jan 16 18:07:45 2017 | Log window Human Timestamp = Fri Apr  7 03:49:06 2017 | Log  Window Unix Timestamp = 1491551346.45 |  Dmesg Log Line =  Call Trace: |
Tue Apr 11 03:49:06 2017 ____________________________________________________________________________________________________
Tue Apr 11 03:49:06 2017 ____________________________________________________________________________________________________
Tue Apr 11 03:49:06 2017 | Dmesg Human Timestamp = Sat Apr  8 00:39:51 2017 | Log window Human Timestamp = Fri Apr  7 03:49:06 2017 | Log  Window Unix Timestamp = 1491551346.45 |  Dmesg Log Line =  megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed |
Tue Apr 11 03:49:06 2017 ____________________________________________________________________________________________________
Tue Apr 11 03:49:06 2017 Log >>  megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed << is within the window of 96 hours
Warning. Following Patterns are found [' megaraid_sas 0000:03:00.0: 3774 (544935568s/0x0008/FATAL) - Battery has failed']

'''
''' A Note about all the times:
  System Uptime is calculated from Epoch time
  Hence System_uptime = (Now_time) - (contents of /proc/uptime)
  Dmesg Timestamps are seconds since System Uptime
'''

debug_flag = False

def dprint(msg):
    """ Print only when debugging is enabled """
    if argv.debug_flag:
        format = "%a %b %d %H:%M:%S %Y"
        today = datetime.datetime.today()
        timestamp = today.strftime(format)
        print(str(timestamp + " " + msg))


class LogPatternFinder():
    def __init__(self, argv):
        self.argv = argv
        dprint("Lets validate our arguments.")
        self.validate_CLI_args(argv)
        self.yaml_file_path = argv.pattern_file
        self.log_src_cmd, self.regex_patterns = self.YAML_to_dict(self.yaml_file_path)

        dprint("Log generating command : %s" % (self.log_src_cmd))
        dprint("Regex Patterns we got : %s" % (self.regex_patterns))

        self.warning_regexes = self.get_regex_of_priority(self.regex_patterns, priority='warn')
        dprint("Warning Regexes look like : %s" % (self.warning_regexes))

        self.critical_regexes = self.get_regex_of_priority(self.regex_patterns, priority='crit')
        dprint("Critical Regexes look like : %s" % (self.warning_regexes))

        cmd_output = self.run_command(self.log_src_cmd)

        critical_regex_results = self.find_regex_in_cmd_output(cmd_output, self.critical_regexes)
        warning_regex_results = self.find_regex_in_cmd_output(cmd_output, self.warning_regexes)

        time_format = "%a %b %d %H:%M:%S %Y"

        self.now_time = time.time()
        dprint("Time right now is %s" % (time.ctime(float(self.now_time))))

        self.system_uptime = float(self.get_system_uptime(self.now_time))

        dprint("\nCritcal Regex we found %s in cmd_output" % critical_regex_results)
        dprint("\nWarning Regex we found %s in cmd_output" % warning_regex_results)

        parsed_critical_regex_results = self.extract_timestamps_from_line(critical_regex_results)
        dprint("After Parsing Critical Logs look like %s" % (parsed_critical_regex_results))

        parsed_warning_regex_results = self.extract_timestamps_from_line(warning_regex_results)
        dprint("After Parsing Warning Logs look like %s" % (parsed_warning_regex_results))

        alerting_critical_logs = self.is_log_in_timewindow(parsed_critical_regex_results, time_window=int(argv.time_crit))
        alerting_warning_logs = self.is_log_in_timewindow(parsed_warning_regex_results, time_window=int(argv.time_warn))

        if len(alerting_critical_logs.keys()) > 0:
            print("Critical. Following Patterns are found %s" % (alerting_critical_logs.values()))
            exit(2)
        elif len(alerting_warning_logs.keys()) > 0:
            print("Warning. Following Patterns are found %s" % (alerting_warning_logs.values()))
            exit(1)
        else:
            print("OK. No Errors messages related to %s found after running %s in last [%s] or [%s] hours" % (self.yaml_file_path, self.log_src_cmd, argv.time_warn, argv.time_crit ))

    def validate_CLI_args(self, argv):
        '''This function validates whether we got all required program args'''
        if argv.debug_flag:
            global debug_flag
            debug_flag = True

        if argv.pattern_file is None:
            print "You need to supply pattern file path (-p)."
            exit(2)
        elif os.path.isfile(argv.pattern_file):
            if not os.access(argv.pattern_file, os.R_OK):
                dprint("Pattern file %s is not readable." % (argv.pattern_file))
                exit(2)
            else:
                dprint("Access to pattern file %s is fine." % (argv.pattern_file))
                return True
        else:
            print("File %s does not exist. Exiting." % (argv.pattern_file))
            exit(2)

        if argv.time_warn <= argv.time_crit:
            print("Warning Window should be greater than Critical Window.")
            print("You can leave this default to Crit/Warn as 48/24 hours.")
            exit(1)

    def YAML_to_dict(self, yaml_file):
        '''This functions extracts command to run and the regexes to run against it.'''
        yaml_regex_patterns = yaml.load(open(yaml_file))
        dprint("We are removing first key called log_src_command to get command.")
        log_src_cmd = yaml_regex_patterns.pop('log_src_command')
        # We now have a dict{} called facility_priority_dict in format such as facility: {priority: regex}
        facility_priority_dict = yaml_regex_patterns
        return log_src_cmd, facility_priority_dict

    def get_system_uptime(self, now_time):
        '''Return Uptime of system in Epoch notation
           Dmesg log timestamp are relative to system uptime
            true_log_timestamps = system_uptime + dmesg_relative_time'''
        with open('/proc/uptime',) as uptime_file:
            uptime = now_time - float(uptime_file.readlines()[0].split()[0].split('.')[0])
        dprint("System Uptime in Epoch notation %s" % (uptime))
        dprint("System Uptime in Human Readable format is %s" % time.ctime(uptime))
        return(uptime)

    def extract_timestamps_from_line(self, matched_log_lines):
        '''This function checks if we have timestamps in log lines and returns a dictionary of log_time:log_message'''
        parsed_logs = {}
        dmesg_time_regex = "^\[\s*(?P<time>\d+\.\d+)\](?P<log_msg>.*)$"
        time_re_obj = re.compile(dmesg_time_regex)

        for keytype_regex_pattern in matched_log_lines.keys():
            for matched_log_line in matched_log_lines[keytype_regex_pattern].keys():
                log_line = matched_log_lines[keytype_regex_pattern][matched_log_line]
                match_obj = time_re_obj.match(log_line)
                if match_obj:
                    log_time = float(match_obj.groupdict().get('time')) + float(self.system_uptime)
                    log_message = match_obj.groupdict().get('log_msg')
                    parsed_logs[log_time] = log_message
        return parsed_logs

    def is_log_in_timewindow(self, parsed_logs, time_window):
        '''
        This function checks whether a dictionary of logs and the corresponding Epoch timing is in time window of 'x' hours
        It will return a dictionary where we found the logs in selected time frame
        '''
        dprint("Calculating Critical and Warning Time Window")
        alerting_window = self.now_time - datetime.timedelta(hours=time_window).total_seconds()
        dprint("Looking for Logs in %s hours Window i.e. upto %s" % (time_window, time.ctime(alerting_window)))
        dprint("Parsed Logs %s" % (parsed_logs))
        alerting_logs = {}
        for dmesg_unix_time in parsed_logs.keys():
            dprint("_" * 100)
            dprint("| Dmesg Human Timestamp = %s | Log window Human Timestamp = %s | Log  Window Unix Timestamp = %s |  Dmesg Log Line = %s | " % (time.ctime(dmesg_unix_time), time.ctime(alerting_window), alerting_window, parsed_logs[dmesg_unix_time]))
            dprint("_" * 100)
            if dmesg_unix_time >= alerting_window:
                dprint("Log >> %s << is within the window of %s hours" % (parsed_logs[dmesg_unix_time], time_window))
                alerting_logs[dmesg_unix_time] = parsed_logs[dmesg_unix_time]
        return(alerting_logs)

    def get_regex_of_priority(self, regex_patterns, priority):
        """" This function returns a dictionary containing priorities like warn and crit """
        dprint("Seperating %s from all Regex Patterns" % (priority))
        filtered_messages = {}
        for keytype_regex_pattern in regex_patterns.keys():
            if priority not in regex_patterns[keytype_regex_pattern].keys():
                dprint("No regexes found for priority %s" % (priority))
            elif priority in regex_patterns[keytype_regex_pattern].keys():
                temp_warn_list = []
                for warning_regexes in regex_patterns[keytype_regex_pattern][priority]:
                    temp_warn_list.append(warning_regexes)
                filtered_messages[keytype_regex_pattern] = temp_warn_list
        return filtered_messages

    def find_regex_in_cmd_output(self, cmd_output, regex_patterns):
        matched_ones = {}

        for pattern_key in regex_patterns.keys():
            dprint("Looking for regexes in key called %s" % (pattern_key))
            for regex_pattern in regex_patterns[pattern_key]:
                re_mix = '.*?' + regex_pattern + '.*?'
                dprint("Looking for -->> %s <<-- in cmd_output" % (re_mix))

                re_result = re.findall(re_mix, cmd_output)

                if re_result:
                    dprint("Found Regex %s" % (regex_pattern))
                    temp_dict = {}
                    temp_dict[regex_pattern] = re_result[-1]
                    matched_ones[pattern_key] = temp_dict

        return matched_ones

    def run_command(self, shell_command):
        shell_return_code, cmd_output = commands.getstatusoutput(shell_command)
        dprint("Return code for %s is %s" % (shell_command, shell_return_code))
        if shell_return_code == 0:
            dprint("Returning command output with %s lines" % len(cmd_output.split('\n')))
            return(cmd_output)
        else:
            dprint("We had issues running %s. Exiting." % (shell_command))
            exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", dest="debug_flag", default=False, action="store_true", help="Debug flag")
    parser.add_argument("--pattern-file", "-p", dest="pattern_file", type=str, action="store",  help="YAML file containing regex patterns for identifying error messages")
    parser.add_argument("--warning-window", "-t", default=48, dest="time_warn", action="store", help="Check only for warning as described in pattern file")
    parser.add_argument("--critical-window", "-T", default=24, dest="time_crit", action="store", help="Check only for warning as described in pattern file")
    argv = parser.parse_args()
    dprint(str(argv))

    log_file_finder = LogPatternFinder(argv=argv)
