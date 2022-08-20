import win32evtlog # requires pywin32 pre-installed

server = 'localhost' # name of the target computer to get event logs
logtype = 'Application' # 'System' # 'Application' # 'Security'
hand = win32evtlog.OpenEventLog(server,logtype)
# EVENTLOG_SEQUENTIAL_READ // 循序读
# EVENTLOG_BACKWARDS_READ  // 向后读
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)

while True:
    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            print('Event Category:', event.EventCategory)
            print('Time Generated:', event.TimeGenerated)
            print('Source Name:', event.SourceName)
            print('Event ID:', event.EventID)
            print('Event Type:', event.EventType)
            data = event.StringInserts
            if data:
                print('Event Data:')
                for msg in data:
                    print(msg)
            # print('\n')