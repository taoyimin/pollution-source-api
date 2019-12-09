#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/7 10:03
import datetime

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
        operatePerson: 操作人
        operateUnit: 操作单位
        operateType: 操作类型
        operateTime: 操作时间
        operateDesc: 操作描述
        attachmentIds: 关联的附件id（多个附件用逗号隔开）
        orderId: 关联报警管理单外键
        order: 对应的报警管理单
    """
    __table_args__ = {'schema': 'pollution_report.dbo'}
    __tablename__ = 't_common_supervise_process_control'
    query_class = ProcessQuery

    processId = db.Column('id', primary_key=True, autoincrement=True)
    operatePerson = db.Column('operate_person_name')
    operateUnit = db.Column('operate_uint')
    operateType = db.Column('operate_type')
    operateTime = db.Column('operate_time', default=datetime.datetime.now())
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
        # 处理流程的附件有两种查询方式
        # 第一种：直接根据attachmentIds字段查询
        # 第二种：根据file model id和file type查询（目前不能用这种方式查询，因为附件表file model id关联的是督办单id，对应不到流程id）
        if self.attachmentIds:
            return Attachment.query.filter(Attachment.attachmentId.in_(self.attachmentIds.split(',')))
        else:
            return Attachment.query.filter_by(attachmentId=None)
