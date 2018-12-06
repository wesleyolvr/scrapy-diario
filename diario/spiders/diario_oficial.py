# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from os import makedirs


class DiarioOficialSpider(scrapy.Spider):
    name = 'diario-oficial'
    start_urls = ['http://dom.parnaiba.pi.gov.br/']

    def parse(self, response):
        urls= response.xpath('//ul[@class="pagination"]//a/@href').extract()
        paths = response.xpath('//div[@class="table-responsive"]//td[@class="text-center"]/text()').extract()
        links_pdf = response.xpath('//div[@class="table-responsive"]//tr//a/@href').extract()

        for arquivo in zip(links_pdf,paths):
            yield Request(response.urljoin(arquivo[0]), meta={'path':arquivo[1]},callback=self.baixa)

        for next_page in urls:
            yield Request(next_page,callback=self.parse)

    def baixa(self,response):
        path = response.meta.get('path')
        ano = path.split('-')[-1]
        try:
            makedirs(ano)
            self.logger.info('Saving PDF %s', path)
            with open('{}/{}.pdf'.format(ano,path), 'wb') as f:
                f.write(response.body)
        except OSError:
            self.logger.info('Saving PDF %s', path)
            with open('{}/{}.pdf'.format(ano,path), 'wb') as f:
                f.write(response.body)
            


