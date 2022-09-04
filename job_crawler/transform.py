from statistics import mean
import requests
import re
import datetime
from dateparser.search import search_dates

class CleanData:
    def __init__(self):
        self.geoapify_url = 'https://api.geoapify.com/v1/geocode/search?filter=countrycode:gb&apiKey=1b48259b810e48ddb151889f9ea58db0&text={}'

    def get_location(self, text):
        response = requests.request('GET', url=self.geoapify_url.format(text))
        response = response.json()
        location = response['features'][0]['properties']
        return location

    def extract_lower_sal(self, r):
        salary_list = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?=\D)', str(r))
        try:
            answer = float(salary_list[0].replace(',', ''))
            return answer
        except:
            return 0
        
    def extract_higher_sal(self, r):
        salary_list = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?=\D)', str(r))
        try:
            answer = float(salary_list[1].replace(',', ''))
            return answer
        except:
            return 0

    def extract_freq_sal(self, r):
        r = str(r)
        if 'annum' in r or 'yearly' in r:
            return 'annum'
        elif 'hour' in r or 'hourly' in r:
            return 'hour'
        elif 'week' in r or 'weekly' in r:
            return 'week'
        elif 'day' in r or 'daily' in r:
            return 'day'
        elif 'month' in r or 'monthly' in r:
            return 'month'
        else:
            return 'null'


    def clean_date_posted(self, time_ext, time_posted):
        p = datetime.datetime.strptime(time_ext, "%Y-%m-%d %H:%M:%S.%f")
        time_posted = search_dates(time_posted, settings={'RELATIVE_BASE':p, 'TIMEZONE': 'UTC'})
        if time_posted:
            return str(time_posted[0][1])
        else:
            return 'null'


    def clean_job_type1(self, r):
        r = str(r).lower()
        if 'full' in r and 'part' in r:
            return 2
        elif 'part' in r:
            return 1
        elif 'full' in r:
            return 0
        else:
            return 'null'

    def clean_job_type2(self,r):
        r = str(r).lower()
        if 'contract' in r and 'permanent' in r and 'temporary' in r:
            return 6
        elif 'permanent' in r and 'temporary' in r:
            return 5
        elif 'contract' in r and 'temporary' in r:
            return 4
        elif 'contract' in r and 'permanent' in r:
            return 3
        elif 'contract' in r:
            return 2
        elif 'permanent' in r or 'perm' in r:
            return 1
        elif 'temporary' in r or 'temp' in r:
            return 0
        return 'null'
      
    def avg_sal(self, lower_sal, higher_sal):
        sal = mean([lower_sal, higher_sal])
        return sal

    
