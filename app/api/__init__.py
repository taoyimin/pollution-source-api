#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Tao Yimin
# Time  :2019/10/22 15:44

from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

from . import enter
from . import monitor
from . import user
