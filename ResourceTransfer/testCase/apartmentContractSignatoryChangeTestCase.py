# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月26日20:06:30
出租合同签约人改变测试用例
"""

import unittest
from common import base
from time import sleep
from erpRequest import sysRequest

contract_num = "zll2018-04-28gzr050"
for_number = 160
wait_time = 1
fixed_time = 20
sign_uid = "8A2152435B0B664D015B0E7C1351006C"

class ApartmentContractSignatoryChangeZHGJ(unittest.TestCase):
    """综合管家（杭州）"""
    def setUp(self):
        """初始化测试数据函数"""
        base.consoleLog("-------------------------综合管家离职，出租合同签约人变更用例集合，执行开始----------------------")
        base.consoleLog(sysRequest.user_quit("18211112222", valus=False))
        base.consoleLog(sysRequest.user_quit("18277778888", valus=False))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_post("18211112222", "租房管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "资产管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18277778888", "综合管家（杭州）"))
        self.for_number = for_number
        self.wait_time = wait_time
        self.fixed_time = fixed_time

        self.contract_num = contract_num
        sql = 'UPDATE apartment_contract set sign_uid = "%s" where contract_num = "%s";' % (sign_uid, self.contract_num)
        base.consoleLog(base.updateSQL(sql))

        sql = 'SELECT user_id from sys_user where user_phone = "18277778888";'
        self.user_id_18277778888 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18211112222";'
        self.user_id_18211112222 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18233334444";'
        self.user_id_18233334444 = base.searchSQL(sql)[0][0]

    def tearDown(self):
        """用例执行结束"""
        base.consoleLog("-------------------------综合管家离职，出租合同签约人变更用例集合，执行结束----------------------")
        base.consoleLog("")
        base.consoleLog("")
        base.consoleLog("")

    def test_signatory_change_a(self):
        """同部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_b(self):
        """同部门，有在职上级岗位是店经理2个。验证：综合管家有出租合同，离职之后，签约人随机变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是2个店经理。验证：综合管家有出租合同，离职之后，签约人随机变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_c(self):
        """同部门，有在职上级岗位是店经理但是已经离职。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理但是已经离职。验证：综合管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_d(self):
        """上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_e(self):
        """上一级部门，有在职上级岗位是店经理2个。验证：综合管家有出租合同，离职之后，签约人随机变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人随机变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  +self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_f(self):
        """上一级部门，有离职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_g(self):
        """上一级的上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_h(self):
        """上一级的上一级部门，有在职上级岗位是店经理2个。验证：综合管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_i(self):
        """上一级的上一级部门，有离职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_j(self):
        """同部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_k(self):
        """同部门，有在职上级岗位是区经理2个。验证：综合管家有出租合同，离职之后，签约人随机变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人随机变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" +self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_l(self):
        """同部门，有在职上级岗位是区经理但是已经离职。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理但是已经离职。验证：综合管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_m(self):
        """上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_n(self):
        """上一级部门，有在职上级岗位是区经理2个。验证：综合管家有出租合同，离职之后，签约人随机变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人随机变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_o(self):
        """上一级部门，有离职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_p(self):
        """上一级的上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_q(self):
        """上一级的上一级部门，有在职上级岗位是区经理2个。验证：综合管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_r(self):
        """上一级的上一级部门，有离职上级岗位是区经理。验证：综合管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：综合管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_s(self):
        """ 只有一个城市总经理。验证：综合管家有出租合同，离职之后，签约人变成城市总经理"""
        base.consoleLog("""************************只有一个城市总经理。验证：综合管家有出租合同，离职之后，签约人变成城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_t(self):
        """ 有2个城市总经理。验证：综合管家有出租合同，离职之后，签约人随机变成城市总经理"""
        base.consoleLog("""************************有2个城市总经理。验证：综合管家有出租合同，离职之后，签约人变成随机城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "城市总经理（杭州）"))

        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.wait_time)

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222+"  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_u(self):
        """异常场景：同部门，有在职上级岗位是店经理,也有区经理。验证：综合管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：综合管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)


