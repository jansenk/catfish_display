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

from django.db import models

class Metadata(models.Model):
    id = models.AutoField(primary_key=True)
    agent_class = models.CharField(db_column='class', max_length=7)  # Field renamed because it was a Python reserved word.
    version = models.CharField(max_length=16)
    guid = models.IntegerField()
    timestamp = models.DateTimeField()
    auth = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'metadata'

class DesktopMtr(models.Model):
    start = models.DateTimeField()
    host = models.CharField(max_length=64)
    id = models.AutoField(primary_key=True)
    metadata_id_fk = models.ForeignKey(Metadata, db_column='metadata_id_fk')

    class Meta:
        managed = False
        db_table = 'desktop_mtr'


class DesktopMtrConnections(models.Model):
    id = models.AutoField(primary_key=True)
    mtr_id_fk = models.ForeignKey(DesktopMtr, db_column='mtr_id_fk')
    name = models.CharField(max_length=64)
    loss_pct = models.DecimalField(max_digits=10, decimal_places=0)
    snt = models.IntegerField()
    last = models.DecimalField(max_digits=10, decimal_places=0)
    avg = models.DecimalField(max_digits=10, decimal_places=0)
    best = models.DecimalField(max_digits=10, decimal_places=0)
    wrst = models.DecimalField(max_digits=10, decimal_places=0)
    stdev = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'desktop_mtr_connections'


class CallStats(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=64)
    call_conn_ms = models.IntegerField()
    call_first_res_ms = models.IntegerField()
    call_time = models.CharField(max_length=64)
    to_user = models.CharField(max_length=64)
    to_domain = models.CharField(max_length=64)
    tag = models.IntegerField()
    metadata_id_fk = models.ForeignKey(Metadata, db_column='metadata_id_fk')

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
    stats_id_fk = models.ForeignKey(CallStats, db_column='stats_id_fk')

    class Meta:
        managed = False
        db_table = 'desktop_stats_txrx'


class TxRxLatency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=11)
    max = models.DecimalField(max_digits=10, decimal_places=0)
    min = models.DecimalField(max_digits=10, decimal_places=0)
    avg = models.DecimalField(max_digits=10, decimal_places=0)
    last = models.DecimalField(max_digits=10, decimal_places=0)
    dev = models.DecimalField(max_digits=10, decimal_places=0)
    txrx_id_fk = models.ForeignKey(StatsTxRx, db_column='txrx_id_fk')

    class Meta:
        managed = False
        db_table = 'desktop_txrx_latency'


class DjangoMigrations(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'



