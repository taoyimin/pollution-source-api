#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 16:01
from . import db


class Enter(db.Model):
    """
    企业信息实体类
    attributes:
        id: 自增长主键
        enterName: 企业名称
    """

    __bind_key__ = 'enterprise_archives'

    __tablename__ = 'T_Enterprise_BasInfo'

    enterId = db.Column('Enter_id', primary_key=True)
    enterName = db.Column('Enterprise_Name')
    enterAddress = db.Column('Ent_Address')
    cityCode = db.Column('City_Code')
    areaCode = db.Column('Area_Code')
    countyCode = db.Column('County_Code')
    monitors = db.relationship('Monitor', order_by='Monitor.monitorId', lazy='dynamic')

    def __repr__(self):
        return '<Enter %r>' % self.enterName
