import csv
import scrapy
from MU_faculty.Artemis import ReadFile
from MU_faculty.Artemis import Paper
from MU_faculty.spiders.transenddata import trans_data
from scrapy import Request
from MU_faculty.Artemis import differentiate_affiliation
from MU_faculty.Artemis import Faculty, remove_duplicateid
import json
import os


class ScopusSpider(scrapy.Spider):
    name = "ScopusSpider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
        'Accept' : 'application/json'
    }
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    w = ReadFile()
   # local_address = 'E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/data_collected/engineering_test.txt'
    path = os.path.abspath('.')
    local_address = path + '\\spiders\\data_collected\\engineering_test.txt'
    paper = Paper()
    api_key = '9008218724e236887e4c74f3eb98c09d'

    def formalizing(self, data):
        for article in data:
            self.paper.get_new_paper(article['title'], article['authors'])

    def start_requests(self):
        url = "https://api.elsevier.com/content/search/author?"

        info = self.w.get_affiliation(self.local_address)
        for name in info['name']:
            # get the first name and last name
            fragment = name.split(' ', 3)
            first_name = 'authfirst' + '(' + fragment[0] + ')'
            last_name = 'authlast' + '(' + fragment[len(fragment)-1] + ')'
            mu_affiliation = 'affil' + '(University of Missouri)'
            query_suffix = "query=" + last_name + '%20and%20' + first_name + '%20and%20' + mu_affiliation
            query_string = url + query_suffix + '&apiKey=' + self.api_key
            print(query_string)
            yield Request(query_string, headers=self.headers, callback=self.author_affiliation)

    def author_affiliation(self, response):
        member = Faculty()
        members = list()
        result = json.loads(response.body)
        search_results = result['search-results']
        authors = search_results['entry']
        for author in authors:
            affiliation = author['affiliation-current']
            if differentiate_affiliation(affiliation) > 0:
                author_id = author['dc:identifier']
                author_eid = author['eid']
                member.id_edit(author_id, 'author_id')
                member.id_edit(author_eid, 'eid')
                members.append(member)


        author = remove_duplicateid(members)
        query_prefix = 'http://api.elsevier.com/content/author/author_id/'
        for each_one in members:
            query_suffix = each_one['author_id'] + '?' + 'apiKey=' + self.api_key + '&start=0&count=200&view=DOCUMENTS '
            query_string = query_prefix + query_suffix
            yield Request(query_string, headers=self.headers, callback=self.author_publication)

    def author_publication(self, response):
        result = json.loads(response.body)
        eid_list = list()
        for p in result:
            eid_list.append(p['eid'])

        query_prefix = 'https://api.elsevier.com/content/abstract/eid/'
        for eid in eid_list:
            query_string = query_prefix + eid + '?' + 'apiKey=' + self.api_key
            yield Request(query_string, headers=self.headers, callback=self.paper_detail)

    def paper_detail(self, response):
        result = json.loads(response.body)
        #self.paper