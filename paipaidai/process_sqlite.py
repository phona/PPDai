#coding:utf-8

import json
import sys


import redis
from items import SqliteClass


reload(sys)
sys.setdefaultencoding('utf-8')


def main():
	DATABASE = r'C:\Users\Heweitao\Desktop\ppdai\SpiderResult1.db3'

	rediscli = redis.StrictRedis(host='192.168.0.200', port=6379, db=0)
	sqlite_item = SqliteClass(DATABASE)

	while True:
		try:
			source, data = rediscli.blpop(["first:items"], timeout=5)
		except TypeError:
			print "done."
			break

		item = json.loads(data)
		sqlite_item["标题"] = item['title']
		sqlite_item["作者"] = item['author']
		sqlite_item["时间"] = item['time']
		sqlite_item["编号"] = item['webid']
		sqlite_item["借款金额"] = item['amount']
		sqlite_item["年利率"] = item['rate']
		sqlite_item["借款期限"] = item['period']
		sqlite_item["发标时间"] = item['begin_time']
		sqlite_item["还款方式"] = item['repayment']
		sqlite_item["回复内容"] = item['response']
		sqlite_item["完成度"] = item['complement']
		sqlite_item["网站编号"] = 124 
		sqlite_item["已发"] = 0
		sqlite_item["已采"] = 1
		sqlite_item["网址"] = r'http://invest.ppdai.com/loan/info?id={}'.format(item['webid'])

		sqlite_item.insert()
		sqlite_item.save()
		print 'process complete:', sqlite_item["网址"]

	sqlite_item.close()

if __name__ == "__main__":
	main()

