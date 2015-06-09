from django.shortcuts import render
import pytz, time, datetime
from models import Traceroute, TracerouteHop, Report, StatsTxRx, CallStats, TxRxLatency, ServerReport
import json
# Create your views here.
# calls : listof {transmission: {jitter, loss, rtt}, reception: {loss, jitter}}

def index(request):
    entries = Report.objects.exclude(call_id="").order_by("call_id").order_by("entry_time")
    callData = []
    current_data = {"id": entries[0].call_id, "desktop": 0, "server":0, "android":0}
    for call in entries:
        if call.call_id != current_data['id']:
            callData.append(current_data)
            current_data = {"id": call.call_id, "desktop": 0, "server":0, "android":0}
        current_data[call.agent_class] += 1
    callData.append(current_data)
    return render(request, 'index.html', dict(callData=callData))


def call(request, callId):
    callEntries = Report.objects.filter(call_id=callId)
    desktop = callEntries.filter(agent_class="desktop")
    stats = traceroutes = None


#ordered desktop reports -> json data for charts
def getDesktopCharts(reports):
    charts = dict()
    for report in reports:


def getServerCharts(reports):



def desktopHelper(request, callId=None):
    if callId is None:
        allCalls = Metadata.objects.filter(agent_class="desktop")
    else:
        allCalls = Metadata.objects.filter(agent_class="desktop", call_id=callId)
    callDataList = []
    for call in allCalls:
        callStats = CallStats.objects.get(metadata_id_fk=call)
        callTx = StatsTxRx.objects.get(stats_id_fk=callStats, type="tx")
        txLoss = TxRxLatency.objects.get(txrx_id_fk=callTx, name="loss_period")
        txJitter = TxRxLatency.objects.get(txrx_id_fk=callTx, name="jitter")
        txRtt = TxRxLatency.objects.get(txrx_id_fk=callTx, name="rtt")
        transmissionDict = dict(loss=txLoss, jitter=txJitter, rtt=txRtt)

        callRx = StatsTxRx.objects.get(stats_id_fk=callStats, type="rx")
        rxLoss = TxRxLatency.objects.get(txrx_id_fk=callRx, name="loss_period")
        rxJitter = TxRxLatency.objects.get(txrx_id_fk=callTx, name="jitter")

        fullTo = callStats.to_user + "@" + callStats.to_domain
        receptionDict = dict(loss=rxLoss, jitter=rxJitter)

        callDataList.append(dict(id=call.id, to=fullTo, transmitted=transmissionDict,
                                 received=receptionDict, time=callStats.call_time))
    return render(request, 'desktop/desktop.html', dict(calls=callDataList))

def desktopCall(request, callId):
		return desktopHelper(request, callId) 
def desktop(request):
		return desktopHelper(request)


def server(request):
    serverCalls = ServerReport.objects.all().distinct()
    return render(request, 'server/server.html', dict(calls=serverCalls))

def serverGraph(request):
    return render(request, 'server/serverGraph.html')

def callServerGraph(request, callId):
    callData = ServerReport.objects.filter(call_id=callId).distinct().order_by("duration")
    recvdData = [[0, 0]]
    recvdLost = [[0, 0]]
    for call in callData:
        timeChunks = map(int, call.duration.split(":"))
        totalMs = sum([chunk*conversion for chunk, conversion in zip(timeChunks, [60000, 1000, 1])])
        recvdData.append([totalMs, call.rec_packets])
        recvdLost.append([totalMs, call.rec_lost])

    return render(request, 'server/callGraph.html', dict(callId=callId, recData=json.dumps(recvdData), recLostData=json.dumps(recvdLost)))

def desktopMtrDisplay(request, callId):
    try:
        #get the most recent mtr data for this call
        call = Metadata.objects.filter(call_id=callId, agent_class="desktop").order_by("timestamp")[0]
        print "Have call"
        callMtr = DesktopMtr.objects.get(metadata_id_fk=call)
        print "Have MTR"
        callMtrConnections = TracerouteHop.objects.filter(mtr_id_fk=callMtr).order_by("hop")
        print "have connections x %d" % len(callMtrConnections)
        hops = [hop.displayDict() for hop in callMtrConnections]
        print "list is good"
        print "all good"
    except Exception as e:
        print e
        return render(request, 'desktop/mtrFlow.html', dict(callId=callId))
    print json.dumps(hops)
    return render(request, 'desktop/mtrFlow.html', dict(callId=callId, hops="%s" % json.dumps(hops)))

def dag(request):
    return render(request, 'dagretest.html')


