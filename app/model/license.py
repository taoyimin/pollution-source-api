#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from sqlalchemy import func

from app.model.attachment import Attachment
from app.model.enter import Enter
from app.util.query import LicenseQuery, LicenseFactorQuery
from . import db


class License(db.Model):
    """
    排污许可证实体类
    attributes:
        licenseId: 自增长主键
        issueUnit：发证单位
        issueTime：发证时间
        licenseTime：领证时间
        validStartTime：有效期开始时间
        validEndTime：有效期结束时间
        licenseManagerType：许可证管理类别
        licenseNumber：许可证编号
        dischargeMode：排污方式
        dischargeCode：允许排污口（编号）
        yearWaterDischargeTotal：年允许废水排放量
        dayWaterDischargeTotal：日允许废水排放量
        firstYearDischargeTotal：第一年排放许可总量
        secondYearDischargeTotal：第二年排放许可总量
        thirdYearDischargeTotal：第三年排放许可总量
        allowSewage：允许排污去向
        notApproveReason：尚未核发的原因
        remark：备注
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_pollution_discharge_license'
    query_class = LicenseQuery

    licenseId = db.Column('license_id', primary_key=True, autoincrement=True)
    issueUnit = db.Column('issue_unit')
    issueTime = db.Column('issue_time')
    licenseTime = db.Column('license_time')
    validStartTime = db.Column('valid_start_time')
    validEndTime = db.Column('valid_end_time')
    licenseManagerType = db.Column('licence_management_type')
    licenseNumber = db.Column('license_number')
    dischargeMode = db.Column('emisse_mode')
    dischargeCode = db.Column('discharge_code')
    yearWaterDischargeTotal = db.Column('year_wat_emite_total')
    dayWaterDischargeTotal = db.Column('day_wat_emite_total')
    firstYearDischargeTotal = db.Column('one_year_total_emission')
    secondYearDischargeTotal = db.Column('two_year_total_emission')
    thirdYearDischargeTotal = db.Column('three_year_total_emission')
    allowSewage = db.Column('allow_sewage')
    notApproveReason = db.Column('approve_remark')
    remark = db.Column('remark')
    isDelete = db.Column('is_deleted', default=0)
    enterId = db.Column('enter_id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="licenses")
    licenseFactors = db.relationship('LicenseFactor', lazy='dynamic', back_populates="license",
                                     query_class=LicenseFactorQuery)

    __mapper_args__ = {
        "order_by": licenseId
    }

    def __repr__(self):
        return '<License %r>' % self.licenseId

    @property
    def enterName(self):
        return self.enter.enterName

    @property
    def issueUnitStr(self):
        return db.session.query(func.enterprise_archives.dbo.getDicName(self.issueUnit, 2, 'issueUnit')).first()[0]

    @property
    def issueTimeStr(self):
        return self.issueTime.strftime('%Y-%m-%d')

    @property
    def licenseTimeStr(self):
        return self.licenseTime.strftime('%Y-%m-%d')

    @property
    def validTimeStr(self):
        return self.validStartTime.strftime('%Y-%m-%d') + '至' + self.validEndTime.strftime('%Y-%m-%d')

    @property
    def licenseManagerTypeStr(self):
        return db.session.query(
            func.enterprise_archives.dbo.getDicName(self.licenseManagerType, 2, 'licenceManagementType')).first()[0]

    @property
    def attachments(self):
        return Attachment.query.filter_by(fileModelId=self.licenseId, fileType='pollutionPermitFile').order_by(
            Attachment.attachmentId)


class LicenseFactor(db.Model):
    """
    排污许可污染物实体类
    attributes:
        factorId: 自增长主键
        factorName：污染物名称
        yearAllowDischargeTotal：年允许排放总量
        dayAllowDischargeTotal：日允许最大排放量
        allowDischargeDensity：允许排放浓度
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 't_pollution_discharge_license_factor'
    query_class = LicenseFactorQuery

    factorId = db.Column('factor_id', primary_key=True, autoincrement=True)
    factorName = db.Column('factor_code')
    yearAllowDischargeTotal = db.Column('year_emite_total')
    dayAllowDischargeTotal = db.Column('day_max_emite')
    allowDischargeDensity = db.Column('max_emite')
    isDelete = db.Column('is_deleted', default=0)
    licenseId = db.Column('license_id', db.ForeignKey(License.licenseId))
    license = db.relationship('License', back_populates="licenseFactors")

    __mapper_args__ = {
        "order_by": factorId
    }

    def __repr__(self):
        return '<LicenseFactor %r>' % self.factorId
