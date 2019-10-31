#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from app.model.discharge import Discharge
from app.util.query import ReportQuery
from app.model.enter import Enter
from app.model.monitor import Monitor
from . import db


class Report(db.Model):
    """
    异常申报单实体类
    attributes:
        reportId: 自增长主键
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_enterprise_abnormal_info'
    query_class = ReportQuery

    reportId = db.Column('id', primary_key=True)
    alarmType = db.Column('alarm_type')
    startTime = db.Column('start_time')
    endTime = db.Column('end_time')
    reason = db.Column('stop_reason')
    isDelete = db.Column('is_deleted')
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    dischargeId = db.Column('out_id', db.ForeignKey(Discharge.dischargeId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    enter = db.relationship('Enter', back_populates="reports")
    discharge = db.relationship('Discharge', back_populates="reports")
    monitor = db.relationship('Monitor', back_populates="reports")

    def __repr__(self):
        return '<Report %r>' % self.monitorName
