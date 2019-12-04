#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/6 15:13
import datetime

from app.util.query import AttachmentQuery
from . import db


class Attachment(db.Model):
    """
    附件实体类
    attributes:
        attachmentId: 自增长主键
        dataSource: 1：自行监测 2：污染源系统
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_Attachment'
    query_class = AttachmentQuery

    attachmentId = db.Column(db.Integer, name='File_Id', primary_key=True, autoincrement=True)
    fileType = db.Column('File_Type')
    fileModel = db.Column('File_Model_Type')
    fileModelId = db.Column('File_Model_Id')
    fileName = db.Column('File_Name')
    url = db.Column('Url')
    size = db.Column('size')
    isDelete = db.Column('Is_Deleted', default=0)
    dataSource = db.Column('data_source', default='2')
    createTime = db.Column('createTime', default=datetime.datetime.now())

    __mapper_args__ = {
        "order_by": attachmentId
    }

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<Attachment %r>' % self.fileName
