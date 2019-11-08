#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.util.query import OrderQuery, ProcessQuery
from app.model.enter import Enter
from app.model.monitor import Monitor
from . import db


# class OrderDelete(TypeDecorator):
#     impl = Integer
#
#     def __init__(self, length=None, format='%H:%M:%S', **kwargs):
#         super().__init__(length, **kwargs)
#         self.format = format
#
#     def process_literal_param(self, value, dialect):
#         # allow passing string or time to column
#         if isinstance(value, basestring):  # use str instead on py3
#             value = datetime.strptime(value, self.format).time()
#
#         # convert python time to sql string
#         return value.strftime(self.format) if value is not None else None
#
#     process_bind_param = process_literal_param
#
#     def process_result_value(self, value, dialect):
#         # convert sql string to python time
#         return datetime.strptime(value, self.format).time() if value is not None else None


class Order(db.Model):
    """
    报警管理单实体类
    attributes:
        monitorId: 自增长主键
    """
    # __bind_key__ = 'pollution_report'
    __table_args__ = {'schema': 'pollution_report.dbo'}
    __tablename__ = 't_monitor_data_common_supervise'
    query_class = OrderQuery

    orderId = db.Column('id', primary_key=True, autoincrement=True)
    orderLevel = db.Column('order_level')
    orderState = db.Column('order_state')
    alarmType = db.Column('alarm_type')
    alarmDateStr = db.Column('alarm_date')
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    alarmRemark = db.Column('alarm_desc')
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
