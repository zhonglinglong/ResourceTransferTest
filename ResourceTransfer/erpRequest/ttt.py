# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月26日20:06:24
委托合同签约人改变接口测试用例
"""

import unittest
from common import base
from erpRequest import contractRequest
from time import sleep
from common import interface
from erpRequest import residentialRequest

residentialRequest.add_residential_number("资源划转专用楼盘","")