class ApartmentContractSignatoryChangeZFGJ(unittest.TestCase):
    """租房管家（杭州）"""
    def setUp(self):
        """初始化测试数据函数"""
        base.consoleLog("-------------------------租房管家（杭州）离职，出租合同签约人变更用例集合，执行开始----------------------")
        base.consoleLog(sysRequest.user_quit("18211112222", valus=False))
        base.consoleLog(sysRequest.user_quit("18277778888", valus=False))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_post("18211112222", "租房管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "资产管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18277778888", "租房管家（杭州）"))
        self.for_number = for_number
        self.wait_time = wait_time
        self.fixed_time = fixed_time

        self.contract_num = contract_num
        sql = 'UPDATE apartment_contract set sign_uid = "%s" where contract_num = "%s";' % (sign_uid, self.contract_num)
        base.consoleLog(base.updateSQL(sql))

        sql = 'SELECT user_id from sys_user where user_phone = "18277778888";'
        self.user_id_18277778888 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18211112222";'
        self.user_id_18211112222 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18233334444";'
        self.user_id_18233334444 = base.searchSQL(sql)[0][0]

    def tearDown(self):
        """用例执行结束"""
        base.consoleLog("-------------------------租房管家（杭州）离职，出租合同签约人变更用例集合，执行结束----------------------")
        base.consoleLog("")
        base.consoleLog("")
        base.consoleLog("")

    def test_signatory_change_a(self):
        """同部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_b(self):
        """同部门，有在职上级岗位是店经理2个。验证：租房管家有出租合同，离职之后，签约人随机变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是2个店经理。验证：租房管家有出租合同，离职之后，签约人随机变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_c(self):
        """同部门，有在职上级岗位是店经理但是已经离职。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理但是已经离职。验证：租房管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]


        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_d(self):
        """上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_e(self):
        """上一级部门，有在职上级岗位是店经理2个。验证：租房管家有出租合同，离职之后，签约人随机变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人随机变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_f(self):
        """上一级部门，有离职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_g(self):
        """上一级的上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_h(self):
        """上一级的上一级部门，有在职上级岗位是店经理2个。验证：租房管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_i(self):
        """上一级的上一级部门，有离职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_j(self):
        """同部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_k(self):
        """同部门，有在职上级岗位是区经理2个。验证：租房管家有出租合同，离职之后，签约人随机变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人随机变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_l(self):
        """同部门，有在职上级岗位是区经理但是已经离职。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理但是已经离职。验证：租房管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_m(self):
        """上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_n(self):
        """上一级部门，有在职上级岗位是区经理2个。验证：租房管家有出租合同，离职之后，签约人随机变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人随机变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_o(self):
        """上一级部门，有离职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_p(self):
        """上一级的上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_q(self):
        """上一级的上一级部门，有在职上级岗位是区经理2个。验证：租房管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_r(self):
        """上一级的上一级部门，有离职上级岗位是区经理。验证：租房管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：租房管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_s(self):
        """ 只有一个城市总经理。验证：租房管家有出租合同，离职之后，签约人变成城市总经理"""
        base.consoleLog("""************************只有一个城市总经理。验证：租房管家有出租合同，离职之后，签约人变成城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_t(self):
        """ 有2个城市总经理。验证：租房管家有出租合同，离职之后，签约人随机变成城市总经理"""
        base.consoleLog("""************************有2个城市总经理。验证：租房管家有出租合同，离职之后，签约人变成随机城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "城市总经理（杭州）"))

        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_u(self):
        """异常场景：同部门，有在职上级岗位是店经理,也有区经理。验证：租房管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：租房管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num)


class ApartmentContractSignatoryChangeZCGJ(unittest.TestCase):
    """资产管家（杭州）"""
    def setUp(self):
        """初始化测试数据函数"""
        base.consoleLog("-------------------------资产管家（杭州）离职，出租合同签约人变更用例集合，执行开始----------------------")
        base.consoleLog(sysRequest.user_quit("18211112222", valus=False))
        base.consoleLog(sysRequest.user_quit("18277778888", valus=False))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_post("18211112222", "租房管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "租房管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18277778888", "资产管家（杭州）"))
        self.for_number = for_number
        self.wait_time = wait_time
        self.fixed_time = fixed_time

        self.contract_num = contract_num
        sql = 'UPDATE apartment_contract set sign_uid = "%s" where contract_num = "%s";' % (sign_uid,self.contract_num)
        base.consoleLog(base.updateSQL(sql))

        sql = 'SELECT user_id from sys_user where user_phone = "18277778888";'
        self.user_id_18277778888 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18211112222";'
        self.user_id_18211112222 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18233334444";'
        self.user_id_18233334444 = base.searchSQL(sql)[0][0]

    def tearDown(self):
        """用例执行结束"""
        base.consoleLog("-------------------------资产管家（杭州）离职，出租合同签约人变更用例集合，执行结束----------------------")
        base.consoleLog("")
        base.consoleLog("")
        base.consoleLog("")

    def test_signatory_change_a(self):
        """同部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_b(self):
        """同部门，有在职上级岗位是店经理2个。验证：资产管家有出租合同，离职之后，签约人随机变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是2个店经理。验证：资产管家有出租合同，离职之后，签约人随机变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_c(self):
        """同部门，有在职上级岗位是店经理但是已经离职。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理但是已经离职。验证：资产管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_d(self):
        """上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_e(self):
        """上一级部门，有在职上级岗位是店经理2个。验证：资产管家有出租合同，离职之后，签约人随机变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人随机变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444+ "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_f(self):
        """上一级部门，有离职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_g(self):
        """上一级的上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_h(self):
        """上一级的上一级部门，有在职上级岗位是店经理2个。验证：资产管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人随机变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_i(self):
        """上一级的上一级部门，有离职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_j(self):
        """同部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_k(self):
        """同部门，有在职上级岗位是区经理2个。验证：资产管家有出租合同，离职之后，签约人随机变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人随机变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_l(self):
        """同部门，有在职上级岗位是区经理但是已经离职。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理但是已经离职。验证：资产管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_m(self):
        """上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_n(self):
        """上一级部门，有在职上级岗位是区经理2个。验证：资产管家有出租合同，离职之后，签约人随机变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人随机变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_o(self):
        """上一级部门，有离职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_p(self):
        """上一级的上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_q(self):
        """上一级的上一级部门，有在职上级岗位是区经理2个。验证：资产管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人随机变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444+"  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_r(self):
        """上一级的上一级部门，有离职上级岗位是区经理。验证：资产管家有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：资产管家有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_s(self):
        """ 只有一个城市总经理。验证：资产管家有出租合同，离职之后，签约人变成城市总经理"""
        base.consoleLog("""************************只有一个城市总经理。验证：资产管家有出租合同，离职之后，签约人变成城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_t(self):
        """ 有2个城市总经理。验证：资产管家有出租合同，离职之后，签约人随机变成城市总经理"""
        base.consoleLog("""************************有2个城市总经理。验证：资产管家有出租合同，离职之后，签约人变成随机城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "城市总经理（杭州）"))

        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_u(self):
        """异常场景：同部门，有在职上级岗位是店经理,也有区经理。验证：资产管家有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：资产管家有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num)


