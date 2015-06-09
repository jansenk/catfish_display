from models import *
from graphHelper import Graph
class Call:
    def __init__(self, callId):
        self.callId = callId
        reports = Report.objects.filter(call_id=callId).order_by("time_entered")
        self.desktop_stats_reports = []
        self.traceroutes = []
        self.server_reports = []
        self.android = []
        for report in reports:
            if report.agent_class == "android":
                self.android.append(report)
            elif report.agent_class == "server":
                self.server_reports.append(report)
            elif report.agent_class == "desktop":
                if report.has_traceroute():
                    self.traceroutes.append(report)
                if report.has_desktop_stats():
                    self.desktop_stats_reports.append(report)

    def get_call_time(self):
        if self.desktop_stats_reports():
            return self.desktop_stats_reports[0].call_time
        else:
            return None

    def getChartJson(self):
        if self.desktop_stats_reports:
            txLatency = dict(loss=[0], rtt=[0], jitter=[0])
            rxLatency = dict(loss=[0], jitter=[0])

            rxPacket = dict(total=[0], loss=[0], discrd=[0], reord=[0], dup=[0])
            txPacket = dict(total=[0], loss=[0], reord=[0], dup=[0])
            time = [0]
            for statReport in self.desktop_stats_reports:
                reportTime = statReport.call_time_in_seconds()
                time.append(int(reportTime))
                txrx = statReport.getTxRx()
                txLatencyNumbers = txrx['tx'].getLatencyNumbers()

                txLatency['loss'].append(txLatencyNumbers['loss'].last)
                txLatency['rtt'].append(txLatencyNumbers['loss'].last)
                txLatency['jitter'].append(txLatencyNumbers['loss'].last)
                
                txPacket['total'].append(expandedValues['tx']['total'])
                txPacket['loss'].append(expandedValues['tx']['loss'])
                txPacket['reord'].append(expandedValues['tx']['reord'])
                txPacket['dup'].append(expandedValues['tx']['loss'])

                rxPacket['total'].append(expandedValues['tx']['loss'])
                rxPacket['loss'].append(expandedValues['tx']['loss'])
                rxPacket['discrd'].append(expandedValues['tx']['loss'])
                rxPacket['reord'].append(expandedValues['tx']['loss'])
                rxPacket['dup'].append(expandedValues['tx']['loss'])
                










