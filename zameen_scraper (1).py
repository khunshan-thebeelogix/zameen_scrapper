# importing packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json


# This is the zameen scraper class
class ZameenScraper(scrapy.Spider):
    # This is the scraper/spider name
    name = 'zameen'

    # base URL
    # base_url = 'https://www.zameen.com/Flats_Apartments/'
    base_url = 'https://www.zameen.com/Houses_Property/'

    # These are the string query parameters we can change these parameters according to our needs
    params = {
        'price_max': 'Any',
        'area_max': 'Any',
        'baths_in': 'All',
        'beds_in': 'All'
    }

    # custom headers https://www.zameen.com/Flats_Apartments/Lahore-1-3.html?price_max=5000000&area_max=104.51592000000001&baths_in=1&beds_in=2

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    # The data will save in the csv format
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'zameen_Johar_Town_1.csv',
        # 'FEED_URI': 'zameen_DHA_Defence_1.csv',
        'FEED_URI': 'zameen_Bahria_Town_1.csv',

        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        # 'DOWNLOAD_DELAY': 2
    }

    #
    # This is the crawler's entry point
    def start_requests(self):
        # This is the loop over the page range
        # We can change the loop range to maximize or minimize the page numbers during scraping
        for page in range(1, 100):
            # This url connects to the base url and we can change it to any other url according to different
            # cities
            # generate next page URL
            # next_page = self.base_url + 'Lahore_Johar_Town-93-' + str(page) + '.html'
            # next_page = self.base_url + 'Lahore_DHA_Defence-9-' + str(page) + '.html'
            next_page = self.base_url + 'Lahore_Bahria_Town-509-' + str(page) + '.html'
            next_page += urllib.parse.urlencode(self.params)

            # This is for crawl the next page URL
            yield scrapy.Request(
                url=next_page,
                headers=self.headers,
                callback=self.parse
            )

    # These are the parse property cards
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

        # This is the list of features
        features = []

        # loop over property cards data
        for card in response.css('li[role="article"]'):
            # data extraction logic
            feature = {
                'title': card.css('h2[aria-label="Title"]::text')
                .get(),

                'price': 'PKR ' + card.css('span[aria-label="Price"]::text')
                .get(),

                'location': card.css('div[aria-label="Location"]::text')
                .get(),

                'block': card.css('div[aria-label="Location"]::text')
                .get().split(", ")[0],

                'town': card.css('div[aria-label="Location"]::text')
                .get().split(", ")[1],

                'details_url': 'https://www.zameen.com' + card.css('a::attr(href)')
                .get(),

                'bedrooms': card.css('span[aria-label="Beds"]::text')
                .get(),

                'bathrooms': card.css('span[aria-label="Baths"]::text')
                .get(),

                'area': card.css('span[aria-label="Area"] *::text')
                .get(),

                'price': 'N/A',

                'latitude': 'N/A',

                'longitude': 'N/A',

                'phone': 'N/A',

                'contact_name': 'N/A',

                'img_url': 'N/A',

                'date': card.css('span[aria-label="Listing creation date"] *::text')
                .get().split("Added: ")
            }

            # extract image URL
            try:
                feature['img_url'] = card.css('source[type="image/webp"]::attr(data-srcset)').get().replace('400x300',
                                                                                                            '800x600')

            except:
                pass

            # append next feature
            features.append(feature)

        # extract additional data
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
    # ZameenScraper.parse(ZameenScraper, '')
