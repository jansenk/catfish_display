from models import *
from graphHelper import Graph
class Call:
    def __init__(self, callId):
        self.id = callId

    def getDesktopCount(self):
        return self.getCount("desktop")
    def getAndroidCount(self):
        return self.getCount("android")
    def getServerCount(self):
        return self.getCount("server")
    def getCount(self, target):
        return Report.objects.filter(callId=self.id, agent_class=target).count()

    def has_traceroute(self):
        return Traceroute.objects.filter(report__call_id=self.id).exists()

    def get_call_time(self):
        try:
            return CallStats.objects.filter(report__call_id=self.id).latest('report__entry_time').call_id
        except models.Model.DoesNotExist:
            return None

    def getStatReports(self):
        return Report.objects.filter(call_id=self.id).

    def getCallTo(self):
        if self.desktop_stats_reports:
            stat = self.desktop_stats_reports[0].callstats_set.first()
            return stat.to_user + "@" + stat.to_domain


    def getChartJson(self):
        txLatency = dict(loss=[0], rtt=[0], jitter=[0])
        rxLatency = dict(loss=[0], jitter=[0])

        rxPacket = dict(total=[0], loss=[0], discrd=[0], reord=[0], dup=[0])
        txPacket = dict(total=[0], loss=[0], reord=[0], dup=[0])
        time = [0]
        for report in self.getStatReports():
            statReport = report.callstats_set.get()
            reportTime = statReport.call_time_in_seconds()
            time.append(int(reportTime))
            txrx = statReport.getTxRx()
            txLatencyNumbers = txrx['tx'].getLatencyNumbers()
            txLatency['loss'].append(txLatencyNumbers['loss_period'])
            txLatency['rtt'].append(txLatencyNumbers['rtt'])
            txLatency['jitter'].append(txLatencyNumbers['jitter'])
                
            txPacket['total'].append(int(txrx['tx'].total_pkt))
            txPacket['loss'].append(int(txrx['tx'].loss))
            txPacket['reord'].append(int(txrx['tx'].reorder))
            txPacket['dup'].append(int(txrx['tx'].dup))

                rxLatencyNumbers = txrx['rx'].getLatencyNumbers()

                rxLatency['loss'].append(rxLatencyNumbers['loss_period'])
                rxLatency['jitter'].append(rxLatencyNumbers['jitter'])

                rxPacket['total'].append(int(txrx['rx'].total_pkt))
                rxPacket['loss'].append(int(txrx['rx'].loss))
                rxPacket['reord'].append(int(txrx['rx'].reorder))
                rxPacket['dup'].append(int(txrx['rx'].dup))
                rxPacket['discrd'].append(int(txrx['rx'].discrd))

            txLatencyGraph = Graph(title="Latency (Transmission)",
                                   xtitle="Time (seconds)",
                                   ytitle="Latency (ms)")
            rxLatencyGraph = Graph(title="Latency (Reception)",
                                   xtitle="Time (seconds)",
                                   ytitle="Latency (ms)")
            txPacketGraph = Graph(title="Transmitted Packets",
                                  type="area",
                                  xtitle="Time (seconds)",
                                  ytitle="Packets")
            rxPacketGraph = Graph(title="Recieved Packets",
                                  type="area",
                                  xtitle="Time (seconds)",
                                  ytitle="Packets")

            context = dict()
            for (name, dataset, graph) in [("txLatency", txLatency, txLatencyGraph),
                                           ("rxLatency", rxLatency, rxLatencyGraph),
                                           ("txPacket", txPacket, txPacketGraph),
                                           ("rxPacket", rxPacket, rxPacketGraph)]:
                for seriesName, seriesData in dataset.iteritems():
                    graph.addSeries(seriesName, zip(time, seriesData))
                context[name] = graph.toJson()
            return context
