import random, datetime, os, calendar, time, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catfish_display.settings')
django.setup()
from desktop.models import *

#packets, total=(min, max) number, else (min, max)percentage of total
#jitter currently meaningless
input_latency_percentages = {"loss_period":(0,0),
                             "rtt":        (0,0),
                             "jitter":     (0,0)}
input_packet_percentages = {"total": (1000,2000),
                            "loss":  (1, 2),
                            "discrd":(2, 3),
                            "reord": (1,2),
                            "dup":   (1,7)}
latency_percentages = {key: random.randint(val[0], val[1])
                      for key, val in input_latency_percentages.iteritems()}
packet_percentages = {key: random.randint(val[0], val[1])
                      for key, val in input_packet_percentages.iteritems()}
print "latency percentages: ", latency_percentages
print "packet percentrages: ", packet_percentages

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

def generateCall(numReports, callId):
    txLatencySequences = dict(loss_period= generateRandomList(0, 20, numReports),
                             rtt= generateRandomList(0, 20, numReports),
                             jitter= generateRandomList(0, 20, numReports))
    rxLatencySequences = dict(loss_period= generateRandomList(0, 20, numReports),
                             jitter= generateRandomList(0, 20, numReports))

    totalPackets = packet_percentages['total']

    rxPacketSequences = dict(total= generateIncreasingList(numReports, totalPackets),
                             loss= generateIncreasingList(numReports, int((.01 * packet_percentages['loss']) * totalPackets)),
                             discrd=generateIncreasingList(numReports, int((.01 * packet_percentages['discrd']) * totalPackets)),
                             reord=generateIncreasingList(numReports, int((.01 * packet_percentages['reord']) * totalPackets)),
                             dup=generateIncreasingList(numReports, int((.01 * packet_percentages['dup']) * totalPackets)))
    txPacketSequences = dict(total= generateIncreasingList(numReports, totalPackets),
                             loss= generateIncreasingList(numReports, int((.01 * packet_percentages['loss']) * totalPackets)),
                             reord=generateIncreasingList(numReports, int((.01 * packet_percentages['reord']) * totalPackets)),
                             dup=generateIncreasingList(numReports, int((.01 * packet_percentages['dup']) * totalPackets)))

    for i in range(0, numReports):
        print "Tick %d" % i
        report = generateReport(callId)
        stats = generateStats(report, i)

        tx = generateTx(stats, txPacketSequences, i)
        generateLatencies(tx, txLatencySequences, i)

        rx = generateRx(stats, rxPacketSequences, i)
        generateLatencies(rx, rxLatencySequences, i)
        print "Tick complete. Sleeping"
        time.sleep(3)
    print "Completed simulating call data"

    print "Simulating traceroute"
    generateTraceroute(callId, report)
    print "Call Complete"


# make a list by starting from zero and the adding a random number (0 - 100)
#  then scale the list to be 0 - 100
def generateIncreasingList(len, ciel=100):
    print "generating a random increasing list"
    firstList = [0]
    total = 0
    for _ in range(0, len):
        total += random.randint(0, 100)
        firstList.append(total)
    print "First list: ", firstList
    scaled = [(x * ciel) / total for x in firstList]
    print "scaled from zero to %d" % ciel
    print scaled

    return scaled

def generateRandomList(floor, ciel, len):
    return [random.randint(floor, ciel) for _ in range(0, len)]


def generateReport(callId,
                   agent="desktop",
                   version="fakeVersion",
                   guid="111000",
                   timestamp=datetime.datetime.now(),
                   auth="42"):
    report = Report()
    report.agent_class = agent
    report.version = version
    report.guid = guid
    report.timestamp = timestamp
    report.auth = auth
    report.call_id = callId
    report.save()
    return report

def generateStats(report, i,
                  status="DataGeneratorConfirmed",
                  con_ms=42,
                  first_ms=42,
                  call_time=None,
                  user="FakeUser",
                  domain="SimulatedDomain",
                  tag=1010101):
    stats = CallStats()
    stats.status = status
    stats.call_conn_ms = con_ms
    stats.call_first_res_ms = first_ms
    if not call_time:
        stats.call_time = generateCallTime(i + 1)
    else :
        stats.call_time = call_time
    stats.to_user = user
    stats.to_domain = domain
    stats.tag = tag
    stats.report = report
    stats.save()
    return stats

def generateCallTime(seconds):
    hours = minutes =  0
    secondsInHour = 60*60
    while seconds >= secondsInHour:
        hours += 1
        seconds -= secondsInHour
    while seconds >= 60:
        minutes += 1
        seconds -= 60

    return "{0:02d}h:{1:02d}m:{2:02d}s".format(hours, minutes, seconds)

def generateTx(stats, packetSequences, i):
    txrx = generateTxRxCommon(stats, packetSequences, i)
    txrx.type = "tx"
    txrx.save()
    return txrx

def generateRx(stats, packetSequences, i):
    txrx = generateTxRxCommon(stats, packetSequences, i)
    txrx.type = "rx"
    txrx.discrd = packetSequences["discrd"][i]
    txrx.discrd_pct = packetSequences['discrd'][i] / txrx.total_pkt if txrx.total_pkt != 0 else 0
    txrx.save()
    return txrx

def generateTxRxCommon(stats, packetSequences, i):
    txrx = StatsTxRx()
    txrx.total_pkt = packetSequences["total"][i]
    txrx.loss = packetSequences['loss'][i]
    txrx.pt = 111000
    txrx.ptime = 111000
    txrx.last_update = "LastUpdateSimulated"
    txrx.total_pkt_size = "PacketSizeSimulated"
    txrx.total_pkt_size_ip_hdr = "IPHDRSizeSimulated"
    txrx.total_pkt_avg = "AvgSizeSimulated"
    txrx.reorder = packetSequences["reord"][i]
    txrx.dup = packetSequences["dup"][i]
    txrx.parent_stats = stats

    if txrx.total_pkt == 0:
        txrx.loss_pct = txrx.reorder_pct = txrx.dup_pct = 0
    else:
        txrx.dup_pct = packetSequences['dup'][i] / txrx.total_pkt
        txrx.reorder_pct = packetSequences['reord'][i] / txrx.total_pkt
        txrx.loss_pct = packetSequences['loss'][i] / txrx.total_pkt

    return txrx

def generateLatencies(txrx, latencySequences, i):
    for key, value in latencySequences.iteritems():
        lat = TxRxLatency()
        lat.name = key
        lat.max = 1
        lat.min = 2
        lat.avg = 3
        lat.dev = 0
        lat.last = value[i]
        lat.parent_txrx = txrx
        lat.save()

def generateTraceroute(callId, report):
    tr = Traceroute()
    tr.start = datetime.datetime.now()
    tr.host = "FakeHost"
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

if (len(sys.argv) == 1):
    ticks = 10
    calls = 1
else:
    try:
        ticks = calls = None
        ticks = int(sys.argv[1])
        calls = int(sys.argv[2])
    except:
        if not ticks:
            ticks = 10
        if not calls:
            calls = 1
print "ticks=%d" % ticks
print "calls=%d" % calls
for calli in range(0, calls):
    print "Generating call %d" % calli
    callId = str(int(calendar.timegm(time.gmtime())))[-8:]
    print "CallId=%s" % callId
    generateCall(ticks, callId)
    print "----"

print "All done"

