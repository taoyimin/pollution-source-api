#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:01
from sqlalchemy import func

from app.util.query import EnterQuery, MonitorQuery, OrderQuery, DischargeQuery, ReportQuery, LicenseQuery, FactorQuery
from . import db


class Enter(db.Model):
    """
    企业信息实体类
    attributes:
        enterId: 自增长主键
        enterName: 企业名称
        enterAddress: 企业地址
        enterTel: 企业电话
        contactPerson: 企业联系人
        contactPersonTel: 联系人电话
        legalPerson: 企业法人
        legalPersonTel: 法人电话
        cityCode: 市代码
        areaCode: 区代码
        countyCode: 县代码
        villageCode: 园区代码
        attentionLevel: 关注程度
        enterType: 企业类型
        industryType: 行业类别
        licenseNumber: 排污许可证编码
        creditCode: 信用代码
    """
    # __bind_key__ = 'enterprise_archives'
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_Enterprise_BasInfo'
    query_class = EnterQuery

    enterId = db.Column('Enter_id', primary_key=True, autoincrement=True)
    enterName = db.Column('Enterprise_Name')
    enterAddress = db.Column('Ent_Address')
    enterTel = db.Column('Ent_LinkPhone')
    contactPerson = db.Column('Envir_LinkMan')
    contactPersonTel = db.Column('Envir_LinkPhone')
    legalPerson = db.Column('LegalPerson')
    legalPersonTel = db.Column('legalLinkPhone')
    cityCode = db.Column('City_Code')
    areaCode = db.Column('Area_Code')
    countyCode = db.Column('County_Code')
    villageCode = db.Column('village_code')
    attentionLevel = db.Column('Attention_Level')
    enterType = db.Column('Enterprise_type')
    industryType = db.Column('Industry_Type')
    licenseNumber = db.Column('licence_no')
    creditCode = db.Column('LegalPerson_Code')
    isDelete = db.Column('Is_Deleted', default=0)
    discharges = db.relationship('Discharge', lazy='dynamic', back_populates="enter", query_class=DischargeQuery)
    monitors = db.relationship('Monitor', lazy='dynamic', back_populates="enter", query_class=MonitorQuery)
    orders = db.relationship('Order', lazy='dynamic', back_populates="enter", query_class=OrderQuery)
    reports = db.relationship('Report', lazy='dynamic', back_populates="enter", query_class=ReportQuery)
    dischargeReports = db.relationship('DischargeReport', lazy='dynamic', back_populates="enter",
                                       query_class=ReportQuery)
    longStopReports = db.relationship('LongStopReport', lazy='dynamic', back_populates="enter",
                                      query_class=ReportQuery)
    factorReports = db.relationship('FactorReport', lazy='dynamic', back_populates="enter", query_class=ReportQuery)
    licenses = db.relationship('License', lazy='dynamic', back_populates="enter", query_class=LicenseQuery)
    factors = db.relationship('Factor', lazy='dynamic', back_populates="enter", query_class=FactorQuery)

    __mapper_args__ = {
        "order_by": enterId
    }

    def __repr__(self):
        return '<Enter %r>' % self.enterName

    @property
    def industryTypeStr(self):
        return db.session.query(
            func.enterprise_archives.dbo.getAreaOrInstulyName(self.industryType, 'industry')).scalar()

    @property
    def enterTypeStr(self):
        return db.session.query(func.enterprise_archives.dbo.f_GetEnterType(self.enterType)).scalar().strip()

    @property
    def attentionLevelStr(self):
        return db.session.query(
            func.enterprise_archives.dbo.getDicName(self.attentionLevel, 2, 'AttentionLevel')).scalar()

    @property
    def cityName(self):
        return db.session.query(func.enterprise_archives.dbo.getAreaName(self.cityCode, '1')).scalar()

    @property
    def areaName(self):
        return db.session.query(func.enterprise_archives.dbo.getAreaName(self.areaCode, '2')).scalar()

    @property
    def countyName(self):
        return db.session.query(func.enterprise_archives.dbo.getAreaName(self.countyCode, '3')).scalar()

    @property
    def villageName(self):
        return db.session.query(func.enterprise_archives.dbo.getAreaName(self.villageCode, '4')).scalar()

    @property
    def districtName(self):
        return self.cityName + self.areaName

    @property
    def orderCompleteCount(self):
        return self.orders.filter_by_state('5').count()

    @property
    def orderTotalCount(self):
        return self.orders.count()

    @property
    def longStopReportTotalCount(self):
        return self.longStopReports.count()

    @property
    def dischargeReportTotalCount(self):
        return self.dischargeReports.count()

    @property
    def factorReportTotalCount(self):
        return self.factorReports.count()

    @property
    def monitorTotalCount(self):
        return self.monitors.filter_by_state('0').count()

    @property
    def monitorOnlineCount(self):
        return self.monitors.filter_by_state('1').count()

    @property
    def monitorAlarmCount(self):
        return self.monitors.filter_by_state('2').count()

    @property
    def monitorOverCount(self):
        return self.monitors.filter_by_state('3').count()

    @property
    def monitorOfflineCount(self):
        return self.monitors.filter_by_state('4').count()

    @property
    def monitorStopCount(self):
        return self.monitors.filter_by_state('5').count()
