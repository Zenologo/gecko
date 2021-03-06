# -*- coding: utf-8 -*-
#
# This file includes all classes and functions for capture
# brand's info from site 1001pharmacies.com
#
# Thanks for the page "/marques" who lists all brand's link.
#


import scrapy
import os, sys
from datetime import datetime
from .geckologger import GeckoLogger
from ..items import BrandItem
from .toolkit import get_parse_module

#scrapy.Spider
class CatalogSpider(scrapy.Spider):
    name = "catalog"
    logger = GeckoLogger("catalog", "log_catalog.log")

    # Site's name, using in file's name what it has downloaded. for exemple: catalog_XXXX.csv
    site = '' 
    usrls=[]
    site_parse = None
    #domain = 'monoprix.fr'
    #allowed_domains = ['monoprix.fr']

    def __init__(self, **kwarg):
        self.urls = [kwarg['arg']]

        # Get site's name
        self.site = self.urls[0].split('//')[-1].split('/')[0]
        if self.site[0:4] == "www.":
            self.site = self.site[4:]
        pos_point = self.site.find(".")
        if pos_point > 0:
            self.site = self.site[0:pos_point]
        #self.set_parse_module()
        self.site_parse = get_parse_module(self.site)


    def start_requests(self):
        """
            Init task site and download site.
        """
        
        for url in self.urls:
            self.verify_path(url)
            yield scrapy.Request(url = url, callback = self.parse,  meta = {'dont_redirect': True})


    def verify_path(self, url):
        """
            Verify site's directory,  if exists. if not create it.
        """
        test_path = os.path.dirname(os.path.realpath(__file__))
        #self.logger.debug('current directory: %s' %  dir_path)
        test_path = test_path + "/../../doc"
        print ('catalog test_path: %s'  % test_path)
        if not os.path.exists(test_path) :
            os.makedirs(test_path)
        site = url.split('//')[-1].split('/')[0]
        if site[0:4] == "www.":
            site = site[4:]
        #dir_path += '/' + site + "/brands"
        if not os.path.exists(test_path):
            os.makedirs(test_path + '')

    def parse(self, response):
        """
            Parse page if sucess, if not save page's source in local.
        """
        self.logger.debug('response status: %s' %  str(response.status))
 
        brand_item = BrandItem()
        page = response.url.split("/")[-2]   

        # parse the page
        if response.status == 200:
            self.logger.debug(response.urljoin('/catalog'))

            brands = self.site_parse.get_brands(response)
            for brand in brands:
                brand_link = self.site_parse.get_brand_link(brand)
                print(brand_link)
                brand_name = self.site_parse.get_brand_name(brand)
                print(brand_name)
                brand_item['brand_link'] = response.urljoin(brand_link)
                brand_item['brand'] = brand_name
                brand_item['created_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield brand_item
        else:
            filename = 'catalog-%s.html' % page
            with open(filename, 'wb') as f:
                f.write(response.body)
 