from django.shortcuts import render
from models import DesktopMtr, DesktopMtrConnections, Metadata, StatsTxRx, CallStats, TxRxLatency
# Create your views here.
# calls : listof {transmission: {jitter, loss, rtt}, reception: {loss, jitter}}
def listCalls(request):
    allCalls = Metadata.objects.all()
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

        fullTo1 = (callStats.to_user, callStats.to_domain)
        fullTo = callStats.to_user + "@" + callStats.to_domain
        receptionDict = dict(loss=rxLoss, jitter=rxJitter)

        callDataList.append(dict(to=fullTo, transmitted=transmissionDict,
                                 received=receptionDict, time=callStats.call_time))
    return render(request, 'desktop/desktop.html', dict(calls=callDataList))
