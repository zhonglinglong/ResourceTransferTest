# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月29日18:37:04
爱上租ERP写死的接口
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from common.interface import *
import datetime


@log
def update_apartment_contract_sign_uid(contract_num):
    """
    修改委托合同签约人
    :param contract_num:
    :return:
    """
    url = "http://isz.ishangzu.com/isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action"
    data = {
	"contract_id": "FF808081630203E90163021073080033",
	"house_id": "FF808081630143A5016301D85704026B",
	"residential_id": "FF80808162FB87C8016301D761DE0020",
	"building_id": "FF80808162FB12D1016301D762C9039E",
	"city_code": "330100",
	"area_code": "330108",
	"entrust_type": "ENTIRE",
	"apartment_id": "FF808081630143A5016302106D0E15F1",
	"contract_status": "EFFECTIVE",
	"passContract": "1",
	"server_flag": "1",
	"apartment_rent_price": "8000",
	"contract_type": "NEWSIGN",
	"apartment_code": "HZBJ1804260294",
	"property_address": "资源划转专用楼盘1幢A104室",
	"production_address": "产权地址",
	"apartment_type": "MANAGE",
	"input_dep_name": "内部产品测试组",
	"input_user_name": "test_钟玲龙",
	"sign_did": "42",
	"sign_uid": "8A2152435DC1AEAA015DE3B72E396299",
	"results_belong_did": "FF8080816250A7770162514D305953B0",
	"contract_num": "zll2018-04-26tsd713",
	"sign_body": "ISZTECH",
	"sign_date": "2018-02-01",
	"apartment_check_in_date": "2018-01-01",
	"rent_start_date": "2018-02-01",
	"rent_end_date": "2019-01-31",
	"payment_date": "2018-02-01",
	"deposit_type": "ONE",
	"payment_type": "NORMAL",
	"payment_cycle": "SEASON",
	"financing_type": "NONE",
	"cash_rent": "800",
	"deposit": "8000.00",
	"agency_fee": "0.00",
	"month_server_fee": "800.00",
	"month_server_fee_discount": "100%",
	"load_interest": "8.00",
	"remark": "测试",
	"dispostIn": 1,
	"sign_name": "testauto",
	"sign_id_type": "PASSPORT",
	"sign_id_no": "15626719073",
	"sign_phone": "13103152253",
	"sign_is_customer": "Y",
	"address": "资源划转专用楼盘1幢A104室",
	"houseContractList": [{
		"contract_id": "FF8080816300B45F016302106BED0092",
		"contract_num": "zll2018-04-26jrg887",
		"cost_account": 100,
		"delay_date": "2020-01-01",
		"dep_name": "杭州城市公司",
		"dispostIn": 0,
		"entrust_end_date": "2020-01-01",
		"entrust_start_date": "2018-01-01",
		"recreate": false,
		"remark": "备注",
		"sign_date": "2018-01-01",
		"start_end_date": "2018-01-01~2020-01-01",
		"user_name": "谭微平"
	}],
	"apartmentContractRentInfoList": [{
		"agencyFeeMoney": "0.00",
		"contract_id": "FF808081630203E90163021073080033",
		"deposit": "8000.00",
		"details": [],
		"end_date": "2019-01-31",
		"end_date_cn": "2019年01月31日",
		"money": 8000,
		"money_cycle": "SEASON",
		"money_type": "RENT",
		"month_server_fee": "800.00",
		"payment_date": "2018-02-01",
		"rent_end_date": "2019-01-31",
		"rent_info_id": "FF808081630203E90163021073AE0035",
		"rent_start_date": "2018-02-01",
		"start_date": "2018-02-01",
		"start_date_cn": "2018年02月01日",
		"firstRow": true,
		"rowIndex": 0,
		"sign_date": "2018-02-01"
	}],
	"model": "1"}

    result = myRequest(url,str(data),method="put",Value=True)
    if result["code"] == 0:
        return "委托合同号：" + contract_num + "。修改签约人成功！"
    else:
        return  "委托合同号：" + contract_num + "。修改签约人失败！错误返回：" + str(result["obj"])