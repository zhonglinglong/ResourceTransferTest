# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月17日13:26:16
一键执行所有资源划转-委托，出租合同用例
"""

import unittest,time
from HTMLTestRunnerCN import HTMLTestRunner
from common import base,interface



test_dir = "./"
discover = unittest.defaultTestLoader.discover(test_dir,pattern="*TestCase.py")
#discover = unittest.defaultTestLoader.discover(test_dir,pattern="apartmentContractSignatoryChangeTestCase.py")
#discover = unittest.defaultTestLoader.discover(test_dir,pattern="houseContractSignatoryChangeTestCase.py")


base.host_set("mock")
interface.get_cookie()



if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = test_dir + '/' + now + "result.html"
    fp = open(filename,"wb")
    runner = HTMLTestRunner(stream=fp,title=u"资源划转接口自动化测试报告",description="用例执行情况：",tester="zhonglinglong")
    runner.run(discover)
    fp.close()
