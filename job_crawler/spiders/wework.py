import datetime, scrapy
from ..items import WeWorkItem



class JobsSpider(scrapy.Spider):
    name = 'wework'
    actual_url = 'https://weworkremotely.com/remote-jobs/search?term=&button=&region%5B%5D=0&region%5B%5D=6'
    start_urls = [
        actual_url
    ]
    covered = 0
    
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.WeWorkPipeline':300
    }}

    def parse(self, response):
  
        cards = response.css('li.feature')
        for card in cards:
            title = card.css('span.title::text').extract_first()
            job_link = 'https://weworkremotely.com'+card.css('a::attr(href)')[-1].get()
            remote = 1
            company_name = card.css('span.company::text').extract_first()
            company_link ='https://weworkremotely.com'+ card.css('a::attr(href)').get()
            location = card.css('span.region::text').extract_first()
            job_type = card.css('span.company::text')[1].get()
            salary = 'null'
            time_extracted = datetime.datetime.now()
            items = {'details':{ 'title':title,  'job_link':job_link, 'company_name':company_name,
            'time_extracted':time_extracted, 'location':location,'salary':salary, 'remote':remote,'company_link':company_link
            ,'job_type':job_type
            }}

            yield response.follow(job_link, self.parse_job, meta=items)


    
    def parse_job(self, response):
        db = WeWorkItem()
        items = response.meta['details']
        db['job_type'] = items['job_type']
        db['salary'] = items['salary']
        db['time_posted'] = response.css('time::text').get()
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['number_of_applicants'] = 'null'
        db['company_link']=items['company_link']
        db['time_extracted']=items['time_extracted']
        db['job_description'] =response.css('div#job-listing-show-container').extract_first()
        db['location'] = items['location']
        db['remote']=items['remote']


        yield db


