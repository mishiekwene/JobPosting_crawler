import scrapy
import datetime
from ..items import IndeedItem


class JobsSpider(scrapy.Spider):
    name = 'indeed'
    actual_url = 'https://uk.indeed.com/jobs?q=jobs&fromage=14'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.IndeedPipeline':300
    }}
    
    def parse(self, response):
        # time.sleep(5) 
        cards = response.css('.cardOutline')
        for card in cards:
            title = card.css('a.jcs-JobTitle span::text').extract_first()
            job_link = 'https://uk.indeed.com'+card.css('h2.jobTitle a.jcs-JobTitle::attr(href)').get()
            company_name = card.css('span.companyName::text').get()
            company_link = card.css('span a.companyOverviewLink::attr(href)').get()
            rating_number = card.css('span.ratingNumber span::text').extract_first()
            rating_link = card.css('span.withRatingLink a::attr(href)').extract_first()
            location = card.css('div.companyLocation::text').extract_first()
            salary = card.css('div.salary-snippet-container div.attribute_snippet::text').extract_first()
            time_posted = card.css('span.date::text').extract_first()
            time_extracted = datetime.datetime.now()
            items = {'details':{ 'title':title, 'job_link':job_link, 'company_name':company_name, 'company_link':company_link,'rating_number':rating_number,
            'rating_link':rating_link, 'location':location, 'salary':salary, 'time_posted':time_posted, 'time_extracted':time_extracted,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        pagination = response.css('div.pagination ul li')
        next_page = pagination[-1]
        if next_page.css('span.pn span.np').extract() is not None:
            next_page_link = next_page.css('a::attr(href)').extract_first()
            next_page_link2 = "https://uk.indeed.com" + next_page_link
            yield response.follow(next_page_link2, self.parse)


    
    def parse_job(self, response):
        db = IndeedItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        if items['company_link'] is not None:
            db['company_link']='https://uk.indeed.com' +items['company_link']
        db['location']=items['location']
        db['salary']=items['salary']
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        rating_count = response.css('div.icl-Ratings-count::text').extract_first()
        job_description =response.css('div.jobsearch-jobDescriptionText').extract_first()
        db['job_description'] = job_description
        if db['company_name'] is None:
            db['company_name'] = response.css('div.icl-u-lg-mr--sm a::text').get()
        if 'company_link' not in db:
            db['company_link'] = response.css('div.icl-u-lg-mr--sm a::attr(href)').get()
        if rating_count is not None:
            db['rating_count'] = rating_count
            db['rating_number']=items['rating_number']
            try:
                db['rating_link']='https://uk.indeed.com'+items['rating_link']
            except:
                db['rating_link'] = 'null'
        yield db