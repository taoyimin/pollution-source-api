#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/6 15:13
from app.util.query import AttachmentQuery
from . import db


class Attachment(db.Model):
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_Attachment'
    query_class = AttachmentQuery

    attachmentId = db.Column('File_Id', primary_key=True, autoincrement=True)
    fileType = db.Column('File_Type')
    fileModelId = db.Column('File_Model_Id')
    fileName = db.Column('File_Name')
    url = db.Column('Url')
    isDelete = db.Column('Is_Deleted', default=0)
    size = db.Column('size')

    __mapper_args__ = {
        "order_by": attachmentId
    }

    def __repr__(self):
        return '<Attachment %r>' % self.fileName
