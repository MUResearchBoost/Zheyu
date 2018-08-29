from scrapy import cmdline


name = "faculty_members"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())