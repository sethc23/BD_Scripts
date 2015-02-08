import sys

def calStr(events):
    template_start = ('BEGIN:VCALENDAR\r\n' + 
          'METHOD:PUBLISH\r\n' + 
          'X-WR-TIMEZONE:US/Eastern\r\n' + 
          'PRODID:-//Apple Inc.//iCal 3.0//EN\r\n' + 
          'CALSCALE:GREGORIAN\r\n' + 
          'X-WR-CALNAME:Home\r\n' + 
          'VERSION:2.0\r\n' + 
          'X-WR-REL' + 
          'CALID:8FA9EA19-3C4D-4FD4-AF01-F3458A9DAE20\r\n' + 
          'X-APPLE-CALENDAR-COLOR:#0252D4\r\n' + 
          'BEGIN:VTIMEZONE\r\n' + 
          'TZID:US/Eastern\r\n' + 
          'BEGIN:DAYLIGHT\r\n' + 
          'TZOFFSETFROM:-0500\r\n' + 
          'TZOFFSETTO:-0400\r\n' + 
          'DTSTART:20070311T020000\r\n' + 
          'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\r\n' + 
          'TZNAME:EDT\r\n' + 
          'END:DAYLIGHT\r\n' + 
          'BEGIN:STANDARD\r\n' + 
          'TZOFFSETFROM:-0400\r\nTZOFFSETTO:-0500\r\n' + 
          'DTSTART:20071104T020000\r\n' + 
          'RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\r\n' + 
          'TZNAME:EST\r\n' + 
          'END:STANDARD\r\n' + 
          'END:VTIMEZONE\r\n')
    template_end = ('END:VCALENDAR')
    calStr = template_start
    for item in events:
        calStr = calStr + item
    calStr = calStr + template_end
    return calStr
    

def eventStr(startDate, endDate, msg):
    template_middle = ('BEGIN:VEVENT\r\n' + 
              'SEQUENCE:5\r\n' + 
              'TRANSP:TRANSPARENT\r\n' + 
              'DTSTART;VALUE=DATE:*startDate*\r\n' + 
              'DTSTAMP:20101226T143010Z\r\n' + 
              'SUMMARY:*eventMsg*\r\n' + 
              'CREATED:20101226T143010Z\r\n' + 
              'DTEND;VALUE=DATE:*endDate*\r\n' + 
              'RRULE:FREQ=YEARLY;INTERVAL=1\r\n' + 
              'END:VEVENT\r\n')
    #   *startDate*==YYYYMMDD
    #   *endDate*== *startDate* + 1 ==YYYYMMDD
    #   *eventMsg* == str
    template_middle = template_middle.replace('*startDate*', startDate).replace('*eventMsg*', msg).replace('*endDate*', endDate)
    return template_middle
    


f = open('/Users/admin/Python/Scripts/new_birthdays.txt', 'r')  # format date-tab-name
x = f.read()
f.close()

events = []
a = x.split('\r')
for line in a:
    b = line.split('	')
    dates = b[0]
    c = dates.split('/')
    startDate = '2011' + c[0] + c[1]
    endDate = '2011' + c[0] + str(eval(c[1].strip('0')) + 1)
    msg = 'B-Day: ' + b[1]
    events.append(eventStr(startDate, endDate, msg))

outputData = calStr(events)

f = open('/Users/admin/Desktop/birthdays.ics', 'w')
# print >> f, outputData
f.write(outputData)
f.close()

