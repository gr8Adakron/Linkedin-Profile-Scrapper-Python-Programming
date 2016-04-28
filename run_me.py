from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import getpass
from bs4 import BeautifulSoup
import requests
import os
import re
from mymodules.extract_profiles import Extract
import json
import sys


class Linkedin_Scraper():
    source_code=None
    browser=None
    user_id=None
    phantom_path=r'phantom_js\bin\phantomjs'
    complete_detail_of_user={}
    failed_url='https://www.linkedin.com/uas/login-submit'
    def __init__(self):
        print('Opening browser in background, Wait for few seconds... ')
        self.browser = webdriver.PhantomJS(self.phantom_path) # or add to your PATH
        self.browser.set_window_size(1024, 768)
        self.browser.get('https://linkedin.com/')
        time.sleep(5)
        #self.stats = {}
        
    def close_phantom(self):
        #os.system('taskkill /f /im phantomjs.exe')
        self.browser.close();
        print('Successfully Ended.')

    def get_authenticated(self,email,password):
        username_input = self.browser.find_element_by_name("session_key")
        password_input = self.browser.find_element_by_name("session_password")
        login_attempt = self.browser.find_element_by_name("submit")
        username_input.send_keys(email)
        password_input.send_keys(password)
        login_attempt.submit()
        print('Wait, Logging In...')
        time.sleep(3)
        current=self.browser.current_url
        if(current==self.failed_url):
            print('Failed Loging.')
            sys.exit("Re-run program, and provide correct credentials. Thank You.!")
        else:
            print('Successfully Loged In.')
        url=input('Enter users url, to be scraped : ')
        self.extract_user_data(user_url=url)
    
    def extract_user_data(self,user_url):
        self.browser.get(user_url) 
        split_url = re.split("/",user_url)
        self.user_id=split_url[4]
        self.browser.save_screenshot('screen_shots/'+self.user_id+'.png') # save a screenshot to disk
        self.source_code = BeautifulSoup(self.browser.page_source, "lxml") 
        print('Screen Shot Taken.')
        e = Extract(self.source_code)
        self.complete_detail_of_user['Basic Information']=e.basic_data_extraction()
        profile_skill=self.source_code.find('div',{"id":"profile-skills"})
        education_detail=self.source_code.find('div',{"id":"background-education"})
        profile_experience=self.source_code.find('div',{"class":"background-experience"})
        if profile_skill is not None:
            self.complete_detail_of_user['Skills']=e.profile_skills()
        else:
            self.complete_detail_of_user['Skills']='Skills Not Specified by user.'
        if profile_experience is not None:
            self.complete_detail_of_user['Experience']=e.get_experience()
        else:
            self.complete_detail_of_user['Experience']='Experience Not Specified by user.'
        self.complete_detail_of_user['A Profile Summary '] = e.get_summary()
        if education_detail is not None:
             self.complete_detail_of_user['Education Detail']=e.get_education()
        else:
            self.complete_detail_of_user['Education Detail']='Education Detail, is Not Specified by user.'
        

    def create_json(self):
        pretty_complete_user_data=json.dumps(self.complete_detail_of_user,sort_keys=True, indent=6)
        print(pretty_complete_user_data)
        with open('json/'+self.user_id+'.json', 'w') as fp:
            json.dump(self.complete_detail_of_user,fp,sort_keys=True, indent=4)
        print('\n\n> Json file of the whole profile, is stored in json folder.\n> Screen Shot of profile is stored in Screen Shot folder.')
        
def main():
    l = Linkedin_Scraper()
    email=str(input('Enter Your Linkedin Email : '))
    password=getpass.getpass('Enter Your Linkedin Password(Carefully) : ')
    #email=str('myemail@gmail.com')
    #password='my_password'
    l.get_authenticated(email=email,password=password)
    l.create_json()
    l.close_phantom()


if __name__ == "__main__":
    main()
