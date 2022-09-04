import datetime, scrapy
from ..items import JobTItem



class JobsSpider(scrapy.Spider):
    name = 'jobt'
    actual_url = 'https://jobtoday.com/gb/jobs'

    start_urls = [
        actual_url
    ]
    covered = 0
    
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.JobTPipeline':300
    }}

    def parse(self, response):
  
        cards = response.css('div.jsx-2dafd18fd2c30d31')
        for card in cards:
            title = card.css('a.jsx-7a85161c8ecef1cc::attr(title)').extract_first()
            job_link = card.css('a.jsx-7a85161c8ecef1cc::attr(href)').extract_first()
            salary = card.css('span.JobCardLarge-salary::text').extract_first()
            job_type = card.css('.JobCardLarge-employmentType::text').extract_first()
            company_name = card.css('div.JobCardLarge-companyName span::text').extract_first()
            location = card.css('div.JobCardLarge-address span::text').extract_first()
            time_extracted = datetime.datetime.now()
            time_posted = card.css('div.JobCardLarge-updateDate::text').extract_first()
            items = {'details':{ 'title':title,  'job_link':job_link, 'company_name':company_name,
            'time_extracted':time_extracted, 'location':location,'salary':salary, 'time_posted':time_posted,
            'job_type':job_type
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        pagination = response.css('a.FeedPage-paginationLink--next::attr(href)').extract_first()
        if pagination is not None:
            yield response.follow(pagination, self.parse)



    
    def parse_job(self, response):
        db = JobTItem()
        items = response.meta['details']
        db['job_type'] = items['job_type']
        db['salary'] = items['salary']
        db['time_posted'] = items['time_posted']
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['number_of_applicants'] = 'null'
        db['remote'] = 0
        db['company_link']='null'
        db['time_extracted']=items['time_extracted']
        db['job_description'] =response.css('span.JobPage-description-text').extract_first()
        db['location'] = items['location']


        yield db


