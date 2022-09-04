import datetime, scrapy
from ..items import ReedsItem



class JobsSpider(scrapy.Spider):
    name = 'reeds'
    actual_url = 'https://www.reed.co.uk/jobs?datecreatedoffset=LastTwoWeeks'

    start_urls = [
        actual_url
    ]
    covered = 0
    custom_settings= {'ITEM_PIPELINES':{
        'job_crawler.pipelines.ReedsPipeline':300
    }}
    

    def parse(self, response):
        cards = response.css('article.job-result-card')
        for card in cards:
            title = card.css('h3.job-result-heading__title a::attr(title)').extract_first()
            job_link = 'https://www.reed.co.uk'+card.css('h3.job-result-heading__title a::attr(href)').extract_first()
            company_name = card.css('a.gtmJobListingPostedBy::text').extract_first()
            try:
                company_link = 'https://www.reed.co.uk' + card.css('a.gtmJobListingPostedBy::attr(href)').extract_first()
            except:
                company_link=''
            location = card.css('li.job-metadata__item--location::text').extract_first().strip().replace('\n','')
            salary = card.css('li.job-metadata__item--salary::text').extract_first()
            time_posted = card.css('div.job-result-heading__posted-by').extract_first()
            job_type = card.css('li.job-metadata__item--type::text').extract_first()
            time_extracted = datetime.datetime.now()
            if card.css('li.job-metadata__item--remote').extract_first() is not None:
                remote = True
            else:
                remote = False
            items = {'details':{ 'title':title,'remote':remote, 'job_link':job_link, 'company_name':company_name, 'company_link':company_link,
            'location':location, 'salary':salary, 'time_posted':time_posted, 'time_extracted':time_extracted, 'job_type':job_type,
            }}

            yield response.follow(job_link, self.parse_job, meta=items)

        if response.css('a#nextPage::attr(href)').extract_first() is not None:
            link = 'https://www.reed.co.uk'+ response.css('a#nextPage::attr(href)').get()
            yield response.follow(link, self.parse)



    
    def parse_job(self, response):
        db = ReedsItem()
        items = response.meta['details']
       
        db['title']=items['title'],
        db['job_link']=items['job_link']
        db['company_name']=items['company_name']
        db['company_link']=items['company_link']
        db['location']=items['location']
        db['salary']=items['salary']
        db['time_posted']=items['time_posted']
        db['time_extracted']=items['time_extracted']
        db['job_type'] = items['job_type']
        db['remote'] = items['remote']
        db['number_of_applicants'] = response.css('div.applications').extract_first()

        try:
            job_description =response.css('div.description span').extract_first().strip().replace('\n', ' ')
            db['job_description'] = job_description
        except:
            db['job_description'] = ''

        yield db


