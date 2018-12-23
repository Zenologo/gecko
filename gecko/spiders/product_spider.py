# -*- coding: utf-8 -*-
#  For 1001pharmacies.com's products

import scrapy
import os
import csv
from w3lib.html import remove_tags
from .geckologger import GeckoLogger
from ..items import ProductItem
from .toolkit import check_doc_folder, get_subfolders

#scrapy.Spider
class ProductSpider(scrapy.Spider):
    name = "product"
    logger = GeckoLogger("product", "log_product.log")
    url_string = ""
    dir_path = ""
    file_name = ""
    site = ""

    def __init__(self, **kwarg):
        self.site = kwarg['arg']
        # Get site's name
        self.file_name = self.site.split('//')[-1].split('/')[0]
        if self.file_name[0:4] == "www.":
            self.file_name = self.file_name[4:]

        pos_point = self.file_name.find(".")
        if pos_point > 0:
            self.file_name = self.file_name[0:pos_point]
        self.file_name = "catalog_%s.csv" % (self.file_name)
        print("file_name: %s" % (self.file_name))



    def start_requests(self):
        urls = self.read_brands()
        pass
        n_url = 0
        for url in urls:
            #yield scrapy.Request(url = url['brand_link'], callback=self.parse_brand)
            pos = url['brand_link'].find("/", 11)
            if (pos != -1):
                self.url_string = url['brand_link'][:pos]
            if n_url == 1:
                pass
                #yield scrapy.Request(url = url['brand_link'], callback=self.parse_brand)
            n_url = n_url + 1
        

#    def set_url(self, url):
#        pass


    def read_brands(self):
        """ 
        Read catalog file and extract all product's url  
        """
        doc_folder_path = check_doc_folder()
        list_file = get_subfolders(doc_folder_path, self.file_name)
        print('')
        print (list_file)
        print("")

        # TODO: 解析文件，读取出每行内容，然后下载

        #self.dir_path = os.path.dirname(os.path.realpath(__file__))
        #self.logger.debug('current directory: %s' %  dir_path)
        path_directory = self.dir_path + "/../../doc/1001pharmacies/"
        #self.logger.debug(path_directory)
        dirs = os.listdir(path_directory)

        """ Find last brand file """
        last_dir = ''
        for file in dirs:
            self.logger.debug(file)
            if file[:6] == "brands" and file > last_dir:
                last_dir = file
        #self.logger.debug('last dir %s' % last_dir)
        path_directory = f'{path_directory}{last_dir}'
        path_brands_file = f'{path_directory}/brands.csv'
        #self.logger.debug(path_brands_file)
        if os.path.isfile(path_brands_file):
            #self.logger.debug("brands cvs file is exist")
            limit = 0 # just read first 3 lines
            with open(path_brands_file, newline='', encoding='utf-8') as brand_file:
                reader = csv.DictReader(brand_file)
                for row in reader:
                    yield row

        else:
            self.logger.debug("brands cvs file is not exist")



    def parse_brand(self, response):
        """ Parse brand page """
        #product_item = ProductItem()
        page = response.url.split("/")[-2]
        #self.logger.debug('page name: %s' % response.url)
        #self.logger.debug('Response status: %s' % response.status)

        # parse the page
        if response.status == 200:
            #self.logger.debug('analyser web begin')
            #self.logger.debug(response.urljoin('/catalog'))
            """ parse page """
            brand_name = response.xpath('//h2[contains(@class, "title-brand--king text--gray-medium")]/text()').extract_first()
            #products = response.xpath('//h3[contains(@class, "title order-2")]/a/@href')
            products = response.xpath('//h3[contains(@class, "title order-2")]/a')
            self.logger.debug("size of links: %s" % len(products) )

            for product in products:
                #tmp_value = product.xpath(".//text()").extract_first()
                #product_item['product_name'] = tmp_value.strip()

                product_url = self.url_string + product.xpath(".//@href").extract_first()
                #product_item['product_url'] = self.url_string + tmp_value.strip()

                yield scrapy.Request(url = product_url, callback=self.parse_product)
                #self.logger.debug(product_item['product_name'].strip())
                #self.logger.debug(product_item['product_url'].strip())
                #yield product_item

            next_page = response.xpath('//li[contains(@class, "next")]/a/@href').extract_first()
            if next_page != None:
                next_page = response.url + "/" + next_page.split("/")[-1]
                yield scrapy.Request(url=next_page, callback=self.parse_brand)

        else:
            filename = 'catalog-%s.html' % page
            with open(filename, 'wb') as f:
                f.write(response.body)


    def parse_product(self, response):
        product_item = ProductItem()
        if response.status == 200:

            value = response.xpath('//h2[contains(@itemprop, "brand")]/a/span/text()').extract_first()
            if value != None:
                product_item['brand_name'] = value.strip()

            value = response.xpath('//h1[@class="order-1" and @itemprop="name"]/text()').extract_first()
            if value != None:
                product_item['name'] = value.strip()

            product_item['url']= response.url

            value = response.xpath('//div[@itemprop="description"]').extract_first()
            if value != None:
                value = remove_tags(value)
                product_item['short_description'] = value.strip()

            value = response.xpath('//div[@itemprop="weight"]/span/text()').extract_first()
            if value != None:
                product_item['weight'] = value.strip()

            value = response.xpath('//div[@id="longDescription"]').extract_first()
            if value != None:
                value = remove_tags(value)
                product_item['long_description'] = value.strip()

            value = response.xpath('//div[@id="usage"]').extract_first()
            if value != None:
                value = remove_tags(value)
                product_item['usage'] = value.strip()

            value = response.xpath('//div[@id="composition"]').extract_first()
            if value != None:
                value = remove_tags(value)
                product_item['composition'] = value.strip()

            value = response.xpath('//p[@class="price"]/meta[@itemprop="price"]/@content').extract_first()
            if value == None:
                product_item['price'] = "INDISPONIBLE"
            else:
                product_item['price'] = value.strip()
            yield product_item

