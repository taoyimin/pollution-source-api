#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from app.util.query import OrderQuery
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

    orderId = db.Column('id', primary_key=True)
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    monitorId = db.Column('monitor_id', db.ForeignKey(Monitor.monitorId))
    alarmRemark = db.Column('alarm_desc')
    enter = db.relationship('Enter', back_populates="orders")
    monitor = db.relationship('Monitor', back_populates="orders")

    def __repr__(self):
        return '<Order %r>' % self.monitorName
