import datetime, scrapy
from ..items import ReedsItem



class JobsSpider(scrapy.Spider):
    name = 'jobsac'
    actual_url = 'https://www.jobs.ac.uk/search/?keywords=&location=United+Kingdom&placeId=&activeFacet=&resetFacet=&sortOrder=1&pageSize=25&startIndex=26'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.JobsAcPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('div.j-search-result__result')
        
        for card in cards:
            title = card.css('div.j-search-result__text a::text').extract_first().strip().replace('\n', '')
            job_link = 'https://www.jobs.ac.uk'+card.css('div.j-search-result__text a::attr(href)').extract_first()
            company_name = card.css('div.j-search-result__employer').extract_first()
            time_extracted = datetime.datetime.now()
            items = {'details':{ 'title':title, 'job_link':job_link, 'company_name':company_name,
            'time_extracted':time_extracted, 
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('div.j-search-content__pagination--control a::attr(href)')[1].get() is not None:
            link = 'https://www.jobs.ac.uk'+ response.css('div.j-search-content__pagination--control a::attr(href)')[1].get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = ReedsItem()
        items = response.meta['details']
       
        headers = response.css('div.j-advert-details__ie-display td::text')
        db['location'] = headers[0].get().strip().replace('\n', '')
        db['salary'] = headers[1].get().strip().replace('\n', '')
        db['job_type'] = headers[2].get().strip().replace('\n', '')
        db['time_posted'] = headers[4].get()
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']='null'
        db['time_extracted']=items['time_extracted']
        db['remote'] = 0
        db['number_of_applicants'] = 'null'
        db['job_description'] = response.css('div#job-description').extract_first()


        yield db


