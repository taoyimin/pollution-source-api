#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10

from . import db


class Monitor(db.Model):
    """
    监控点信息实体类
    attributes:
        monitorId: 自增长主键
    """

    __bind_key__ = 'enterprise_archives'

    __tablename__ = 'T_DisChargeMonitor'

    monitorId = db.Column('Monitor_Id', primary_key=True)
    monitorName = db.Column('Dis_Monitor_Name')
    monitorAddress = db.Column('Dis_Monitor_Address')
    enterId = db.Column('Enter_Id', db.ForeignKey('T_Enterprise_BasInfo.Enter_id'))

    def __repr__(self):
        return '<Monitor %r>' % self.monitorName
