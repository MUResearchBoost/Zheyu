import scrapy
from MU_faculty.items import MuFacultyItem
from scrapy import Request
from MU_faculty.Artemis import Faculty


class EngineeringSpider(scrapy.Spider):
    name = "engineering_faculty_members"
    allowed_domain = ['engineering.missouri.edu']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

    def start_requests(self):
        url = "https://engineering.missouri.edu/academics/faculty/"
        yield Request(url, headers=self.headers)

    def parse(self, response):
        members = Faculty()
        item = MuFacultyItem()
        people = response.xpath('//div[@class = "vc_grid vc_row vc_grid-gutter-30px vc_pageable-wrapper vc_hook_hover"]')
        individuals = people.xpath('./div[@class = "vc_pageable-slide-wrapper vc_clearfix"]')
        aristotle = individuals.xpath('./div')

        for individual in aristotle:
            basic_info = individual.xpath('./div[@class]')
            personal_link = basic_info.xpath('./div[@class="vc_gitem-animated-block  vc_gitem-animate vc_gitem-animate-none"]')
            item['prof_page'] = personal_link.xpath('./div[@class]/a/@href').extract()
            item['prof_name'] = personal_link.xpath('./div[@class]/a/@title').extract_first()
            detailed_info = basic_info.xpath('./div[@class="vc_gitem-zone vc_gitem-zone-c"]')
            personal_info0 = detailed_info.xpath('./div/div')
            item['prof_department'] = personal_info0.xpath('./div/div[1]/text()').extract_first()
            item['prof_title'] = personal_info0.xpath('./div/div[2]/text()').extract_first()
            personal_info1 = detailed_info.xpath('./div/div/div[1]')
            item['prof_email'] = personal_info1.xpath('./div[@class= "vc_gitem-acf email field_5a0e048319668"]/text()').extract_first()
            item['prof_phone'] = personal_info1.xpath('./div[@class= "vc_gitem-acf phone field_5a0e045119667"]/text()').extract_first()

            members.edit_info(item['prof_page'][0], item['prof_name'], item['prof_department'], item['prof_title'], item['prof_email'], item['prof_phone'])

        filename = "member_list.txt"
        with open(filename, 'w') as f:
            for link in members.personal_info['page']:
                f.write(link)
                f.write('\n')
        self.log('Saved file %s' % filename)
