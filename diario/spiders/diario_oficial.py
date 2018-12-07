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
            
        yield Request(response.url, callback=self.anos_anteriores)
    
    def anos_anteriores(self,response):
        name_paths = response.xpath('//div[@class="modal-body"]//a/text()').extract()
        links_pdf = response.xpath('//div[@class="modal-body"]//a/@href').extract()
        makedirs('Diarios anteriores')
        for arquivo in zip(links_pdf, name_paths):
            yield Request(response.urljoin(arquivo[0]), meta={'name_file':arquivo[1]},callback=self.baixa_anos_anteriores)


    def baixa_anos_anteriores(self,response):
        name_file = response.meta.get('name_file')
        self.logger.info('Saving PDF %s', name_file.encode('utf-8'))
        with open('{}/{}'.format('Diarios anteriores',name_file.encode('utf-8')), 'wb') as f:
            f.write(response.body)

    def baixa(self,response):
        name_file = response.meta.get('path')
        ano = name_file.split('-')[-1]
        try:
            makedirs(ano)
            self.logger.info('Saving PDF %s', name_file)
            with open('{}/{}'.format(ano,name_file), 'wb') as f:
                f.write(response.body)
        except OSError:
            self.logger.info('Saving PDF %s', name_file)
            with open('{}/{}'.format(ano,name_file), 'wb') as f:
                f.write(response.body)
            


