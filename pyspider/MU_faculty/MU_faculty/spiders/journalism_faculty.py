import scrapy
from MU_faculty.items import MuFacultyItem
from scrapy import Request
from MU_faculty.Artemis import Faculty


class JournalismSpider(scrapy.Spider):
    name = "JournalismSpider_faculty_members"
    allowed_domain = ['journalism.missouri.edu']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

    def start_requests(self):                   # get the start pages
        url = "https://journalism.missouri.edu/jschool/directory/"
        urls = list()
        urls.append(url)
        for i in range(2, 23):
            page_number = str(i)
            urls.append(url+"page/"+page_number+"/")

        for url in urls:
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):                 # reach personal pages
        pages = response.xpath('//div[@id = "loop"]')
        halo = pages.xpath('//article[@class = "post-tile profile-tile"]')
        address = list()
        for i in halo:
            adonis = i.xpath('./div[@class = "post-excerpt"]')
            link = adonis.xpath('./h2[@class = "title post-title"]')
            url = link.xpath('./a/@href').extract()
            address.append(url[0])

        for link in address:
            yield Request(link, headers=self.headers, callback=self.parse_individual)

    def parse_individual(self, response):
        members = Faculty()
        item = MuFacultyItem()
        info = response.xpath('//div[@class="profile-meta"]')
        item['prof_name'] = response.xpath('//h1[@class="profile-title title"]/text()').extract_first()
        item['prof_title'] = info.xpath('./hgroup[@class]/h3[@class]/text()').extract_first()
        item['prof_department'] = info.xpath('./div[@class]/a[@href]/text()').extract_first()
        item['prof_page'] = "https://journalism.missouri.edu/staff/" + str(item['prof_name'])
        contact_list = info.xpath('./dl[@class = "profile-meta-contact-list"]')
        item['prof_phone'] = contact_list.xpath('./dd[1]/text()').extract_first()
        item['prof_email'] = contact_list.xpath('./dd[2]/a/text()').extract_first()

        members.edit_info(item['prof_page'], item['prof_name'], item['prof_department'], item['prof_title'], item['prof_email'], item['prof_phone'])

        filename = "0member_list.txt"
        with open(filename, 'a') as f:
            for link in members.personal_info['page']:
                f.write(link)
                f.write('\n')
        self.log('Saved file %s' % filename)
