import scrapy
from MU_faculty.items import MuFacultyItem
from scrapy import Request
from MU_faculty.Artemis import ReadFile
from MU_faculty.Artemis import Paper
from MU_faculty.Artemis import ClusteringPaper
import csv


class ScienceDirect(scrapy.Spider):
    name = "SCISpider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
    allowed_domain = ["www.sciencedirect.com"]
    journal = ClusteringPaper()
    narcissus = list()
    heracles = ReadFile()
    address = "E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/member_name_list.txt"
    namelist = heracles.txt(address)

    def start_requests(self):
        url = 'https://www.sciencedirect.com/'
        address = "E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/member_name_list.txt"

        sci_search = list()
        for name in self.namelist:
            name = self.heracles.scisearch(name)
            search = url + "search?authors=" + name + "&show=100&sortBy=relevance"
            sci_search.append(search)


        #url = "https://www.sciencedirect.com/search?authors=Ismail%20Akturk&show=100&sortBy=relevance"
        #yield Request(url, headers=self.headers, meta={'key': name}, callback=self.index_page_parse)
        for url in sci_search:
            k = sci_search.index(url)
            i = {'name': self.namelist[k]}
            yield Request(url, headers=self.headers, meta={"faculty": i}, callback=self.index_page_parse)

    def special_characters(self, s):
        m = s.decode('utf-8')
        return m

    def index_page_parse(self, response):
        next_page = response.xpath('//*[@id="main_content"]/main/div[1]/div[2]/div[3]/div[2]/ol/li[2]/a/@href').extract()
        contents = response.xpath('//*[@id="main_content"]/main/div[1]/div[2]/div[2]/ol/li')
        Dorian_Gray = response.meta['faculty']
        for j in contents:
            each_paper = j.xpath('./div/div[2]')
            paper = Paper()
            faculty_member_name = Dorian_Gray['name']
            journal_name = each_paper.xpath('./div[1]/ol/li[1]/a/span/text()').extract_first()
            w = each_paper.xpath('./h2[@id]/a[@href]//text()').extract()
          #  print(w)
            paper_title = self.special_characters(''.join(each_paper.xpath('./h2[@id]/a[@href]//text()').extract()))
            paper_source = ''.join(each_paper.xpath('./div[1]/ol//text()').extract())
            author_list = ''.join(each_paper.xpath('./ol[2][@class]//text()').extract())
            paper_preview = each_paper.xpath('./div[2]')
            paper_container = paper_preview.xpath('//*[@id="main_content"]/main/div[1]/div[2]/div[2]/ol/li[5]/div/div[2]/div[2]/div')
            paper_contain = ''.join(paper_container.xpath('./div/div//text()').extract())
            p = each_paper.xpath('./h2[@id]/a/@href').extract()
            page_link = "http://www.sciencedirect.com" + p[0]
            paper.get_new_paper(title=paper_title,
                                author=author_list,
                                abstract=paper_contain,
                                source=paper_source,
                                link=page_link,
                                faculty=faculty_member_name,
                                journal=journal_name)
            self.journal.author_pub(paper)
            self.journal.journal_pub(paper)
            balder = {'paper': paper}
            yield Request(page_link, headers=self.headers, meta={'key': balder}, callback=self.paper_detail_parse)

        k = len(next_page)
        if k > 0:
            yield Request(next_page[0], headers=self.headers, callback=self.index_page_parse)

    def paper_detail_parse(self, response):
        a = response.meta['key']
        paper = a['paper']
        abstract_root = response.xpath('//*[@id="abstracts"]')
        abstract = ''.join(abstract_root.xpath('./div/div/p//text()').extract())
        paper.abstract = abstract

        t1 = paper.title

        filename = "science_direct11.csv"
        with open(filename, 'a+', newline='') as f:
            if paper is not None:
                #print(paper.title)
                writer = csv.writer(f)
                writer.writerow([paper.title, paper.author, paper.source, paper.abstract])
                f.close()
            else:
                writer = csv.writer(f)
                writer.writerow(["None", "None", "None"])
                f.close()
        self.log('Saved file %s' % filename)




