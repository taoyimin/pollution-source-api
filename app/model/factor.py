#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.model.monitor import Monitor
from app.util.query import FactorQuery
from . import db


class Factor(db.Model):
    """
    监测因子实体类
    attributes:
        factorId: 自增长主键
        factorCode: 因子代码
        factorName: 因子名
        alarmUpper:
        alarmLower:
        overproofUpper:
        overproofLower:
        rangeUpper: 输出量程上限
        rangeLower: 输出量程下限
        measureUpper: 测量量程上限
        measureLower: 测量量程下限
        isDelete: 是否删除
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_auto_monitor_point'
    query_class = FactorQuery

    factorId = db.Column('Factor_Id', primary_key=True, autoincrement=True)
    factorCode = db.Column('Factor_Code')
    factorName = db.Column('Factor_Name')
    alarmUpper = db.Column('Alarm_Upper')
    alarmLower = db.Column('Alarm_Lower')
    overproofUpper = db.Column('Overproof_Upper')
    overproofLower = db.Column('Overproof_Lower')
    rangeUpper = db.Column('Range_Upper')
    rangeLower = db.Column('Range_Lower')
    measureUpper = db.Column('measure_Upper')
    measureLower = db.Column('measure_Lower')
    isDelete = db.Column('Is_Deleted', default=0)
    enterId = db.Column('Enter_Id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="factors")
    dischargeId = db.Column('Out_Id', db.ForeignKey(Discharge.dischargeId))
    discharge = db.relationship('Discharge', back_populates="factors")
    monitorId = db.Column('Monitor_Id', db.ForeignKey(Monitor.monitorId))
    monitor = db.relationship('Monitor', back_populates="factors")

    __mapper_args__ = {
        "order_by": factorId
    }

    def __repr__(self):
        return '<Factor %r>' % self.factorId
