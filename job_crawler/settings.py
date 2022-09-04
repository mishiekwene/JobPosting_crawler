# Scrapy settings for job_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'job_crawler'

SPIDER_MODULES = ['job_crawler.spiders']
NEWSPIDER_MODULE = 'job_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'job_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'job_crawler.middlewares.JobCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'job_crawler.middlewares.JobCrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'job_crawler.pipelines.IndeedPipeline':300,
   'job_crawler.pipelines.CvLibraryPipeline':300,
   'job_crawler.pipelines.JobTPipeline':300,
   'job_crawler.pipelines.ReedsPipeline':300,
   'job_crawler.pipelines.GuardianPipeline':300,
   'job_crawler.pipelines.WeWorkPipeline':300,
   'job_crawler.pipelines.JobsAcPipeline':300,
   'job_crawler.pipelines.CharityPipeline':300,
   'job_crawler.pipelines.FindAJobPipeline':300,
   'job_crawler.pipelines.TesPipeline':300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DATABASE = {
    'drivername': 'postgresql',
    'host': 'ec2-3-226-163-72.compute-1.amazonaws.com',
    'port': '5432',
    'username': 'wyftsbbpojixkq',
    'password': 'a1d8c53fc40fbb1ebf290c4e24e7f16444274116b0916bbfb941660c2562ba59',
    'database': 'dvjjvpb99kd8i'

}


    # 'drivername': 'postgresql',
    # 'host': 'ec2-3-226-163-72.compute-1.amazonaws.com',
    # 'port': '5432',
    # 'username': 'wyftsbbpojixkq',
    # 'password': 'a1d8c53fc40fbb1ebf290c4e24e7f16444274116b0916bbfb941660c2562ba59',
    # 'database': 'dvjjvpb99kd8i'


    # 'drivername': 'postgresql',
    # 'host': 'localhost',
    # 'port': '5432',
    # 'username': 'postgres',
    # 'password': 'october7',
    # 'database': 'job_crawler1'
DOWNLOADER_CLIENTCONTECTFACTORY = 'job_crawler.context.MyContextFactory'