#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 19:10
from app.model.enter import Enter
from app.util.query import MonitorQuery, DischargeQuery
from . import db


class Discharge(db.Model):
    """
    排口信息实体类
    attributes:
        dischargeId: 自增长主键
    """
    # __bind_key__ = 'enterprise_archives'
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_DisChargeOut'
    query_class = DischargeQuery

    dischargeId = db.Column('Out_Id', primary_key=True)
    dischargeName = db.Column('Dis_Out_Name')
    dischargeAddress = db.Column('Dis_Out_Address')
    isDelete = db.Column('Is_Deleted', default=0)
    enterId = db.Column('Enter_Id', db.ForeignKey(Enter.enterId))
    enter = db.relationship('Enter', back_populates="discharges")
    monitors = db.relationship('Monitor', lazy='dynamic', back_populates="discharge", query_class=MonitorQuery)

    def __repr__(self):
        return '<Discharge %r>' % self.dischargeName
