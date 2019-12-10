#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.model.enter import Enter
from app.util.query import MonitorQuery, DischargeQuery, ReportQuery, FactorQuery
from . import db


class Discharge(db.Model):
    """
    排口信息实体类
    attributes:
        dischargeId: 自增长主键
        dischargeName：排口名称
        dischargeShortName：排口简称
        dischargeAddress：排口地址
        dischargeNumber：排口编号
        dischargeType：排口类型
        outType：排放类型 0出口、1进口
        denoterInstallType：标志牌安装形式
        dischargeRule：排放规律
        dischargeCategory：排口类别
        longitude：经度
        latitude：纬度
        dischargeMonitorType：0：人工监测 1：自动监测
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_DisChargeOut'
    query_class = DischargeQuery

    dischargeId = db.Column('Out_Id', primary_key=True, autoincrement=True)
    dischargeName = db.Column('Dis_Out_Name')
    dischargeShortName = db.Column('dis_out_short_name')
    dischargeAddress = db.Column('Dis_Out_Address')
    dischargeNumber = db.Column('Dis_Out_Id')
    dischargeType = db.Column('Dis_Out_Type')
    outType = db.Column('out_type')
    denoterInstallType = db.Column('Denoter_InstallType')
    dischargeRule = db.Column('Dis_Out_Rule')
    dischargeCategory = db.Column('outletType')
    longitude = db.Column('Dis_Out_Longitude')
    latitude = db.Column('Dis_Out_Latitude')
    dischargeMonitorType = db.Column('Dis_Out_MonitorType')
    isDelete = db.Column('Is_Deleted', default=0)
    enterId = db.Column('Enter_Id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="discharges")
    monitors = db.relationship('Monitor', lazy='dynamic', back_populates="discharge", query_class=MonitorQuery)
    reports = db.relationship('Report', lazy='dynamic', back_populates="discharge", query_class=ReportQuery)
    dischargeReports = db.relationship('DischargeReport', lazy='dynamic', back_populates="discharge",
                                       query_class=ReportQuery)
    factorReports = db.relationship('FactorReport', lazy='dynamic', back_populates="discharge", query_class=ReportQuery)
    factors = db.relationship('Factor', lazy='dynamic', back_populates="discharge", query_class=FactorQuery)

    __mapper_args__ = {
        "order_by": dischargeId
    }

    def __repr__(self):
        return '<Discharge %r>' % self.dischargeName

    @property
    def enterName(self):
        return self.enter.enterName

    @property
    def enterAddress(self):
        return self.enter.enterAddress

    @property
    def dischargeTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.dischargeType, 2, 'outletType')).first()[0]

    @property
    def dischargeCategoryStr(self):
        return db.session.query(func.enterprise_archives.dbo.f_getthreeMultiName(
            self.dischargeCategory, self.dischargeType, 'outletType')).first()[0]

    @property
    def dischargeRuleStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.dischargeRule, 2, 'disOutRule')).first()[0]

    @property
    def denoterInstallTypeStr(self):
        return db.session.query(
            func.enterprise_archives.dbo.getDicName(self.denoterInstallType, 2, 'denoterInstallType')).first()[0]

    @property
    def outTypeStr(self):
        if self.outType == '0':
            return '进口'
        elif self.outType == '1':
            return '出口'
        else:
            return '未知'

    @property
    def dischargeReportTotalCount(self):
        return self.dischargeReports.count()

    @property
    def factorReportTotalCount(self):
        return self.factorReports.count()
