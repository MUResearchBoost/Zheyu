import scrapy
import csv
import json
from scrapy import Request
from MU_faculty.Artemis import ReadFile
from MU_faculty.Artemis import Paper
from MU_faculty.spiders.transenddata import trans_data

class IEEESpider(scrapy.Spider):
    name = "IEEESpider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    w = ReadFile()
    local_address = 'E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/affiliation.txt'
    paper = Paper()

    def formalizing(self, data):
        for article in data:
            self.paper.get_new_paper(article['title'], article['authors'])


    def start_requests(self):
        url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?"
        api_key = '&apikey=fdppvwbgcvbq764sx4ctpppf'
        info = self.w.get_affiliation(self.local_address)
        for name, affiliation in zip(info['name'], info['affiliation']):
            author = 'author=' + name
            mu_affiliation = '&affiliation=' + affiliation + ' University of Missouri'
            #query_string = 'https://ieeexploreapi.ieee.org/api/v1/search/articles?author=Dong Xu&affiliation=University of Missouri&apikey=fdppvwbgcvbq764sx4ctpppf'
           # query_string =  'https://ieeexploreapi.ieee.org/api/v1/search/articles?author=Steve%20Borgelt&affiliation=%20Associate%20Professor%20University%20of%20Missouri&apikey=fdppvwbgcvbq7'
            query_string = url + author + mu_affiliation + api_key
            #print(query_string)
            yield Request(query_string, headers=self.headers, callback=self.parse)

    def parse(self, response):
        Json_lized = Paper()
        data_sent = trans_data()
        print(response.body)
        str0 = response.body.decode(encoding='utf-8')
        json.dumps(str0)
        papers_detail = json.loads(str0)
        if papers_detail is not None:
            papers = papers_detail['articles']
            for paper in papers:
                Json_lized.paper_list.append(Json_lized.IEEE_data(paper))
            rez = data_sent.post_data(endpoint="http://10.7.111.175:8080", data=Json_lized.paper_list)
            if rez:
                print(json.loads(rez.text))
            else:
                print("No papers")
        filename = 'abstract.txt'
      #  papers = json.JSONDecoder(response)
       # for paper in papers:
        #    print(paper)




