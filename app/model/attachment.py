#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/6 15:13
import datetime

from sqlalchemy import func

from app.util.query import AttachmentQuery
from . import db


class Attachment(db.Model):
    """
    附件实体类
    attributes:
        attachmentId: 自增长主键
        fileType: 附件所属模块
        fileModel: 附件所属模块
        fileModelId: 附件所属模块的id
        fileName: 文件名
        url: 远程路径
        size: 附件大小 单位bit
        isDelete: 是否删除
        dataSource: 1：自行监测 2：污染源系统
        createTime: 上传时间
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
    createTime = db.Column('createTime', default=func.now())

    __mapper_args__ = {
        "order_by": attachmentId
    }

    # def __init__(self, **kwargs):
    #     self.__dict__.update(kwargs)

    def __repr__(self):
        return '<Attachment %r>' % self.attachmentId
