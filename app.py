# Import Scrapy 
from scrapy.spiders import CrawlSpider, Rule,Request
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.selector import HtmlXPathSelector
import unicodedata

#Import some function helpers
from helpers import *  
class WikipediaCrawler(CrawlSpider):
     # Crawler name
    name = 'wikipediacrawler'
    # Link where the spiders gonna start
    start_urls = fetch_start_urls()
    #Domains that the spiders must respect
    allowed_domains = ['fr.wikipedia.org']
    # The links that are similar to the start link must be parsed by parse_page function. 
    rules = (
        Rule(LinkExtractor(allow=[
             r'^https:\/\/fr\.wikipedia\.org\/wiki\/[A-Za-z0-9\_]+\/?$']), callback='parse_page', follow=True),
    )
    custom_settings = {
        'LOG_ENABLED': False,  # Disable log
        'ROBOTSTXT_OBEY':False # Don't obey the robots.txt
    }
    iteration = 0 # Number of crawled pages
    total = 0 # Number of downloaded audios

    def parse_page(self,response):
        def _clean(value):
            value = ' '.join(value)
            value = value.replace('\n', '')
            value = unicodedata.normalize("NFKD", value)
            value = re.sub(r' , ', ', ', value)
            value = re.sub(r' \( ', ' (', value)
            value = re.sub(r' \) ', ') ', value)
            value = re.sub(r' \)', ') ', value)
            value = re.sub(r'\[\d.*\]', ' ', value)
            value = re.sub(r' +', ' ', value)
            return value.strip()
        try:
            filename = re.findall(r'[A-Za-z0-9\_\-\(\)]+\/?$', response.url)[0]
            path = "./data/train/"+filename
            if create_dir(path):
                strings = []
                for i in range(0, 100):
                    try:
                        for node in response.xpath('//*[@id="mw-content-text"]/div/p[{}]'.format(i)):
                            text = _clean(node.xpath('string()').extract())
                            if len(text):
                                strings.append(text)
                    except Exception as error:
                        strings.append(str(error))
                text = _clean(strings)
                with open(path+'/'+filename+'.txt','w',encoding='utf-8') as f:
                    f.write(text)

                with open('data/link_list.txt','a',encoding='utf-8') as f:
                    f.write(response.url+'\n')
        except Exception as e:
            print(str(e))
