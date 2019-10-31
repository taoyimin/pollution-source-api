#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:01
from app.util.query import EnterQuery, MonitorQuery, OrderQuery, DischargeQuery
from . import db


class Enter(db.Model):
    """
    企业信息实体类
    attributes:
        id: 自增长主键
        enterName: 企业名称
    """
    # __bind_key__ = 'enterprise_archives'
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_Enterprise_BasInfo'
    query_class = EnterQuery

    enterId = db.Column('Enter_id', primary_key=True)
    enterName = db.Column('Enterprise_Name')
    enterAddress = db.Column('Ent_Address')
    cityCode = db.Column('City_Code')
    areaCode = db.Column('Area_Code')
    countyCode = db.Column('County_Code')
    attentionLevel = db.Column('Attention_Level')
    enterType = db.Column('Enterprise_type')
    industryType = db.Column('Industry_Type')
    isDelete = db.Column('Is_Deleted', default=0)
    discharges = db.relationship('Discharge', lazy='dynamic', back_populates="enter", query_class=DischargeQuery)
    monitors = db.relationship('Monitor', lazy='dynamic', back_populates="enter", query_class=MonitorQuery)
    orders = db.relationship('Order', lazy='dynamic', back_populates="enter", query_class=OrderQuery)

    def __repr__(self):
        return '<Enter %r>' % self.enterName
