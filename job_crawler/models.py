import requests

url = 'https://job-aggregator.azurewebsites.net'

class MyApi:
    def __init__(self):
        self.job_point =   'https://job-aggregator.azurewebsites.net/api/jobs/'
       # self.skill_point = 'https://job-aggregator.azurewebsites.net/api/skills/'
       # self.title_point = 'https://job-aggregator.azurewebsites.net/api/titles/'
        
        self.headers = {'Content-Type': "application/json"}


    def post_job(self, item):

        payload = {"title":item['title'], "company_name":item['company_name'], "company_link":item['company_link'], "description":item['job_description'],
         "job_link":item['job_link'], "location":item['location'], "medium":item['medium'], "num_of_applicants":item['number_of_applicants'],
        "remote":item['remote'], "salary":item['salary'], "time_extracted":item['time_extracted'], "time_posted":item['time_posted'], "job_type":item['job_type'],
        "job_type1":item['job_type1'], "job_type2":item['job_type2'], "lower_sal":item['lower_sal'], "higher_sal":item['higher_sal'], "avg_sal":item['avg_sal'],
        "sal_freq":item['sal_freq'], "county":item['county'], "state":item['state'], "date_posted":item['date_posted'], "city":item['city']
        
        }
        response = requests.request("POST", self.job_point, headers=self.headers, json=payload)
        response = response.json()
        return response


