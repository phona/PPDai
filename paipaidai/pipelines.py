# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime


import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class PaipaidaiPipeline(object):

	def process_item(self, item, spider):
		item["crawled"] = datetime.utcnow()
		item["spider"] = spider.name
		return item



# class PaipaidaiPipeline(object):

# 	def __init__(self):
# 		super(self.__class__, self).__init__()
# 		self.sql_obj = SqliteClass(DATABASE)

# 	def process_item(self, item, spider):

# 		self.sql_obj["标题"] = item['title']
# 		self.sql_obj["时间"] = item['time']
# 		self.sql_obj["编号"] = item['webid']
# 		self.sql_obj["借款金额"] = item['amount']
# 		self.sql_obj["年利率"] = item['rate']
# 		self.sql_obj["借款期限"] = item['period']
# 		self.sql_obj["发标时间"] = item['begin_time']
# 		self.sql_obj["还款方式"] = item['repayment']
# 		self.sql_obj["回复内容"] = item['response']
# 		self.sql_obj["网站编号"] = 5564
# 		self.sql_obj["已发"] = 0
# 		self.sql_obj["已采"] = 1
# 		self.sql_obj["网址"] = r'http://invest.ppdai.com/loan/info?id={}'.format(item['webid'])

# 		self.sql_obj.insert()
# 		self.sql_obj.save()
# 		return item

# 	def close_spider(self, spider):
# 		self.sql_obj.close()
