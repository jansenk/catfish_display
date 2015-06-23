import datetime, calendar, time, django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catfish_display.settings')
print os.environ['DJANGO_SETTINGS_MODULE']
django.setup()
from desktop.models import *
from catfish_display import *


txLatency = dict(loss_period=[4,0,0,0,0,0,0,0,0,0],
                 rtt=[0,0,6,3,0,0,1,0,2,0],
                 jitter=[0,0,0,9,0,0,0,0,0, 0])
rxLatency = dict(loss_period=[1, 2, 5, 6, 7, 10, 11, 12, 17, 0],
                 jitter=[0,0,0,0,0,0,9,1,0,0])

rxPacket = dict(total=[12,13,20,25,30,35,50,51,70,80],
                loss= [0,0,0,0,0,0,0,0,10, 11],
                discrd=[0,0,0,6,7,8,9,10,11,12],
                reord=[0,0,2,2,2,2,2,4,5,6],
                dup=[0,0,0,0,0,3,6,10,2,3])

txPacket = dict(total=[12,13,20,25,30,35,50,51,70,80],
                loss= [0,0,0,0,0,0,0,0,10, 11],
                reord=[0,0,2,2,2,2,2,4,5,6],
                dup=[0,0,0,0,0,3,6,10,2,3])


def generateCallTime(timeSequence):
    if timeSequence == 10:
        return "00h:00m:10s"
    else:
        return "00h:00m:0%ds" % timeSequence

def generateReport(callId):
    report = Report()
    report.agent_class = "desktop"
    report.version = "fakeVersion"
    report.guid = "111000"
    report.timestamp = "2015-1-1 12:50:13"
    report.auth = "42"
    report.call_id = callId
    report.entry_time = datetime.datetime.now()
    return report

def generateStats(report, timeSequence):
    stats = CallStats()
    stats.status = "conFYrmd"
    stats.call_conn_ms = 42
    stats.call_first_res_ms = 42
    stats.call_time = generateCallTime(timeSequence + 1)
    stats.to_user = "bobby binkins"
    stats.to_domain = "google.website"
    stats.tag = 42
    stats.report = report
    return stats

def generateTxRxHelper(stats, dataSource, timeSequence):
    txrx = StatsTxRx()
    txrx.loss = dataSource["loss"][timeSequence]
    txrx.loss_pct = 0
    txrx.pt = 0
    txrx.ptime = 0
    txrx.last_update = "who cares"
    txrx.total_pkt_size = "666"
    txrx.total_pkt_size_ip_hdr = "666"
    txrx.total_pkt_avg = "666"
    txrx.reorder = dataSource["reord"][timeSequence]
    txrx.reorder_pct = 0
    txrx.dup = dataSource["dup"][timeSequence]
    txrx.dup_pct = 0
    txrx.total_pkt = dataSource["total"][timeSequence]
    txrx.parent_stats = stats
    return txrx
def generateTx(stats, timeSequence):
    txrx = generateTxRxHelper(stats, txPacket, timeSequence)
    txrx.type = "tx"
    return txrx
def generateRx(stats, timeSequence):
    txrx = generateTxRxHelper(stats, rxPacket, timeSequence)
    txrx.type = "rx"
    txrx.discrd = rxPacket["total"][timeSequence]
    txrx.discrd_pct = 0
    return txrx

def generateLatencies(timeSequence, dataSource, txrx):
    for field in dataSource:
        lat = TxRxLatency()
        lat.name = field
        lat.max = 0
        lat.min = 0
        lat.avg = 0
        lat.last = txLatency[field][timeSequence]
        lat.dev = 0
        lat.parent_txrx = txrx
        lat.save()

tracerouteData = [("192.168.1.1",0.00,10,2.2,2.2,2,2.7,0.2),
                  ("???", 100, 10,8.6,11,8.4,17.8,3),
                  ("68.86.210.126", 0.00,10,9.1,12.1,8.5,24.3,5.2),
                  ("68.86.208.22", 0.00, 10,12.2,15.1,11.7,23.4,4.4),
                  ("68.85.192.86", 0.00,10,17.2,14.8,13.2,17.2,1.3),
                  ("68.86.90.25", 0.00, 10, 14.2, 16.4, 14.2, 20.3, 1.9),
                  ("68.86.86.194", 0.00,10,17.6,16.8,15.5,18.1,0.9),
                  ("75.149.230.194", 0.00,10,15,20.1,15,33.8,5.6),
                  ("72.14.238.232", 0.00,10,15.6,18.7,14.1,32.8,5.9),
                  ("209.85.241.148", 0.00,10,16.3,16.9,14.7,21.2,2.2),
                  ("66.249.91.104", 0.00,10,22.2,18.6,14.2,36,6.5)]

def generateTraceroute(callId, report):
    tr = Traceroute()
    tr.start = datetime.datetime.now()
    tr.host = "boogeyman"
    tr.report = report
    tr.save()

    for i, hopData in zip(range(1, len(tracerouteData) + 1), tracerouteData):
        print "hop", i
        generateHop(i, hopData, tr, callId)

def generateHop(num, data, parent, callId):
    hop = TracerouteHop()
    hop.hop = num
    hop.name = data[0]
    hop.loss_pct = data[1]
    hop.snt = data[2]
    hop.last = data[3]
    hop.avg = data[4]
    hop.best = data[5]
    hop.wrst = data[6]
    hop.stdev = data[7]
    hop.traceroute = parent

    try:
        loc = TracerouteLocation.objects.get(name = hop.name)
    except:
        loc = TracerouteLocation()
        loc.name = hop.name
        loc.save()

    loc.most_recent_call_id = callId
    hop.location = loc
    hop.save()
    loc.most_recent_traceroute_hop_id = hop.id
    loc.save()

def generateData():
    callId = str(int(calendar.timegm(time.gmtime())))[-8:]
    print "CallId=%s" % callId
    for timeSequence in range(0, 10):
        print "Report for tick " + str(timeSequence)
        report = generateReport(callId)
        report.save()

        stats = generateStats(report, timeSequence)
        stats.save()
        print "stats for tick %d" % timeSequence

        tx = generateTx(stats, timeSequence)
        tx.save()
        print "stats for tick %d" % timeSequence

        rx = generateRx(stats, timeSequence)
        rx.save()

        generateLatencies(timeSequence, txLatency, tx)
        generateLatencies(timeSequence, rxLatency, rx)
        time.sleep(5)

    print "adding traceroute"
    report = generateReport(callId)
    report.save()
    generateTraceroute(callId, report)




    print "done"

if __name__ == "__main__":
    generateData()













