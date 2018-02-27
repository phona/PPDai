# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import sqlite3

import scrapy


class PaipaidaiItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field()
	amount = scrapy.Field()
	rate = scrapy.Field()
	period = scrapy.Field()
	repayment = scrapy.Field()
	complement = scrapy.Field()
	response = scrapy.Field()
	webid = scrapy.Field()
	begin_time = scrapy.Field()
	time = scrapy.Field()
	crawled = scrapy.Field()
	spider = scrapy.Field()


class SqliteClass(object):

	def __init__(self, database):
		self.conn = sqlite3.connect(database)
		self.cur = self.conn.cursor()
		table_info = self.cur.execute('PRAGMA table_info(Content)').fetchall()

		self.col_name = {}
		for col in table_info:
			self.col_name[col[1]] = ""

		del self.col_name["ID"]
		
		self.place_holder = ",".join(['?' for i in range(len(self.col_name))])

	def __getitem__(self, key):
		return self.col_name[key.decode('utf-8')]

	def __setitem__(self, key, value):
		self.col_name[key.decode('utf-8')] = value

	def insert(self, table="Content"):
		keys = ",".join(self.col_name.keys())
		values = map(unicode, self.col_name.values())
		sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, keys, self.place_holder)
		self.cur.execute(sql, values)

	def select(self, field="*", where="", table="Content"):
		if where:
			sql = "SELECT {0} FROM {1} WHERE {2}".format(field, table, where)
		else:
			sql = "SELECT {0} FROM {1}".format(field, table)

		return self.cur.execute(sql)	

	def save(self):
		self.conn.commit()

	def close(self):
		self.cur.close()
		self.conn.close()