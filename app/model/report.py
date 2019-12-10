#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
import datetime
from sqlalchemy import func

import app
from app.model.attachment import Attachment
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
        alarmType: 异常类型
        startTime：异常开始时间
        endTime：异常结束时间
        dataType：数据类型 S：排口异常 A：因子异常 L：长期停产
        state：状态 0：待审核 1：审核通过 2：审核不通过（目前只要上报成功就默认审核通过）
        reportTime：申报时间
        isDelete：是否删除
        dataSource：数据来源
        enterId：关联企业外键
        dischargeId：关联排口外键
        monitorId：关联监控点外键
        enter：申报单对应的企业
        discharge：申报单对应的排口
        monitor：申报单对应的监控点
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_enterprise_abnormal_info'
    query_class = ReportQuery

    reportId = db.Column(db.Integer, name='id', primary_key=True, autoincrement=True)
    alarmType = db.Column('alarm_type')
    startTime = db.Column('start_time')
    endTime = db.Column('end_time')
    dataType = db.Column('dataType')
    state = db.Column('is_review', default=1)
    reportTime = db.Column('update_time', default=func.now())
    isDelete = db.Column('is_deleted', default=0)
    dataSource = db.Column('data_scource', default='wryapp')
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId), nullable=False)
    dischargeId = db.Column('out_id', db.ForeignKey(Discharge.dischargeId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    enter = db.relationship('Enter', back_populates="reports")
    discharge = db.relationship('Discharge', back_populates="reports")
    monitor = db.relationship('Monitor', back_populates="reports")

    __mapper_args__ = {
        "order_by": reportTime.desc(),
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


class LongStopReport(Report):
    """
    长期停产实体类
    attributes:
        remark: 描述
    """
    remark = db.Column('remark')

    @property
    def reportTimeStr(self):
        return self.reportTime.strftime('%Y-%m-%d %H:%M')


class DischargeReport(Report):
    """
    排口异常实体类
    attributes:
        reportTime: 申报时间（和父类用的字段不同，所以重写）
        stopReason: 停产原因
    """
    reportTime = db.Column('applay_time', default=func.now())
    stopReason = db.Column('stop_reason')

    __mapper_args__ = {
        "order_by": reportTime.desc()
    }

    # def __init__(self, **kwargs):
    #     self.__dict__.update(kwargs)

    @property
    def reportTimeStr(self):
        return self.reportTime.strftime('%Y-%m-%d')

    @property
    def stopTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.alarmType, 2, 'stopType')).first()[0]

    @property
    def attachments(self):
        return Attachment.query.filter_by(fileModelId=self.reportId,
                                          fileType=app.app.config['DISCHARGE_REPORT_FILE_TYPE'])


class FactorReport(Report):
    """
    因子异常实体类
    attributes:
        factorCode: 申报污染源（因子代码，用逗号隔开）
        exceptionReason: 异常原因
    """
    factorCode = db.Column('factor_code')
    exceptionReason = db.Column('exception_reason')

    # def __init__(self, **kwargs):
    #     self.__dict__.update(kwargs)

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
        return Attachment.query.filter_by(fileModelId=self.reportId,
                                          fileType=app.app.config['FACTOR_REPORT_FILE_TYPE']).order_by(
            Attachment.attachmentId)
