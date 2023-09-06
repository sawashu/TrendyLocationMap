# -*- coding: utf-8 -*-
import scrapy
import json
import time
import os.path

import urllib
import requests

from scrapy.exceptions import CloseSpider

#from scrapy_instagram.items import Post
from scrapy_instagram.scrapy_instagram.items import Post

SCRAPER_API_KEY = 'b540792acf59a8b298e38a00a0949d86'
GOOGLE_API_KEY = 'AIzaSyDRBTWvi-YH6WfBwbXh5rIWfH6UsGxmSV4' 

'''
API = 'b540792acf59a8b298e38a00a0949d86'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    print(payload)
    proxy_url = 'http://api.scraperapi.com/?' + 'api_key=' + payload.get('api_key') + '&url='+ payload.get('url')
     
    return proxy_url
''' 

class InstagramSpider(scrapy.Spider):

    name = "hashtag"  # Name of the Spider, required value
    #fix HERE LATER!!!
    COUNT_MAX = 20
    custom_settings = {
        'BOT_NAME': 'scrapy_instagram',
        #'FEED_FORMAT': "json",
        'FEED_URI': './scraped/%(name)s/%(hashtag)s/%(date)s',
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX,
        'USER_AGENT' : '123my-capstone-project (http://example.com)',
        'CONCURRENT_REQUESTS' : 10,
        'DOWNLOAD_DELAY' : 2
    }
    checkpoint_path = './scraped/%(name)s/%(hashtag)s/.checkpoint'

    #API = 'b540792acf59a8b298e38a00a0949d86'

    # def closed(self, reason):
    #     self.logger.info('Total Elements %s', response.url)

    def __init__(self, hashtag=''):
        self.hashtag = hashtag
        if hashtag == '':
            self.hashtag = input("Name of the hashtag? ")
        self.start_urls = ["https://www.instagram.com/explore/tags/"+self.hashtag+"/?__a=1"]
        self.date = time.strftime("%d-%m-%Y_%H")
        self.checkpoint_path = './scraped/%s/%s/.checkpoint' % (self.name, self.hashtag)
        self.readCheackpoint()


    def readCheackpoint(self):
        filename = self.checkpoint_path
        if not os.path.exists(filename):
            self.last_crawled = ''
            return
        self.last_crawled = open(filename).readline().rstrip()

    # Entry point for the spider
    def parse(self, response):
        '''
        print("response")
        print("###################################################")
        print("###################################################")
        print("###################################################")
        print(response.text)
        print("###################################################")
        print("###################################################")
        print("###################################################")
        '''
        return self.parse_htag(response)

    # Method for parsing a hastag
    def parse_htag(self, response):
        print("###################################################")
        print("###################################################")
        print(response.text)
        print("###################################################")
        print("###################################################")
 
        #Load it as a json object
        graphql = json.loads(response.text)
        
       
        has_next = graphql['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        edges = graphql['graphql']['hashtag']['edge_hashtag_to_media']['edges']

        if not hasattr(self, 'starting_shorcode') and len(edges):
            self.starting_shorcode = edges[0]['node']['shortcode']
            filename = self.checkpoint_path
            f = open(filename, 'w')
            f.write(self.starting_shorcode)

        for edge in edges:

            #if self.count >= 10:
             #   raise CloseSpider('\n\n\n\ndone')
            node = edge['node']
            '''
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(node)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            '''
            shortcode = node['shortcode']
            if(self.checkAlreadyScraped(shortcode)):
                return
            #yield scrapy.Request("https://www.instagram.com/p/"+shortcode+"/?__a=1", callback=self.parse_post)
            post_url = f'https://www.instagram.com/p/{shortcode}/?__a=1'
            #request =  scrapy.Request(self.get_url(post_url), callback=self.parse_post)
            #request =  scrapy.Request(get_url(post_url), callback=self.parse_post)
            request =  scrapy.Request(post_url, callback=self.parse_post)
            request.meta['dont_redirect'] = True
            #ACTIVATE THIS! 
            #time.sleep(1)
            request.dont_filter = True
            #request.handle_httpstatus_list = [302]
            yield request
            #yield scrapy.Request("https://www.instagram.com/p/"+shortcode+"/?__a=1", meta={'dont_redirect': True,'handle_httpstatus_list': [302]},
            #    callback=self.parse_post)

        if has_next:
            print("###################################################")
            print("########go to next page for scraping ########")
            print("###################################################")
            end_cursor = graphql['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            yield scrapy.Request("https://www.instagram.com/explore/tags/"+self.hashtag+"/?__a=1&max_id="+end_cursor, callback=self.parse_htag)


    def checkAlreadyScraped(self,shortcode):
        return self.last_crawled == shortcode
           
    def parse_post(self, response):
        ''' 
        print("###################################################")
        print(vars(response))
        print("###################################################")
        print(response)
        #response = str(response).strip("'<>() ").replace('\'', '\"')
        print("###################################################")
        print("###################################################")
        print(response.body)
        print("###################################################")
        '''
        graphql = json.loads(response.text)
        #graphql = json.loads(response)
        media = graphql['graphql']['shortcode_media']
        location = media.get('location', {})
        #self.count += 1
        if location is not None:
            
            #print("###################################################")
            loc_id = location.get('id', 0)
            #print(location)
            #print("$$$$$$$$$$$$$$$$")

            #print("###################################################")
            #print(media)
            #print("###################################################")
            request = scrapy.Request("https://www.instagram.com/explore/locations/"+loc_id+"/?__a=1", callback=self.parse_post_location)
            request.dont_filter = True
                    #headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})
            request.meta['media'] = media
            #print(vars(request))
            #yield request
            yield self.makePost(media) 
        ''' 
        else:
            print("NO LOCATION-----------------------------")
        
            media['location'] = {}
            yield self.makePost(media)         
        '''  

    def parse_post_location(self, response):
        media = response.meta['media']
        location = json.loads(response.text)
        '''
        print("###################################################")
        print("###################################################")
        print(location)
        print("###################################################")
        print("###################################################")
        '''
        location = location['graphql']['location']
        #print("###################################################")
        print("###################################################")
        print(location)
        print("###################################################")
        #print("###################################################")
        media['location'] = location
        yield self.makePost(media)

    def makePost(self, media):
        location = media['location']
        caption = ''
        if len(media['edge_media_to_caption']['edges']):
            caption = media['edge_media_to_caption']['edges'][0]['node']['text']
        '''
        print("###################################################")
        print("###################################################")
        print(self.count)
        print("###################################################")
        print("###################################################")
        if self.count >= 10:
            raise CloseSpider('\n\n\n\ndone')
        '''

        display_urls=media['display_url']
        short_codes = media['shortcode']
        imgURL = "https://api.scraperapi.com/?api_key="+SCRAPER_API_KEY+"&url="+display_urls

        img_dir = "./static/img/"+self.hashtag+"/"+self.date
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        #time.sleep(5)
        image_found = "Found"
        try: 
            urllib.request.urlretrieve(imgURL, img_dir+"/"+short_codes+".jpg")
        except:
            image_found = "Not_Found"
            print("###############")
            print("image not founddddddddddddddddd")
            print("###############")
            pass

        loc_slug = location.get('slug', '')
        if loc_slug == '':
            loc_slug = location.get('name', '')
        lat, lng = None, None
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_url = f"{base_url}?address={loc_slug}&key={GOOGLE_API_KEY}"
        r = requests.get(geocode_url)
        try:
            results = r.json()['results'][0]
            lat = results['geometry']['location']['lat']
            lng = results['geometry']['location']['lng']
        except:
            print("fail to get lat, lng!!!!!!!!!!!!")
            lat = "Nothing"
            lng = "Nothing"
            pass


        return Post(id=media['id'],
                    shortcode=media['shortcode'],
                    caption=caption,
                    #display_url=media['display_url'],
                    display_url= image_found,
                    loc_id=location.get('id', 0),
                    loc_name=loc_slug,
                    #loc_lat=location.get('lat',0),
                    loc_lat=lat,
                    #loc_lon=location.get('lng',0),
                    loc_lon=lng,
                    owner_id =media['owner']['id'],
                    owner_name = media['owner']['username'],
                    taken_at_timestamp= media['taken_at_timestamp'])

'''
    def get_url(self, url):
        payload = {'api_key': API, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url
        '''
