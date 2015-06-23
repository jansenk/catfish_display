from django.shortcuts import render
from django.shortcuts import get_object_or_404
import pytz, time, datetime
from models import Traceroute, TracerouteHop, Report, StatsTxRx, CallStats, TxRxLatency, ServerReport, TracerouteLocation
import json
from call import Call
# Create your views here.
# calls : listof {transmission: {jitter, loss, rtt}, reception: {loss, jitter}}

def index(request):
    entries = Report.objects.exclude(call_id="").order_by("call_id")
    calls = []
    current_id = None
    for report in entries:
       	if report.call_id != current_id:
      			calls.append(Call(report.call_id))
			current_id = report.call_id
    return render(request, 'index.html', dict(calls=calls))

def call(request, callId):
    try:
        targetCall = Call(callId)
    except Exception as e:
        print "Cannot create call " + str(e)
        return render(request, 'call.html', dict(callId=callId))
    else:
        context = targetCall.getChartJson()
        context['call_duration'] = targetCall.get_call_time()
        context['callId'] = callId
        context['call_to'] = targetCall.getCallTo()
        context['call'] = targetCall
        return render(request, 'call.html', context)

def desktopHelper(request, callId=None):
    if callId is None:
        allCalls = Report.objects.filter(agent_class="desktop")
    else:
        allCalls = Report.objects.filter(agent_class="desktop", call_id=callId)
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
        call = Call(callId)
        print "have call"
        if not call.has_traceroute():
            print "No traceroute found for %s" % callId
        trace = call.traceroutes[-1].traceroute_set.get()
        callMtrConnections = trace.traceroutehop_set.order_by("hop")
        print "have connections x %d" % len(callMtrConnections)
        hops = [hop.displayDict() for hop in callMtrConnections]
        print "list is good"
        print "all good"
    except Exception as e:
        print e
        return render(request, 'altTraceroute.html', dict(callId=callId))
    print json.dumps(hops)
    return render(request, 'altTraceroute.html', dict(callId=callId, trace=hops))

def dag(request):
    return render(request, 'dagretest.html')

def tracerouteLocation(request, location_id):
    location = get_object_or_404(TracerouteLocation, id=location_id)
    recent_hop = TracerouteHop.objects.get(id=location.most_recent_traceroute_hop_id)
    return render(request, "location.html", dict(location=location, hops=recent_hop.traceroute.traceroutehop_set.all()))



