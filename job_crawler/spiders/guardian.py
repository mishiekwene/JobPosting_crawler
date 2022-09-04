import datetime, scrapy
from ..items import GuardianItem



class JobsSpider(scrapy.Spider):
    name = 'guardian'
    actual_url = 'https://jobs.theguardian.com/searchjobs/?Keywords=&radialtown=&LocationId=&RadialLocation=30'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.GuardianPipeline':300
    }}
    # 'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'}
    

    def parse(self, response):
        cards = response.css('li.lister__item ')
        for card in cards:
            title = card.css('h3.lister__header span::text').extract_first()
            link = card.css('h3.lister__header a::attr(href)').extract_first().strip().replace(' ', '')
            job_link = 'https://jobs.theguardian.com'+ link
            company_name = card.css('li.lister__meta-item--recruiter::text').extract_first()
            company_link = 'null'
            location = card.css('li.lister__meta-item--location::text').extract_first().strip().replace('\n','')
            salary = card.css('li.lister__meta-item--salary::text').extract_first()
            time_posted = 'null'
            time_extracted = datetime.datetime.now()
            items = {'details':{ 'title':title, 'job_link':job_link, 'company_name':company_name, 'company_link':company_link,
            'location':location, 'salary':salary, 'time_posted':time_posted, 'time_extracted':time_extracted, 
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('ul.paginator__items li a::attr(href)')[-1] is not None:
            link = 'https://jobs.theguardian.com'+ response.css('ul.paginator__items li a::attr(href)')[-1].get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = GuardianItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']=items['company_link']
        db['location']=items['location']
        db['salary']=items['salary']
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        db['job_type'] = 'null'
        db['number_of_applicants']= 'null'

        try:
            job_description =response.css('div.mds-edited-text').extract_first().strip().replace('\n', ' ')
            db['job_description'] = job_description
        except:
            db['job_description'] = ''

        yield db


