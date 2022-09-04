import datetime, scrapy
from ..items import TesItem



class JobsSpider(scrapy.Spider):
    name = 'tes'
    actual_url = 'https://www.tes.com/jobs/search?keywords=&locations=United%20Kingdom'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.TesPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('div.tds-job-card')
        for card in cards:
            title = card.css('h3.tds-job-card__content-title::text').extract_first()
            job_link = card.css('a[data-testid="job-card-link"]::attr(href)').extract_first()
            salary = card.css('span.tds-salary').extract_first()
            time_extracted = datetime.datetime.now()
            remote = False
            items = {'details':{ 'title':title,'remote':remote, 'job_link':job_link,
            'salary':salary,'time_extracted':time_extracted,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('a.pagination__next::attr(href)').extract_first() is not None:
            page = response.css('a.pagination__next::attr(href)').extract_first()
            link = 'https://www.tes.com/jobs/search?currentpage={}&keywords=&locations=United%20Kingdom'.format(page)
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = TesItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=response.css('strong[data-testid="app_job_details_employer_header_name"]::text').extract_first()
        db['company_link']='null'
        db['location']=response.css('span[data-testid="app_job_details_employer_header_location"]::text').extract_first()
        db['salary']=items['salary']
        db['time_posted']=response.css('time[data-testid="app_job_details_summary_posted_value"]::text').extract_first()
        db['time_extracted']=items['time_extracted']
        db['job_type'] =response.css('strong[data-testid="app_job_details_summary_contract_value"]::text').extract_first()
        db['remote'] = items['remote']
        db['number_of_applicants'] = 'null'

        try:
            job_description =response.css('div.job-details-content__body__description').extract_first().strip().replace('\n', ' ')
            db['job_description'] = job_description
        except:
            db['job_description'] = ''

        yield db


