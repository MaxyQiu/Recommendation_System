import json

from bs4 import BeautifulSoup
from fileinput import filename
import re
import os
import string
import nltk
import scrapy
from nltk.tokenize import RegexpTokenizer
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from urllib.request import urlopen as uReq
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse
from pathlib import Path

class CUResearchSpider(CrawlSpider):

  name='CUResearchSpider'
  start_urls = ['https://www.concordia.ca/research.html']
  allowed_domains=['concordia.ca']
  max_document_size = 10000  # Number of links the crawler will extract
  document_counter = 0
  urlCounter=0
  visited=[]
  def parse(self, response):

      # page = response.url.replace('.html', '').replace('/', '-').replace(':', '')


      self.urlCounter += 1
      filename = str(self.urlCounter)

      if self.urlCounter < self.max_document_size+1:
          self.visited.append(str(response.url))
          with open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/CrawledFiles/' + filename+'.json', 'w') as theFile:
              postingsList = {}
              postingsList[str(response.url)] = {}
              p=response.xpath('//p/text()').extract()
              span=response.xpath('//span/text()').extract()
              a= response.xpath('//a/text()').extract()
              h1=   response.xpath('//h1/text()').extract()
              h2=   response.xpath('//h2/text()').extract()
              h3= response.xpath('//h3/text()').extract()
              h4=   response.xpath('//h4/text()').extract()
              h5=   response.xpath('//h5/text()').extract()
              h6=   response.xpath('//h6/text()').extract()
              postingsList[str(response.url)] = p+span+a+h1+h2+h3+h4+h5+h6

              json.dump(postingsList, theFile)
      else:
          raise CloseSpider('At the upper limit')

      for url in response.xpath('//a/@href').extract():

          if url.endswith('.html') and url not in self.visited:
              url = response.urljoin(url)
              yield scrapy.Request(url, callback=self.parse)
          else:
              continue

class AISPider(CrawlSpider):
    name = 'CUResearchSpider'
    start_urls = ['https://aitopics.org/search']
    # start_urls=['http://www.concordia.ca/artsci/science-college/about/life-at-the-college.html']
    allowed_domains = ['aitopics.org']
    max_document_size = 10000  # Number of links the crawler will extract
    document_counter = 0
    urlCounter = 0

    def parse(self, response):

        # page = response.url.replace('.html', '').replace('/', '-').replace(':', '')

        self.urlCounter += 1
        filename = str(self.urlCounter)

        if self.urlCounter < self.max_document_size+1:
            with open('/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/AICrawledFiles/' + filename + '.json',
                      'w') as theFile:
                postingsList = {}
                postingsList[str(response.url)] = {}
                p = response.xpath('//p/text()').extract()
                span = response.xpath('//span/text()').extract()
                a = response.xpath('//a/text()').extract()

                postingsList[str(response.url)] = p + span + a

                json.dump(postingsList, theFile)
        else:
            raise CloseSpider('At the upper limit')

        for url in response.xpath('//a/@href').extract():

            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse)



if __name__ == '__main__':

     parsing= CrawlerProcess()
     parsing.crawl(AISPider)
     parsing.start()
