# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月26日16:12:13
爱上租系统管理模块接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *


@log
def user_quit(user_phone,valus=True):
	"""
	提交用户离职
	:param user_phone:手机号码
	:return:
	"""
	try:
		sql = "select user_id,update_time from sys_user where user_phone = '%s'" % user_phone
		user_id_update_time = searchSQL(sql)
	except Exception as e:
		return"查询sql报错。sql:" + sql + str(e)

	if valus:
		user_status = "LEAVING"
		url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
		data = {
			"remark": "测试专用",
			"Operation_type": "DEPARTURE",
			"user_status": user_status,
			"user_id": user_id_update_time[0][0],
			"update_time": str(user_id_update_time[0][1])}
		result = myRequest(url, str(data), Value=True)

		if result["code"] == 0 and valus:
			return "账号：" + user_phone + "提交离职成功！"
	else:
		try:
			sql = 'UPDATE sys_user set user_status = "INCUMBENCY" where user_phone = "%s"; ' % user_phone
			updateSQL(sql)
			return "账号：" + user_phone + "数据库更改在职成功！"
		except Exception as e:
			return "账号：" + user_phone + "数据库更改在职异常！" + str(e) + sql

@log
def modify_user_post(phone,rolename):
    """
    修改用户岗位
    :param phone: 用户手机
    :param rolename:岗位名称
    :return:执行接口之后的返回值
    """
    sql = 'SELECT user_id from sys_user where user_phone = "%s"' % phone
    user_id = searchSQL(sql)[0][0]
    url = "http://isz.ishangzu.com/isz_base/UserController/searchNewUser.action"
    data = {"user_id":user_id}
    result = myRequest(url,str(data),Value=True)["obj"]

    sql = 'select position_id from sys_position where position_name = "%s" ' % rolename
    position_id = searchSQL(sql)[0][0]
    sql = 'SELECT update_time from sys_user where user_phone = "%s"' % phone
    update_time =str(searchSQL(sql)[0][0])
    url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
    data = {
    "position_id": position_id,
    "update_time": update_time,
    "user_id": result["sysFollows"][0]["user_id"],
    "role_id": result["role_id"],
    "Operation_type": "POSTMOVE"}

    result = myRequest(url, str(data), Value=True)
    if result["code"] ==0:
        return "账号：" + phone + " 岗位变更成：" + rolename + " 成功！"

@log
def modify_user_department(phone,department):
    """
    修改用户部门
    :param phone:用户号码
    :param department: 部门名称
    :return:执行接口之后的返回值
    """
    sql = 'SELECT user_id from sys_user where user_phone = "%s"' % phone
    user_id = searchSQL(sql)[0][0]
    url = "http://isz.ishangzu.com/isz_base/UserController/searchNewUser.action"
    data = {"user_id": user_id}
    result = myRequest(url, str(data), Value=True)["obj"]

    sql = 'select dep_id from sys_department where dep_name = "%s" ' % department
    dep_id= searchSQL(sql)[0][0]
    sql = 'SELECT update_time from sys_user where user_phone = "%s"' % phone
    update_time = str(searchSQL(sql)[0][0])
    url = "http://isz.ishangzu.com/isz_base/UserController/saveUser.action"
    data = {
    "dep_id": dep_id,
    "update_time": update_time ,
    "user_id": user_id,
    "Operation_type": "DEPMOVE"}
    result = myRequest(url, str(data), Value=True)
    if result["code"] ==0:
        return "账号" + phone + "  部门变更成：" + department + "成功！"

@log
def add_role_authority(role_name):
    """
    给角色赋所有权限
    :param role_name: 角色名称
    :return: 执行接口之后的返回值
    """
    sql = "select role_id from sys_role where role_name = '%s' limit 1" % role_name
    try:
        role_id = searchSQL(sql)[0][0]
    except BaseException as e:
        print e
        return "ERP不存在这样的角色名称！"
    sql = "select res_id from sys_res"
    res_list = searchSQL(sql)
    def reslist():
        list = []
        for i in range(len(res_list)):
            res = {}
            res["res_id"] = res_list[i][0]
            res["attributes"] = "DEPARTMENTS"
            list.append(res)
        return list

    url = "http://isz.ishangzu.com/isz_base/RoleController/saveResByRole.action"

    data ={
"role_id": role_id,
"flow_list": [{
		"activityId": "30",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "31",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "32",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "22",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "23",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "24",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "25",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "14",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "15",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "16",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "17",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "6",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "7",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "8",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "9",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "2",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "3",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "4",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "5",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "10",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "11",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "12",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "13",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "18",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "19",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "20",
		"attributes": "DEPARTMENTS"
	}, {
		"activityId": "21",
		"attributes": "DEPARTMENTS"
	}],
	"data_list": [{
		"data_type": "HOUSECONTRACT",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTCONTRACT",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTRECEIVABLE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTPAYABLE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "GENERALCONTRACT",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CUSTOMER",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CUSTOMERPERSON",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CUSTOMERFOLLOW",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CUSTOMERVIEW",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTVIEW",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTRECEIVABLEFI",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTPAYABLEFI",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTCONTRACTEND",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSECONTRACTEND",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "REIMBURSEMENTEXPENSE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "REIMBURSEMENTEXPENSEITEM",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTACHIEVEMENT",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "PUSHRENTRECORD",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTACHIEVEMENT",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "EARNEST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "EARNESTBREACH",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTCONTRACTENDLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "MANAGESHARE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSECONTRACTENDLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "GENERALCONTRACTRECEIVABLE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSEPRICEMEASURE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "REPAIRORDER",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "VACANCYACHIEVEMENTLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "BREACHACHIEVEMENTLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "BACKACHIEVEMENTLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "INSTALLMENTREPAYPLANS",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "REPAYLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "OVDLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "LENDLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "INSTREPAYLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CLEANINGORDER",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "DEDUCTIONEXPENSELIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "DEVELOPHOUSE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSERESOURCE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "VALIDHOUSE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "TRUSTEESHIPHOUSE",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "DCOVERDUERECEIVABLELIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "LOANSTATUSLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "LOCKLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "DCFINANCIALSTAGINGLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSESUBJECTACTIVITYLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "COMPLAINORDER",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "ONLINEHOUSELIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSEDEVELOPLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSESTATUSCHANGELIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "EXPLORATIONHOUSELIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "APARTMENTFOLLOWLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "HOUSEFOLLOWLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "LOCKHOUSEINSTALLED",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "SYSTEMUSERLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "PROPERTYDELIVERYLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CONTRACTAPPLICATIONORDER",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "WORKORDERLIST",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "CALLLOGINDEX",
		"perm_type": "DEPARTMENTS"
	}, {
		"data_type": "WORKORDERINDEX",
		"perm_type": "DEPARTMENTS"
	}]
}
    data["res_list"] = reslist()

    return myRequest(url,str(data),Value=True)



