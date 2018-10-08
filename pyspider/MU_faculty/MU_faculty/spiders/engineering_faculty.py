import scrapy
from MU_faculty.items import MuFacultyItem
from scrapy import Request
from MU_faculty.Artemis import Faculty
import csv


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

       # filename = "member_name_list.txt"
        #with open(filename, 'w', encoding='utf-8') as f:
         #   for link in members.personal_info['name']:
          #      f.write(link)
           #     f.write('\n')
        #self.log('Saved file %s' % filename)

        filename2 = 'affiliation.txt'
        with open(filename2, 'w', encoding='utf-8') as f2:
            for affiliation in members.personal_info['title']:
                f2.write(affiliation)
                f2.write('\n')
        self.log('Saved file %s' % filename2)

'''  filename1 = "engineer_faculty.csv"
        with open(filename1, 'a+', newline='',encoding='utf-8') as f1:
            writer = csv.writer(f1)
            for (name, title, department, page, email, phone) in zip(members.personal_info['name'], members.personal_info['title'], members.personal_info['department'], members.personal_info['page'], members.personal_info['email'], members.personal_info['phone']):
                #print(name, title, department, page, email, phone)
                writer.writerow([name, title, department, page, phone, email])
            f1.close()
        self.log('Saved file %s' % filename1)'''
