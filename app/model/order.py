#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.util.query import OrderQuery, ProcessQuery
from app.model.enter import Enter
from app.model.monitor import Monitor
from . import db


class Order(db.Model):
    """
    报警管理单实体类
    attributes:
        orderId: 自增长主键
        orderLevel:
        orderLevel: 报警管理单状态
        alarmType: 报警类型
        alarmDateStr: 报警日期
        alarmRemark: 报警描述
        enterId：关联企业外键
        monitorId：关联监控点外键
        enter：对应的企业
        monitor：对应的监控点
        processes：处理流程集合
    """
    __table_args__ = {'schema': 'pollution_report.dbo'}
    __tablename__ = 't_monitor_data_common_supervise'
    query_class = OrderQuery

    orderId = db.Column('id', primary_key=True, autoincrement=True)
    orderLevel = db.Column('order_level')
    orderState = db.Column('order_state')
    alarmType = db.Column('alarm_type')
    alarmDateStr = db.Column('alarm_date')
    alarmRemark = db.Column('alarm_desc')
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    enter = db.relationship('Enter', back_populates="orders")
    monitor = db.relationship('Monitor', back_populates="orders")
    processes = db.relationship('Process', lazy='dynamic', back_populates="order", query_class=ProcessQuery)

    __mapper_args__ = {
        "order_by": alarmDateStr.desc()
    }

    def __repr__(self):
        return '<Order %r>' % self.enterName

    @property
    def enterName(self):
        return self.enter.enterName

    @property
    def enterAddress(self):
        return self.enter.enterAddress

    @property
    def monitorName(self):
        return self.monitor.monitorName

    @property
    def districtName(self):
        return self.enter.cityName + self.enter.areaName

    @property
    def orderLevelStr(self):
        return db.session.query(func.pollution_monitor.dbo.getDicName(self.orderLevel, 2, 'orderLevel')).first()[0]

    @property
    def orderStateStr(self):
        return db.session.query(func.pollution_monitor.dbo.getDicName(self.orderState, 2, 'distOrderStatus')).first()[0]

    @property
    def alarmTypeStr(self):
        return db.session.query(func.pollution_monitor.dbo.f_GetAlarmType(self.alarmType)).first()[0]
