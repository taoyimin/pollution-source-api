#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from app.model.discharge import Discharge
from app.model.enter import Enter
from app.util.query import MonitorQuery, OrderQuery
from . import db


class Monitor(db.Model):
    """
    监控点信息实体类
    attributes:
        monitorId: 自增长主键
    """
    # __bind_key__ = 'enterprise_archives'
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_DisChargeMonitor'
    query_class = MonitorQuery

    monitorId = db.Column('Monitor_Id', primary_key=True)
    monitorName = db.Column('Dis_Monitor_Name')
    monitorAddress = db.Column('Dis_Monitor_Address')
    isDelete = db.Column('Is_Deleted', default=0)
    enterId = db.Column('Enter_Id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="monitors")
    dischargeId = db.Column('Out_Id', db.ForeignKey(Discharge.dischargeId))
    discharge = db.relationship('Discharge', back_populates="monitors")
    orders = db.relationship('Order', lazy='dynamic', back_populates="monitor", query_class=OrderQuery)

    def __repr__(self):
        return '<Monitor %r>' % self.monitorName
