from scrapy import cmdline


name = "ScopusSpider"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())