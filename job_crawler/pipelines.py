import w3lib.html as wh
from .models import MyApi
from .transform import CleanData
# from .models import LinkedIn, db_connect, create_all_table, Indeed, CvLibrary
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
clean = CleanData()


class IndeedPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'][0]
        item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        item['medium'] = 'indeed'
        item['time_extracted'] =str(item['time_extracted'])
        item['number_of_applicants']='null'
        item['remote'] = 0
        item['job_type'] = 'null'
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])
        
        self.store_item(item)

        return item
    
    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)

class CvLibraryPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'][0]
        item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        item['medium'] = 'cvlib'
        item['time_extracted'] =str(item['time_extracted'])
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])
        
        self.store_item(item)

        return item
    
    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)

class JobTPipeline:

    def process_item(self, item, spider):
        item['title'] = wh.remove_tags(item['title'][0])
        item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        item['time_extracted']=str(item['time_extracted'])
        item['medium'] = 'jobstoday'
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])




        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)


class ReedsPipeline:
    def process_item(self, item, spider):
        try:
            item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        except:
            pass
        item['job_type'] = item['job_type'].strip().replace('\n', '')
        item['number_of_applicants'] = wh.remove_tags(item['number_of_applicants']).strip().replace('\n', '')
        item['salary'] = item['salary'].strip().replace('\n', '')
        item['time_extracted']=str(item['time_extracted'])
        item['time_posted'] = wh.remove_tags(item['time_posted']).strip().replace('\n', '')
        item['medium'] = 'reeds'
        item['title'] = item['title'][0]
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])



        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)


class GuardianPipeline:
    def process_item(self, item, spider):
        try:
            item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        except:
            pass
        item['number_of_applicants'] = 'null'
        item['time_extracted']=str(item['time_extracted'])
        item['medium'] = 'guardian'
        item['title'] = item['title'][0]
        item['remote'] = 0
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])
        item = item

        self.store_item(item)
        return item

    def store_item(self, item):
        print(item['date_posted'])
        myapi = MyApi()
        status = myapi.post_job(item)


class WeWorkPipeline:
    def process_item(self, item, spider):
        try:
            item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        except:
            pass
        item['number_of_applicants'] = 'null'
        item['time_extracted']=str(item['time_extracted'])
        item['medium'] = 'wework'
        item['title'] = item['title'][0]
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])

        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)


class JobsAcPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'][0]
        item['time_extracted'] = str(item['time_extracted'])
        item['medium'] = 'jobsac'
        item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        item['company_name'] = wh.remove_tags(item['company_name'])
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])

        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)

class CharityPipeline:
    def process_item(self, item, spider):
        item['job_type'] = wh.remove_tags(item['job_type']).strip().replace('\n', '')
        item['location'] = wh.remove_tags(item['location']).strip().replace('\n', '')
        item['time_posted'] = item['time_posted'].strip().replace('\n', '')
        item['title'] = item['title'][0]
        item['time_extracted'] = str(item['time_extracted'])
        item['job_description'] = wh.remove_tags(item['job_description']).strip().replace('\n', ' ')
        item['medium'] = 'charity'
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])


        
        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)


class FindAJobPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'][0].strip().replace('\n', ' ')
        item['company_name'] = wh.remove_tags(item['company_name']).strip().replace('\n', ' ')
        item['job_type'] = wh.remove_tags(item['job_type']).strip().replace('\n', ' ')
        item['location'] = wh.remove_tags(item['location']).strip().replace('\n', ' ')
        item['salary'] = wh.remove_tags(item['salary']).strip().replace('\n', ' ')
        item['time_extracted'] = str(item['time_extracted'])
        item['job_description'] = wh.remove_tags(item['job_description'])
        item['time_posted'] = wh.remove_tags(item['time_posted']).strip().replace('\n', ' ')
        item['medium'] = 'findajob'
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])
        
        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)


class TesPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'][0]
        item['salary'] = wh.remove_tags(item['salary'])
        item['time_extracted'] = str(item['time_extracted'])
        item['job_description'] = wh.remove_tags(item['job_description'])
        item['medium'] = 'tes'
        item['job_type1'] = clean.clean_job_type1(item['job_type'])
        item['job_type2'] = clean.clean_job_type2(item['job_type'])
        item['lower_sal'] = clean.extract_lower_sal(item['salary'])
        item['higher_sal'] = clean.extract_higher_sal(item['salary'])
        item['avg_sal'] = clean.avg_sal(item['lower_sal'], item['higher_sal'])
        item['sal_freq'] = clean.extract_freq_sal(item['salary'])
        location = clean.get_location(item['location'])
        item['city'] = location.get('city', 'null')
        item['state'] = location.get('state', 'null')
        item['county'] = location.get('county', 'null')
        item['date_posted'] = clean.clean_date_posted(item['time_extracted'], item['time_posted'])


        self.store_item(item)
        return item

    def store_item(self, item):
        myapi = MyApi()
        status = myapi.post_job(item)
        print(status)
