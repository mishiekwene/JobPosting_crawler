import datetime, scrapy
from ..items import CvLibraryItem



class JobsSpider(scrapy.Spider):
    name = 'cvlibrary'
    actual_url = 'https://www.cv-library.co.uk/jobs?posted=28'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.CvLibraryPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('article.search-card')
        for card in cards:
            title = card.css('h2.job__title a::attr(title)').extract_first()
            job_link = 'https://www.cv-library.co.uk'+card.css('h2.job__title a::attr(href)').extract_first()
            company_name = card.css('a.job__company-link::text').get()
            company_link = card.css('a.job__company-link::attr(href)').get()
            location = card.css('span.job__details-location::text').extract_first().strip().replace('\n','')
            salary = card.css('dd.salary::text').extract_first()
            time_posted = card.css('p.job__posted-by span.color-green::text').extract_first()
            time_extracted = datetime.datetime.now()
            number_of_applicants = response.css('dl.mobile-no dd.job__details-value a::text').extract_first().strip().replace('\n', ' ')
            if card.css('span.job__icon--remote').get() is not None:
                remote = True
            else:
                remote = False
            items = {'details':{ 'title':title,'remote':remote, 'number_of_applicants':number_of_applicants, 'job_link':job_link, 'company_name':company_name, 'company_link':company_link,
            'location':location, 'salary':salary, 'time_posted':time_posted, 'time_extracted':time_extracted,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        self.covered+=1
        if response.css('a.pagination__next::attr(href)').extract_first() is not None:
            link = response.css('a.pagination__next::attr(href)').get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = CvLibraryItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']=items['company_link']
        db['location']=items['location']
        db['salary']=items['salary']
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        db['remote'] = items['remote']
        db['number_of_applicants'] = items['number_of_applicants']


        job_description =response.css('div.job__description').extract_first().strip().replace('\n', ' ')

        db['job_description'] = job_description
        db['job_type'] = response.css('dl.bottom dd.job__details-value::text').extract_first()


        yield db


