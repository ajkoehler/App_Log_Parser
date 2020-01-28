# get app, get failure message
# look for next success message for same app
# do time math
# store and see if it's the longest
# max_log_parse.py
# 2018-08-21

import os
import re
import datetime
from datetime import timedelta
import math
myFile = 'C:/BuildReleaseExample.log'

#regex of log file, date, time, then words 
q = re.compile('((\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3}) - (\w+.*) (\w+.*))')

myList = []


#open file
with open(myFile, 'r') as f:
    lines = f.read().splitlines()
    #print(lines)
    #print(' ' + lines[0])
    for line in lines:
        #print(line)
        prev = None
        # find all values in the file
        key_val = q.findall(line)
        for x in key_val:
            #print(key_val)
            #print(line)
            #i = 0
            #it = iter(key_val)
            #prev = next(it)
            #print(x)
            #print ()
            #a = x[:]
            # set variables
            YEAR = x[1]
            MONTH = x[2]
            DAY = x[3]
            HOUR = x[4]
            MINUTE = x[5]
            SEC = x[6]
            MS = x[7]
            APP = x[8]
            STATUS = x[9]
            #print(a[8] + ' ' + a[9])
            # look for failure
            if STATUS == 'failure':
                #print(APP + ' ' + STATUS)		
                #print(i)
                #print('Found Test Failure: ',x[0])
                lookup = x[0]
                # find line # of failure
                line_no = lines.index(lookup)
                #print('Found on line: ', line_no+1)

                #print('Looking for next success of that ' + APP + ' Test: ')
                #print(lines)
                # look for successes of that APP
                suc_search = APP + ' ' + 'success'
                # enumerate through successes (line numbers)
                indices = [i for i, s in enumerate(lines) if suc_search in s]
                for i in indices:
                    #print(i)
                    # if the success is later in the file, aka higher line number, do more
                    if i > line_no:
                        #print('Success found at line: ', i+1)
                        
                        #print('That line is: ', lines[i])
                        # split line into variables
                        t = lines[i].split()
                        #print(t[0:])
                        DATE = t[0]
                        TIME = t[1]
                        #print(DATE + ' ' + TIME)
                        date1 = YEAR + '-' + MONTH + '-' + DAY + ' ' + HOUR + ':' + MINUTE + ':' + SEC + '.' + MS
                        date2 = DATE + ' ' + TIME
                        # calculate time difference
                        #print(date1)
                        #print(date2)
                        start = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
                        ends = datetime.datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
                        diff = ends - start
                        #print(diff)
                        days = diff.days
                        seconds = int(round(diff.total_seconds()))
                        
                        mins, seconds = divmod(seconds, 60)
                        hours, mins = divmod(mins, 60)
                        
                        hours = int(diff.seconds // (60 * 60))
                        mins = int((diff.seconds // 60) % 60)

                        # add time difference to a list to compare it to the next iteration
                        #print("{:d}:{:02d}:{:02d}".format(hours, mins, seconds))
                        myList.append(diff)
                        if myList[0] < diff:
                            myList[0] = diff
                            a = APP
                            d = days
                            h = hours
                            m = mins
                            s = seconds
                            #print(APP + ' was in failure state for: ', hours, 'hours, ', mins, 'mins, and ', seconds, ' seconds')
                            #print('New Max is ', myList[0])       
                        break
print('')
# finally print the final top time
print(a + ': ', d, ' days, ', h, ' hours, ', m, ' minutes and ', s, ' seconds')
#RealTimeTradingSystem: 2 days, 3 hours, 15 minutes and 41 seconds
print('')
