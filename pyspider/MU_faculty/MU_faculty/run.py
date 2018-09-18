from scrapy import cmdline


name = "SCISpider"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())