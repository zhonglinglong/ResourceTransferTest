# -*- coding:UTF-8 -*-

"""
author = crazyzhong
2018年4月25日10:54:40
调试专用
"""
import  pymysql

# 线上连接
# sqlConn = pymysql.connect(host='192.168.0.200', port=33307, user='sizhenzhen', password='Sizz#123456', db='isz_erp',charset='utf8')
# sqlCursor = sqlConn.cursor()
#
# def erp_sql(sql):
#     sqlCursor.execute(sql)
#     result = sqlCursor.fetchall()
#     if result:
#         return result

# sqlConn = pymysql.connect(host='192.168.0.200', port=33307, user='sizhenzhen', password='Sizz#123456', db='isz_decoration',charset='utf8')
# sqlCursor = sqlConn.cursor()

# def dg_sql(sql):
#     sqlCursor.execute(sql)
#     result = sqlCursor.fetchall()
#     if result:
#         return result
# #
# # sql = "select info_id,house_id from decoration_house_info where deleted=0"
# # info_id = list(dg_sql(sql))
# # #print info_id
# #
# # dhc = {}
# # for i in range(len(info_id)):
# #     sql2 = "select config_progress from new_decoration_project where info_id = '%s'" % info_id[i][0]
# #     try:
# #         dhc[info_id[i][1]] = dg_sql(sql2)[0][0]
# #     except:
# #         dhc[info_id[i][1]] = "None"
# #     print dhc[info_id[i][1]]
# #
# # ahc = {}
# # for i,j in dhc.items():
# #     try:
# #         sql3 = "SELECT fitment_status from apartment where house_id = '%s'" % i
# #         ahc[i] = erp_sql(sql3)[0][0]
# #     except:
# #         ahc[i] = "None"
# #     print ahc[i]
# #
# # print dhc
# # print ahc
# #
# # result = []
# # for x,y in dhc.items():
# #     if ahc[x] != y:
# #         print x
# #         result.append(x)
# #
# # print result


# sql = 'SELECT contract_num from house_contract where create_time > "2018-04-17 18:17:38";'
# contract_num = erp_sql(sql)
#
# err = []
# for i in range(len(contract_num)):
#     try:
#         sql = 'SELECT contract_num  from query_house_contract where contract_num = "%s"' % contract_num[i][0]
#         contract_numsss = erp_sql(sql)[0][0]
#     except:
#         print contract_num[i][0]
#         err.append(contract_num[i][0])
#
# print len(err)





import time
from time import sleep

house_contract = [1,12,33,44,55]
apament_contract = [2,4,5,6,88]

for i in range(len(house_contract)):
    if i/2 ==0:
        print "除掉反审的时间"
        break
    for j in range(len(apament_contract)):
        if len(apament_contract) == 1:
            if house_contract[i] > apament_contract[j]:
                print "重叠1"
                break
        else:
            if j/2 !=0:
                try:
                    if time.strptime(house_contract[i], "%Y-%m-%d %H:%M:%S") > time.strptime(apament_contract[j], "%Y-%m-%d %H:%M:%S") and time.strptime(house_contract[i], "%Y-%m-%d %H:%M:%S") < time.strptime(apament_contract[j+1], "%Y-%m-%d %H:%M:%S"):
                        print "重叠2"
                        break
                except:
                    pass

                if time.strptime(house_contract[i], "%Y-%m-%d %H:%M:%S") > time.strptime(apament_contract[j], "%Y-%m-%d %H:%M:%S"):
                    print "重叠3"
                    break

                try:
                    if time.strptime(house_contract[i], "%Y-%m-%d %H:%M:%S") < time.strptime(apament_contract[j], "%Y-%m-%d %H:%M:%S") and time.strptime(house_contract[i+1], "%Y-%m-%d %H:%M:%S") >  time.strptime(apament_contract[j], "%Y-%m-%d %H:%M:%S"):
                        print "重叠4"
                        break
                except:
                    pass

                if time.strptime(house_contract[i], "%Y-%m-%d %H:%M:%S") < time.strptime(apament_contract[j], "%Y-%m-%d %H:%M:%S"):
                    print "重叠5"
                    break














A = []
for i in range(5):
    sleep(1)
    A.append(time.strftime("%Y-%m-%d %H:%M:%S"))

print A
print type(time.strptime(A[0], "%Y-%m-%d %H:%M:%S"))

if  time.strptime(A[3], "%Y-%m-%d %H:%M:%S") > time.strptime(A[2], "%Y-%m-%d %H:%M:%S")  and time.strptime(A[3], "%Y-%m-%d %H:%M:%S") < time.strptime(A[4], "%Y-%m-%d %H:%M:%S"):
    print 1

