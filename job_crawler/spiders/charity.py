import datetime, scrapy, re
from ..items import CharityItem



class JobsSpider(scrapy.Spider):
    name = 'charity'
    actual_url = 'https://www.charityjob.co.uk/jobs?UserHasGrantedBrowserGeoLocationPermission=No&radius=80'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.CharityPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('article.job-card-wrapper')
        for card in cards:
            title = card.css('div.job-title span::text').extract_first()
            job_link = 'https://www.charityjob.co.uk'+card.css('div.job-title a::attr(href)').extract_first()
            company_name = card.css('div.organisation::text').extract_first()
            time_posted = card.css('div.posted-item::text').extract_first()
            time_extracted = datetime.datetime.now()
            items = {'details':{ 'title':title, 'job_link':job_link, 'company_name':company_name,
           'time_posted':time_posted, 'time_extracted':time_extracted,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('li.new-pagination__item--arrow-right a::attr(href)').extract_first() is not None:
            link = response.css('li.new-pagination__item--arrow-right a::attr(href)').get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = CharityItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']=response.css('div.organisation a::attr(href)').get()
        db['location']=response.css('div.location-wrapper').get()
        db['salary']=response.css('div.more-info div.job-summary-item span::text')[0].get()
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        db['job_type'] = response.css('div.job-summary-item')[2].get()
        if re.search("Remote", db['location']) is not None:
            db['remote'] = 1
        else:
            db['remote'] = 0
        db['number_of_applicants'] = 'null'

        job_description =response.css('div.job-description').extract_first().strip().replace('\n', ' ')
        db['job_description'] = job_description
        yield db


