import scrapy
from scrapy.http import FormRequest

class JobsSpider(scrapy.Spider):
    name = 'linkedin'
    actual_url = 'https://www.linkedin.com/checkpoint/rm/sign-in-another-account'

    start_urls = [
        actual_url
    ]

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        yield response.follow('https://www.linkedin.com/checkpoint/lg/login-submit',self.login, meta={'token':token}, method='POST' )


    def login(self, response):
        return FormRequest.from_response(response,formdata={
            'csrfToken':response.meta.get('token'),
            'session_key':'sarahunoke@gmail.com',
            'session_password':'october7',
            # 'loginFlow':'REMEMBER_ME_OPTIN'
    }, callback=self.start_scraping)

    def start_scraping(self, response):
        print("""
        
        IN!!
        """)
