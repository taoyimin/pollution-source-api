#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 15:44

from flask import Blueprint
from flask_restful import Api, fields

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

upload_return_fields = {
    'success': fields.Boolean,
    'message': fields.String,
}

from . import enter
from . import monitor
from . import discharge
from . import order
from . import report
from . import attachment
from . import process
from . import user
from . import license
from app.model.district import District
