#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.model.attachment import Attachment
from app.model.discharge import Discharge
from app.util.query import ReportQuery
from app.model.enter import Enter
from app.model.monitor import Monitor
from . import db


# class Report(db.Model):
#     """
#     异常申报单实体类
#     attributes:
#         reportId: 自增长主键
#     """
#     __table_args__ = {'schema': 'enterprise_archives.dbo'}
#     __tablename__ = 't_enterprise_abnormal_info'
#     query_class = ReportQuery
#
#     reportId = db.Column('id', primary_key=True)
#     alarmType = db.Column('alarm_type')
#     startTime = db.Column('start_time')
#     endTime = db.Column('end_time')
#     reason = db.Column('stop_reason')
#     isDelete = db.Column('is_deleted')
#     enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
#     dischargeId = db.Column('out_id', db.ForeignKey(Discharge.dischargeId))
#     monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
#     enter = db.relationship('Enter', back_populates="reports")
#     discharge = db.relationship('Discharge', back_populates="reports")
#     monitor = db.relationship('Monitor', back_populates="reports")
#
#     def __repr__(self):
#         return '<Report %r>' % self.monitorName

class Report(db.Model):
    """
    异常申报单实体类
    attributes:
        reportId: 自增长主键
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_enterprise_abnormal_info'
    query_class = ReportQuery

    reportId = db.Column('id', primary_key=True, autoincrement=True)
    alarmType = db.Column('alarm_type')
    startTime = db.Column('start_time')
    endTime = db.Column('end_time')
    dataType = db.Column('dataType')
    state = db.Column('is_review')
    isDelete = db.Column('is_deleted', default=0)
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    dischargeId = db.Column('out_id', db.ForeignKey(Discharge.dischargeId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    enter = db.relationship('Enter', back_populates="reports")
    discharge = db.relationship('Discharge', back_populates="reports")
    monitor = db.relationship('Monitor', back_populates="reports")

    __mapper_args__ = {
        "order_by": reportId
    }

    def __repr__(self):
        return '<Report %r>' % self.reportId

    @property
    def enterName(self):
        return self.enter.enterName

    @property
    def enterAddress(self):
        return self.enter.enterAddress

    @property
    def dischargeName(self):
        return self.discharge.dischargeName

    @property
    def monitorName(self):
        return self.monitor.monitorName

    @property
    def districtName(self):
        return self.enter.cityName + self.enter.areaName

    @property
    def startTimeStr(self):
        return self.startTime.strftime('%Y-%m-%d %H:%M')

    @property
    def endTimeStr(self):
        return self.endTime.strftime('%Y-%m-%d %H:%M')


class DischargeReport(Report):
    stopReason = db.Column('stop_reason')
    reportTime = db.Column('applay_time')

    __mapper_args__ = {
        "order_by": reportTime.desc()
    }

    @property
    def reportTimeStr(self):
        return self.reportTime.strftime('%Y-%m-%d')

    @property
    def stopTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.alarmType, 2, 'stopType')).first()[0]

    @property
    def attachments(self):
        return Attachment.query.filter_by(fileModelId=self.reportId, fileType='enterStopApply')


class FactorReport(Report):
    exceptionReason = db.Column('exception_reason')
    reportTime = db.Column('update_time')
    factorCode = db.Column('factor_code')

    __mapper_args__ = {
        "order_by": reportTime.desc()
    }

    @property
    def alarmTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.f_GetEnterType(self.alarmType)).first()[0]

    @property
    def reportTimeStr(self):
        return self.reportTime.strftime('%Y-%m-%d')

    @property
    def factorCodeStr(self):
        return db.session.query(func.enterprise_archives.dbo.f_GetEnterType(self.factorCode)).first()[0]

    @property
    def attachments(self):
        return Attachment.query.filter_by(fileModelId=self.reportId, fileType='enterAbnormalApply').order_by(
            Attachment.attachmentId)
