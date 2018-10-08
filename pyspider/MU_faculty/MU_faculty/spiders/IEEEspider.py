import scrapy
import csv
import json
from scrapy import Request
from MU_faculty.Artemis import ReadFile


class IEEESpider(scrapy.Spider):
    name = "IEEESpider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    w = ReadFile()
    local_address = 'E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/affiliation1.txt'

    def start_requests(self):
        url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?"
        api_key = '&apikey=fdppvwbgcvbq764sx4ctpppf'
        info = self.w.get_affiliation(self.local_address)
        for name, affiliation in zip(info['name'], info['affiliation']):
            author = 'author=' + name
            mu_affiliation = '&affiliation=' + affiliation + ' University of Missouri'
            query_string = 'https://ieeexploreapi.ieee.org/api/v1/search/articles?author=Dong Xu&affiliation=University of Missouri&apikey=fdppvwbgcvbq764sx4ctpppf'

            #query_string = url + author + mu_affiliation + api_key
            print(query_string)
            yield Request(query_string, headers=self.headers, callback=self.parse)

    def parse(self, response):
        #print(response.body)
        str0 = response.body.decode(encoding='utf-8')
        json.dumps(str0)
        papers = json.loads(str0)
        paper = papers['articles']
        print(paper)

        filename = 'abstract.txt'

        yield str0
      #  papers = json.JSONDecoder(response)
       # for paper in papers:
        #    print(paper)