class ApartmentContractSignatoryChangeDFL(unittest.TestCase):
    """店副理（杭州）"""
    def setUp(self):
        """初始化测试数据函数"""
        base.consoleLog("-------------------------店副理（杭州）离职，出租合同签约人变更用例集合，执行开始----------------------")
        base.consoleLog(sysRequest.user_quit("18211112222", valus=False))
        base.consoleLog(sysRequest.user_quit("18277778888", valus=False))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平综合一组"))
        base.consoleLog(sysRequest.modify_user_post("18211112222", "租房管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "资产管家（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18277778888", "店副理（杭州）"))
        self.for_number = for_number
        self.wait_time = wait_time
        self.fixed_time = fixed_time

        self.contract_num = contract_num
        sql = 'UPDATE apartment_contract set sign_uid = "%s" where contract_num = "%s";' % (sign_uid,self.contract_num)
        base.consoleLog(base.updateSQL(sql))

        sql = 'SELECT user_id from sys_user where user_phone = "18277778888";'
        self.user_id_18277778888 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18211112222";'
        self.user_id_18211112222 = base.searchSQL(sql)[0][0]

        sql = 'SELECT user_id from sys_user where user_phone = "18233334444";'
        self.user_id_18233334444 = base.searchSQL(sql)[0][0]


    def tearDown(self):
        """用例执行结束"""
        base.consoleLog("-------------------------店副理（杭州）离职，出租合同签约人变更用例集合，执行结束----------------------")
        base.consoleLog("")
        base.consoleLog("")
        base.consoleLog("")


    def test_signatory_change_a(self):
        """同部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_b(self):
        """同部门，有在职上级岗位是店经理2个。验证：店副理有出租合同，离职之后，签约人随机变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是2个店经理。验证：店副理有出租合同，离职之后，签约人随机变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_c(self):
        """同部门，有在职上级岗位是店经理但是已经离职。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理但是已经离职。验证：店副理有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_d(self):
        """上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_e(self):
        """上一级部门，有在职上级岗位是店经理2个。验证：店副理有出租合同，离职之后，签约人随机变成上级部门店经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人随机变成上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_f(self):
        """上一级部门，有离职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_g(self):
        """上一级的上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_h(self):
        """上一级的上一级部门，有在职上级岗位是店经理2个。验证：店副理有出租合同，离职之后，签约人随机变成上一级的上级部门店经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人随机变成上一级的上级部门店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_i(self):
        """上一级的上一级部门，有离职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_j(self):
        """同部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222","区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid,self.user_id_18211112222,msg=self.contract_num)

    def test_signatory_change_k(self):
        """同部门，有在职上级岗位是区经理2个。验证：店副理有出租合同，离职之后，签约人随机变更成在职区经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人随机变更成在职区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num+sign_uid)

    def test_signatory_change_l(self):
        """同部门，有在职上级岗位是区经理但是已经离职。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************同部门，有离职上级岗位是区经理但是已经离职。验证：店副理有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888+ "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num+sign_uid)

    def test_signatory_change_m(self):
        """上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_n(self):
        """上一级部门，有在职上级岗位是区经理2个。验证：店副理有出租合同，离职之后，签约人随机变成上级部门区经理"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人随机变成上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "和平店"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_o(self):
        """上一级部门，有离职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "和平店"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_p(self):
        """上一级的上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222","中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num+sign_uid)

    def test_signatory_change_q(self):
        """上一级的上一级部门，有在职上级岗位是区经理2个。验证：店副理有出租合同，离职之后，签约人随机变成上一级的上级部门区经理"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人随机变成上一级的上级部门区经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18233334444", "中区（周保红）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18233334444:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18233334444 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18233334444, msg=self.contract_num + sign_uid)

    def test_signatory_change_r(self):
        """上一级的上一级部门，有离职上级岗位是区经理。验证：店副理有出租合同，离职之后，签约人不变"""
        base.consoleLog("""************************上一级的上一级部门，有在职上级岗位是区经理。验证：店副理有出租合同，离职之后签约人不变***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "区经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_department("18211112222", "中区（周保红）"))
        base.consoleLog(sysRequest.user_quit("18211112222"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))
        sleep(self.fixed_time)

        sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
        sign_uid = base.searchSQL(sql)[0][0]

        base.consoleLog("预期结果：" + self.user_id_18277778888 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18277778888, msg=self.contract_num + sign_uid)

    def test_signatory_change_s(self):
        """ 只有一个城市总经理。验证：店副理有出租合同，离职之后，签约人变成城市总经理"""
        base.consoleLog("""************************只有一个城市总经理。验证：店副理有出租合同，离职之后，签约人变成城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_t(self):
        """ 有2个城市总经理。验证：店副理有出租合同，离职之后，签约人随机变成城市总经理"""
        base.consoleLog("""************************有2个城市总经理。验证：店副理有出租合同，离职之后，签约人变成随机城市总经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "城市总经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "城市总经理（杭州）"))

        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果："  + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num + sign_uid)

    def test_signatory_change_u(self):
        """异常场景：同部门，有在职上级岗位是店经理,也有区经理。验证：店副理有出租合同，离职之后，签约人变更成在职店经理"""
        base.consoleLog("""************************同部门，有在职上级岗位是店经理。验证：店副理有出租合同，离职之后，签约人变更成在职店经理***********""")
        base.consoleLog(sysRequest.modify_user_post("18211112222", "店经理（杭州）"))
        base.consoleLog(sysRequest.modify_user_post("18233334444", "区经理（杭州）"))
        sleep(self.wait_time)
        base.consoleLog(sysRequest.user_quit("18277778888"))

        for i in range(self.for_number):
            sql = "select sign_uid from apartment_contract where contract_num = '%s'" % self.contract_num
            sign_uid = base.searchSQL(sql)[0][0]
            if sign_uid == self.user_id_18211112222:
                break
            else:
                sleep(self.wait_time)

        sql = "select contract_id from apartment_contract where contract_num = '%s' " % self.contract_num
        contract_id = base.searchSQL(sql)[0][0]
        sql = "SELECT follow_content from follow_contract where contract_id = '%s' GROUP BY create_time desc limit 1" % contract_id
        base.consoleLog(base.searchSQL(sql)[0][0])

        base.consoleLog("预期结果：" + self.user_id_18211112222 + "  测试结果：" + sign_uid)
        self.assertEqual(sign_uid, self.user_id_18211112222, msg=self.contract_num)



if __name__ == "__main__":
    unittest.main()
