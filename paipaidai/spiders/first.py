# -*- coding: utf-8 -*-
import sys


from lxml import etree


import scrapy
from scrapy.http import Request
from paipaidai.items import PaipaidaiItem
from scrapy.dupefilters import RFPDupeFilter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Spider


reload(sys)
sys.setdefaultencoding('utf-8')


class FirstSpider(Spider):

    name = 'first'
    allowed_domains = ['ppdai.com']
    url = r'http://invest.ppdai.com/loan/info?id={}' 


    def start_requests(self):
        for i in xrange(88606400, 98606400):
            yield Request(url=self.url.format(i),
                          callback=self.parse, meta={'id': i})

    def parse(self, response):
        meta = response.meta
        html = etree.HTML(response.text)

        detail_group = html.xpath("//div[@class='newLendDetailbox']")

        try:

            detail_money_group = detail_group[0].xpath(
                "//div[@class='newLendDetailMoneyLeft']"
            )
            detail_refund_group = detail_group[0].xpath(
                "//div[@class='newLendDetailRefundLeft']//div[@class='item w260']"
            )
            response_group = html.xpath(
                "//div[@id='bidTable_div']//div[@class='scroll-area']/ol"
            )

            title = self.get_title(detail_group)
            complement = self.get_complement(detail_refund_group)

            print "title:", title
            print "complement:", complement

            if complement != '100':
                raise IndexError


            item = PaipaidaiItem() 
            item['title'] = title
            item['author'] = self.get_author(detail_group)
            item['amount'] = self.get_amount(detail_money_group)
            item['rate'] = self.get_rate(detail_money_group)
            item['period'] = self.get_period(detail_money_group)
            item['repayment'] = self.get_repayment(detail_refund_group)
            item['complement'] = complement
            item['webid'] = meta['id']
            item['begin_time'] = self.get_begin_time(response_group)
            item['time'] = self.get_time(response_group)
            item['response'] = self.get_response(response_group)

            yield item

        except IndexError:
            yield

    def get_title(self, detail_group):
        return detail_group[0].xpath("h3/span")[0].text

    def get_author(self, detail_group):
        return detail_group[0].xpath("//span[@class='username']")[0].text

    def get_amount(self, detail_money_group):
        amount = detail_money_group[0].xpath("dl[1]/dd/em")[0].tail
        return amount.replace(',', '')

    def get_rate(self, detail_money_group):
        rate = detail_money_group[0].xpath("dl[2]/dd")
        return rate[0].text

    def get_period(self, detail_money_group):
        period = detail_money_group[0].xpath("dl[3]/dd")
        return "".join(map(lambda x: x.strip(), period[0].itertext()))

    def get_repayment(self, detail_refund_group):
        repayment = detail_refund_group[0].text.strip()
        if '等额本息' in repayment:
            repayment = 2
        return repayment   

    def get_complement(self, detail_refund_group):
        return detail_refund_group[1].xpath("span")[0].tail.strip().strip("%")

    def get_time(self, response_group):
        return response_group[0].xpath("li[5]")[0].text

    def get_begin_time(self, response_group):
        return response_group[-1].xpath("li[5]")[0].text

    def get_response(self, response_group):
        result = []
        for each_ol in response_group:
            username = each_ol.xpath("li/span[@class='listname']")[0].text
            user_rate = each_ol.xpath("li[2]")[0].text.strip("%")
            user_amount = each_ol.xpath("li[4]")[0].text.strip("&#165;").strip("¥")
            user_time = each_ol.xpath("li[5]")[0].text

            result.append(
                '{username=%s|rate=%s|postmoney=%s|money=%s|postdate=%s|status=全部通过}' % (
                    username, user_rate, user_amount, user_amount, user_time
                ))
        return ''.join(result)
