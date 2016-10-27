#!/usr/bin/env python
# -*- coding: utf-8

import re
from datetime import datetime

import scrapy
from scrapy_douban.items import Movie


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com/tag/']

    rules = {
        'TAG': '//table[@class="tagCol"][1]/tbody/tr/td/a/@href',
        'PAGE_NUM': '//span[@class="break"]/following-sibling::a[2]/text()',
        'URL': '//a[@class="nbg"]/@href',
        'TITLE': '//h1/span/text()',
        'DIRECTOR': '//div[@id="info"]/span[1]/span[2]/a/text()',
        'WRITER': '//div[@id="info"]/span[2]/span[2]/a/text()',
        'PERFORMER': '//div[@id="info"]/span[3]/span[2]/a/text()',
        'GENRE': '//div[@id="info"]/span[@property="v:genre"]/text()',
        'DATE': '//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()',
        'LENGTH': '//div[@id="info"]/span[@property="v:runtime" ]/text()',
        'SUMMARY': '//span[@property="v:summary"]/text()',
        'RATING': '//strong[@property="v:average"]/text()',
        'COUNTRY_RE': re.compile(ur'制片国家/地区:</span> (.+?)<br/>'),
        'LANGUAGE_RE': re.compile(ur'语言:</span> (.+?)<br/>'),
    }

    def parse(self, response):
        links = response.xpath(self.rules['TAG']).extract()
        for link in links:
            url = ''.join(['http://movie.douban.com', link])
            yield scrapy.Request(url, callback=self.parse_tag)

    def parse_tag(self, response):
        pageNum = int(response.xpath(self.rules['PAGE_NUM']).extract_first())
        for page in range(pageNum):
            start = page * 20
            query = '?start=%s&type=T' % start
            url = ''.join([response.url, query])
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        urls = response.xpath(self.rules['URL']).extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_movie)

    def parse_movie(self, response):
        movie = Movie()
        movie['url'] = response.url
        movie['title'] = response.xpath(self.rules['TITLE']).extract_first()
        movie['director'] = response.xpath(self.rules['DIRECTOR']).extract()
        movie['writer'] = response.xpath(self.rules['WRITER']).extract()
        movie['performer'] = response.xpath(self.rules['PERFORMER']).extract()
        movie['genre'] = response.xpath(self.rules['GENRE']).extract()
        movie['release_date'] = self.get_release_date(response)
        movie['film_length'] = response.xpath(self.rules['LENGTH']).extract_first()
        movie['summary'] = self.get_summary(response)
        movie['rating'] = self.get_rating(response)
        movie['language'] = self.get_language(response)
        movie['country'] = self.get_country(response)

        yield movie

    @staticmethod
    def _serialize_date(Date):
        pat = re.compile('\d{4}\-\d{1,2}\-\d{1,2}')
        m = re.search(pat, Date)
        if m:
            result = m.group().split('-')
            year, month, day = map(lambda x: int(x), result)
            return datetime(year, month, day)
        else:
            return

    def get_release_date(self, response):
        Date = response.xpath(self.rules['DATE']).extract_first()
        if not Date:
            return
        else:
            return self._serialize_date(Date)

    def get_rating(self, response):
        rating = response.xpath(self.rules['RATING']).extract_first()
        if not rating:
            return
        else:
            return float(rating)

    def get_summary(self, response):
        con = response.xpath(self.rules['SUMMARY']).extract()
        if not con:
            return
        else:
            return ''.join(con).replace(' ', '')

    def get_language(self, response):
        s = ''.join(response.xpath('//div[@id="info"]').extract())
        m = self.rules['LANGUAGE_RE'].search(s)
        if not m:
            return
        else:
            return [ lang.strip() for lang in m.group(1).split('/') ]

    def get_country(self, response):
        s = ''.join(response.xpath('//div[@id="info"]').extract())
        m = self.rules['COUNTRY_RE'].search(s)
        if not m:
            return
        else:
            return [ country.strip() for country in m.group(1).split('/') ]