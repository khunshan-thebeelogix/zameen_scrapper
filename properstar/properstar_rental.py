
# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json
import csv
from tempfile import NamedTemporaryFile

# zameen scraper class
class ZameenScraper(scrapy.Spider):
    # scraper/spider name
    name = 'zameen'
    
    # base URL
    # base_url = 'https://www.zameen.com/Flats_Apartments/'
    # base_url = 'https://www.properstar.com/turkey/istanbul/buy/house'
    # base_url = 'https://www.properstar.com/turkey/buy/apartment-house'
    base_url = 'https://www.properstar.com/turkey/buy/apartment-house'
    # base_url = "https://www.properstar.com/turkey/rent/apartment-house"
    # base_url ='https://www.properstar.com/turkey/rent/house'
    # base_url = 'https://www.properstar.com/turkey/rent/commercial'
    
    # string query parameters
    params = {
        'price_max': 'Any',
        'area_max': 'Any',
        'baths_in': 'All',
        'beds_in': 'All'
    }
    
    # custom headershttps://www.zameen.com/Flats_Apartments/Lahore-1-3.html?price_max=5000000&area_max=104.51592000000001&baths_in=1&beds_in=2

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        # 'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'zameen_Sudhnoti.csv',
        
        # uncomment below to limit the spider speed
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        # 'DOWNLOAD_DELAY': 2
    }
    
    # crawler's entry point
    def start_requests(self):
        field_names = ['title', 'price', 'location', 'highlights', 'house_type', 'area', 'bath','rooms_or_beds', 
                       'rooms_or_bed','details_url', 'image_url', 'date']
        with open('turkey_apartment_buy_data_1.csv', 'w', encoding='utf-8') as csvfile:
            # reader = csv.DictReader(csvfile, fieldnames=field_names)
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader()
        # loop over the page range
        for page in range(1, 5000):
            # generate next page URL
            next_page = self.base_url + '?p=' + str(page)
            # next_page += urllib.parse.urlencode(self.params)
            
            # crawl the next page URL
            yield scrapy.Request(
                url=next_page,
                headers=self.headers,
                callback=self.parse
            )
    
    # parse property cards
    def parse(self, response):
        '''
        # write HTML response to local file
        with open('res.html', 'w') as f:
            f.write(response.text)
        '''
        
        '''
        # local HTML content
        content = ''
        
        # load local HTML file to debug data extraction logic
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''
        
        # features list
        features = []
        
        # loop over property cards data
        # for card in response.css('article[class="item-adaptive card-full"]') or response.css('article[class="item-adaptive card-extended"]'):
        for card in response.css('article[class="item-adaptive card-extended"]') or response.css('article[class="item-adaptive card-basic vendor-hidden"]'):
            # data extraction logic
            feature = {
                'title': card.css('a[class="link listing-title stretched-link"]::text')
                             .get(),
                
                
                # 'price': card.css('span[class="title-price"]//span::text')
                #              .get(),
                
                'price': card.css('div.title-price span:only-child::text')
                             .get(),
                
                'location': card.css('div[class="item-location"]::text')
                                    .get(),
                
                'highlights': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • "),
                
                'house_type': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • ")[0],
                
                'area': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • ")[-1],
                
                'bath': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • ")[-2],
                
                'rooms_or_beds': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • ")[-3],
                
                'rooms_or_bed': card.css('p[class="item-highlights"]::text')
                                    .get().split(" • ")[1],

                'details_url': 'https://www.properstar.com' + card.css('a::attr(href)')
                                   .get(),
                
                'image_url': 'https:' + card.css('div.lazybackground img::attr(src)')
                                    .get(),
                
                'date': card.css('span[class="badge badge-time"]::text')
                             .get(),
                
                # 'house type': card.css('p[class="item-highlights"]::text')
                #                     .get()[0:5].strip(),

                
                
            }
            features.append(feature)
        print(features)
        featur = features
        field_names = ['title', 'price', 'location', 'highlights', 'house_type', 'area', 'bath','rooms_or_beds', 
                       'rooms_or_bed','details_url', 'image_url', 'date']
        # tempfile = NamedTemporaryFile(mode='w', delete=False)
        with open('turkey_apartment_buy_data_1.csv', 'a', encoding='utf-8') as csvfile:
            # reader = csv.DictReader(csvfile, fieldnames=field_names)
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            # writer.writeheader()
            writer.writerows(featur)
        
        try:
            json_data = ''.join([
                script.get() for script in
                response.css('script::text')
                if 'window.state = ' in script.get()
            ])
            
            # extract JSON part
            json_data = json_data.split('window.state = ')[-1].split('}};')[0] + '}}'
            
            # parse JSON to dictionary
            json_data = json.loads(json_data)
            
            # extrract cards data
            json_data = json_data['algolia']['content']['hits']
            
            # loop over the features
            for index in range(0, len(features)):
                features[index]['price'] = json_data[index]['price']
                features[index]['latitude'] = json_data[index]['geography']['lat']
                features[index]['longitude'] = json_data[index]['geography']['lng']
                features[index]['phone'] = ', '.join(json_data[index]['phoneNumber']['mobileNumbers'])
                features[index]['contact_name'] = json_data[index]['contactName']
                
                # write feature to output CSV file
                yield features[index]
        except:
            pass

# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ZameenScraper)
    process.start()
    
    # debugging selectors
    #ZameenScraper.parse(ZameenScraper, '')
    

