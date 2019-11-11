#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/7 10:03
from app.model.attachment import Attachment
from app.model.dictionary import Dictionary
from app.model.order import Order
from app.util.query import ProcessQuery
from . import db


class Process(db.Model):
    """
    报警管理单流程实体类
    attributes:
        processId: 自增长主键
    """
    __table_args__ = {'schema': 'pollution_report.dbo'}
    __tablename__ = 't_common_supervise_process_control'
    query_class = ProcessQuery

    processId = db.Column('id', primary_key=True, autoincrement=True)
    operatePerson = db.Column('operate_person_name')
    operateUnit = db.Column('operate_uint')
    operateType = db.Column('operate_type')
    operateTime = db.Column('operate_time')
    operateDesc = db.Column('operate_desc')
    attachmentIds = db.Column('attach')
    orderId = db.Column('supervise_id', db.ForeignKey(Order.orderId))
    order = db.relationship('Order', back_populates="processes")

    __mapper_args__ = {
        "order_by": operateTime
    }

    @property
    def operateTypeStr(self):
        unit_str = Dictionary.query.filter_by(dictId=109, dictCode=self.operateUnit).one().dictName
        type_str = Dictionary.query.filter_by(dictId=75, dictCode=self.operateType).one().dictName
        return unit_str + type_str

    @property
    def operateTimeStr(self):
        return self.operateTime.strftime('%Y-%m-%d %H:%M')

    @property
    def attachments(self):
        if self.attachmentIds:
            return Attachment.query.filter(Attachment.attachmentId.in_(self.attachmentIds.split(',')))
        else:
            return Attachment.query.filter_by(attachmentId=None)
