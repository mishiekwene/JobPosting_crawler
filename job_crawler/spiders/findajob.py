import datetime, scrapy
from ..items import FindAJobItem



class JobsSpider(scrapy.Spider):
    name = 'findajob'
    actual_url = 'https://findajob.dwp.gov.uk/search?f=14&loc=86383'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.FindAJobPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('div.search-result')
        for card in cards:
            title = card.css('h3 a.govuk-link::text').extract_first()
            job_link = card.css('h3 a.govuk-link::attr(href)').extract_first()
            company_name = card.css('ul.search-result-details li strong')[0].get()
            company_link = 'null'
            try:
                salary = card.css('ul.search-result-details li strong')[1].get()
            except:
                salary=''
            location = card.css('ul.search-result-details li span').extract_first()
            time_posted = card.css('ul.search-result-details li')[0].get()
            time_extracted = datetime.datetime.now()
            remote = False
            items = {'details':{ 'title':title,'remote':remote, 'job_link':job_link, 'company_name':company_name, 'company_link':company_link,
            'location':location, 'salary':salary, 'time_posted':time_posted, 'time_extracted':time_extracted,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('a.pager-next::attr(href)').extract_first() is not None:
            link = response.css('a.pager-next::attr(href)').get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = FindAJobItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']=items['company_link']
        db['location']=items['location']
        db['salary']=items['salary']
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        db['job_type'] = response.css('tr.govuk-table__row td.govuk-table__cell')[-2].get()
        db['remote'] = items['remote']
        db['number_of_applicants'] = 'null'

        try:
            job_description =response.css('div.govuk-body').extract_first().strip().replace('\n', ' ')
            db['job_description'] = job_description
        except:
            db['job_description'] = 'null'

        yield db


