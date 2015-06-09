# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
import re

from django.db import models
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    agent_class = models.CharField(db_column='class', max_length=7)  # Field renamed because it was a Python reserved word.
    version = models.CharField(max_length=16)
    guid = models.IntegerField()
    timestamp = models.DateTimeField()
    auth = models.CharField(max_length=16)
    call_id = models.CharField(max_length=64)
    entry_time = models.DateTimeField()

    def has_traceroute(self):
        return len(self.traceroute_set) != 0
    def has_desktop_stats(self):
        return len(self.callstats_set) != 0

    class Meta:
        managed = False
        db_table = 'report'

class Traceroute(models.Model):
    start = models.DateTimeField()
    host = models.CharField(max_length=64)
    id = models.AutoField(primary_key=True)
    report = models.ForeignKey(Report, db_column='report_id_fk')

    class Meta:
        managed = False
        db_table = 'traceroute'

class TracerouteHop(models.Model):
    id = models.AutoField(primary_key=True)
    traceroute = models.ForeignKey(Traceroute, db_column='traceroute_id_fk')
    name = models.CharField(max_length=64)
    loss_pct = models.DecimalField(max_digits=10, decimal_places=0)
    snt = models.IntegerField()
    last = models.DecimalField(max_digits=10, decimal_places=0)
    avg = models.DecimalField(max_digits=10, decimal_places=0)
    best = models.DecimalField(max_digits=10, decimal_places=0)
    wrst = models.DecimalField(max_digits=10, decimal_places=0)
    stdev = models.DecimalField(max_digits=10, decimal_places=0)
    hop = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'traceroute_hops'

    # The label is :
    def getLabel(self):
        template = "%(hop)s)%(name)s: %(loss)s%% loss\n" + \
                   "Average ping: %(avg)s\n" + \
                   "Best ping: %(best)s\n" + \
                   "Worst ping: %(worst)s\n" + \
                   "Last ping: %(last)s\n" + \
                   "Ping Standard Deviation: %(stddev)s"
        return template % dict(hop=self.hop, name=self.name, loss=self.loss_pct, avg=self.avg, best=self.best, worst=self.wrst,
                               last=self.last, stddev=self.stdev)

    # If any values are "abnormal" the color is red
    # If any of the values are "questionable" the color is yellow
    # else, green
    def getColor(self):
        if self.name == "???":
            return "#FFFF85"
        else:
            return "#99FF66"

    def displayDict(self):
        label = self.getLabel()
        print "got label"
        return {"label": label, "style": "fill: %s" % self.getColor()}


callStatsTimeRe = re.compile("(.*?)h:(.*?)m:(.*?)s")
class CallStats(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=64)
    call_conn_ms = models.IntegerField()
    call_first_res_ms = models.IntegerField()
    call_time = models.CharField(max_length=64)
    to_user = models.CharField(max_length=64)
    to_domain = models.CharField(max_length=64)
    tag = models.IntegerField()
    report = models.ForeignKey(Report, db_column='report_id_fk')

    def getTxRx(self):
        return {txrx.type: txrx for txrx in self.statxtxrx_set}

    def call_time_in_seconds(self):
        match = callStatsTimeRe.search(self.call_time)
        return sum([chunk*conversion for chunk, conversion in zip(match.groups(), [3600, 60, 1])])

    class Meta:
        managed = False
        db_table = 'desktop_stats'



class StatsTxRx(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=2)
    loss = models.IntegerField()
    loss_pct = models.DecimalField(max_digits=10, decimal_places=0)
    pt = models.IntegerField()
    discrd = models.IntegerField(blank=True, null=True)
    discrd_pct = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    ptime = models.IntegerField(blank=True, null=True)
    last_update = models.CharField(max_length=64)
    total_pkt_size = models.CharField(max_length=64)
    total_pkt_size_ip_hdr = models.CharField(max_length=64)
    total_pkt_avg = models.CharField(max_length=64)
    reorder = models.IntegerField()
    reorder_pct = models.DecimalField(max_digits=10, decimal_places=0)
    dup = models.IntegerField()
    dup_pct = models.DecimalField(max_digits=10, decimal_places=0)
    total_pkt = models.IntegerField()
    parent_stats = models.ForeignKey(CallStats, db_column='stats_id_fk')

    class Meta:
        managed = False
        db_table = 'desktop_stats_txrx'

    def getLatencyNumbers(self):
        return {txrxl.name: txrxl for txrxl in self.txrxlatency_set}

class TxRxLatency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=11)
    max = models.DecimalField(max_digits=10, decimal_places=0)
    min = models.DecimalField(max_digits=10, decimal_places=0)
    avg = models.DecimalField(max_digits=10, decimal_places=0)
    last = models.DecimalField(max_digits=10, decimal_places=0)
    dev = models.DecimalField(max_digits=10, decimal_places=0)
    parent_txrx = models.ForeignKey(StatsTxRx, db_column='txrx_id_fk')

    class Meta:
        managed = False
        db_table = 'desktop_txrx_latency'

class ServerReport(models.Model):
    peer = models.CharField(max_length=45, blank=True, null=True)
    call_id = models.CharField(max_length=45, blank=True, null=True)
    duration = models.CharField(max_length=45, blank=True, null=True)
    rec_packets = models.IntegerField(blank=True, null=True)
    rec_lost = models.IntegerField(blank=True, null=True)
    rec_lost_pct = models.CharField(max_length=45, blank=True, null=True)
    rec_jitter = models.CharField(max_length=45, blank=True, null=True)
    sent_packets = models.IntegerField(blank=True, null=True)
    sent_lost = models.IntegerField(blank=True, null=True)
    sent_lost_pct = models.CharField(max_length=45, blank=True, null=True)
    sent_jitter = models.CharField(max_length=45, blank=True, null=True)
    report = models.ForeignKey(Report, db_column="metadata_id_fk")

    class Meta:
        managed = False
        db_table = 'server_report'





