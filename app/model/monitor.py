#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.model.discharge import Discharge
from app.model.enter import Enter
from app.util.query import MonitorQuery, OrderQuery, ReportQuery, FactorQuery
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

    monitorId = db.Column('Monitor_Id', primary_key=True, autoincrement=True)
    monitorName = db.Column('Dis_Monitor_Name')
    monitorAddress = db.Column('Dis_Monitor_Address')
    monitorType = db.Column('Dis_Monitor_Type')
    monitorCategory = db.Column('outletType')
    networkType = db.Column('network_type')
    mnCode = db.Column('Mn_Code')
    isDelete = db.Column('Is_Deleted', default=0)
    enterId = db.Column('Enter_Id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="monitors")
    dischargeId = db.Column('Out_Id', db.ForeignKey(Discharge.dischargeId))
    discharge = db.relationship('Discharge', back_populates="monitors")
    orders = db.relationship('Order', lazy='dynamic', back_populates="monitor", query_class=OrderQuery)
    reports = db.relationship('Report', lazy='dynamic', back_populates="monitor", query_class=ReportQuery)
    dischargeReports = db.relationship('DischargeReport', lazy='dynamic', back_populates="monitor",
                                       query_class=ReportQuery)
    factorReports = db.relationship('FactorReport', lazy='dynamic', back_populates="monitor", query_class=ReportQuery)
    factors = db.relationship('Factor', lazy='dynamic', back_populates="monitor", query_class=FactorQuery)

    __mapper_args__ = {
        "order_by": monitorId
    }

    def __repr__(self):
        return '<Monitor %r>' % self.monitorName

    @property
    def enterName(self):
        return self.enter.enterName

    @property
    def enterAddress(self):
        return self.enter.enterAddress

    @property
    def dischargeShortName(self):
        return self.discharge.dischargeShortName

    @property
    def monitorTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.monitorType, 2, 'outletType')).first()[0]

    @property
    def monitorCategoryStr(self):
        return db.session.query(func.enterprise_archives.dbo.f_getthreeMultiName(
            self.monitorCategory, self.monitorType, 'outletType')).first()[0]

    @property
    def networkTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.networkType, 2, 'networkType')).first()[0]

    @property
    def orderCompleteCount(self):
        return self.orders.filter_by_state('5').count()

    @property
    def orderVerifyCount(self):
        return self.orders.filter_by_state('3').count()

    @property
    def orderTotalCount(self):
        return self.orders.filter_by_state('0').count()

    @property
    def dischargeReportTotalCount(self):
        return self.dischargeReports.count()

    @property
    def factorReportTotalCount(self):
        return self.factorReports.count()
