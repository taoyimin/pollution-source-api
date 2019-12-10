#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/11/7 10:25
from app.util.query import DictionaryQuery
from . import db


class Dictionary(db.Model):
    """
    数据字典实体类
    attributes:
        dictionaryId: 自增长主键
    """
    __table_args__ = {'schema': 'enterprise_archives.dbo'}
    __tablename__ = 'T_Dictionary_Sub'
    query_class = DictionaryQuery

    dictionaryId = db.Column('Dic_Sub_Id', primary_key=True, autoincrement=True)
    dictId = db.Column('Dic_Id')
    dictCode = db.Column('Dic_Sub_Code')
    dictName = db.Column('Dic_Sub_Name')
    isDelete = db.Column('Is_Deleted', default=0)

    __mapper_args__ = {
        "order_by": dictionaryId
    }

    def __repr__(self):
        return '<Dictionary %r>' % self.dictionaryId
