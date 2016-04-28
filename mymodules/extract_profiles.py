from bs4 import BeautifulSoup
from collections import OrderedDict

class Extract():
    extracted_code=None
    basic_data=None
    experience_data=None
    skills=None
    education=None
    def __init__(self,sc):
        self.extracted_code=sc
        self.basic_data=self.extracted_code.find('div',{"class":"profile-overview"})
        self.experience_data=self.extracted_code.find('div',{"class":"background-experience"})
        self.skills=self.extracted_code.find('div',{"id":"profile-skills"})
        self.summary=self.extracted_code.find('div',{"class":"summary"})
        self.education=self.extracted_code.find('div',{"id":"background-education"})

    def basic_data_extraction(self):
        print('This is basic class extractiion : ')
        member=self.basic_data.find('div',{"class":"member-connections"})
        name=self.basic_data.find('span',{"class":"full-name"})
        title=self.basic_data.find('p',{"class":"title"})
        locality=self.basic_data.find("span",{"class":"locality"})
        other_basic=self.basic_data.find("tbody")
        values=other_basic.find_all("tr")
        b_details={}
        b_details=OrderedDict()
        total_connections=member.find("strong")
        b_details['Connection']=total_connections.text
        b_details['Name']=name.text
        b_details['Title']=title.text
        b_details['Locality']=locality.text
        for v in values:
            data=v.find_next('a').find_next('a')
            #print(data.text+'++++++++\n')
            data_2= v.find_all('a')
            count=1
            basic_details=''
            for d in data_2:
                if(count>2):
                    last_basic_detail=basic_details
                    basic_details=basic_details+' '+d.text
                    #print(d.text)
                count+=1
            if(data.text=='Education' or d.text=='Previous'):
                b_details[data.text]=last_basic_detail
            else:
                b_details[data.text]=basic_details
        return b_details

    def profile_skills(self):
        skills={}
        #endo_skills_li=profile_skill.find_all("li",{"class":"endorse-item has-endorsements "})
        endo_skills_li=self.skills.find_all("span",{"class":"skill-pill"})
        for single_skills in endo_skills_li:
            skills_value=single_skills.find_next('a')
            skills_name=single_skills.find_next('a').find_next('a')
            skills[skills_name.text]=skills_value.text+', Endorsements'
        return skills

    def get_experience(self):
        single_exp=self.experience_data.findAll('div')
        complete_exp={}
        unique_id=1
        job=['empty']
        company=['empty']
        for experience in single_exp:
            len_job=len(job)
            len_com=len(company)
            exp_heading=experience.find_next('h4')
            e_company=exp_heading.find_next('h5')
            exp_company=e_company.find_next('a')
            if(company[len_com-1]!=exp_company.text or job[len_job-1]!=exp_heading.text):
                single_exp={}
                exp_date=experience.find_next("span",{"class":"experience-date-locale"})
                i=1
                if exp_date is not None:
                    time=exp_date.find_all('time')
                    single_exp['To']='Present'
                    for t in time:
                        if(i==1):
                            single_exp['From']=t.text
                        else:
                            single_exp['To']=t.text
                        i+=1
                    start_duration=False
                    duration=''
                    for s in exp_date.text:
                        #print(s)
                        if(s=='('):
                            start_duration=True
                        if(start_duration==True):
                            duration=duration+s
                            if(s==')'):
                                start_duration=False
                                break
                    single_exp['Duration']=duration
                if exp_date is not None:    
                    exp_area=exp_date.find_next("span",{"class":"locality"})
                exp_desc=experience.find("p",{"dir":"ltr"})
                if(exp_desc!=None):
                    single_exp['Description']=exp_desc.text
                else:
                    single_exp['Description']="Description Not Specified."
                if(exp_area!=None):
                    #print(exp_area.text)
                    single_exp['Area']=exp_area.text
                else:
                    single_exp['Area']="Area or Locality, Not Specified."
                single_exp['a.Job_title']=exp_heading.text
                single_exp['Company Name']=exp_company.text
                job.append(exp_heading.text)
                company.append(exp_company.text)
                complete_exp['Experience_'+str(unique_id)]=single_exp
                unique_id+=1 
        complete_exp['A Total Number of Experience']=unique_id-1
        return complete_exp

    def get_summary(self):
        summary={}
        if self.summary is not None:
            summary['Summary']=self.summary.text
            return summary
        else:
            summary['Summary']='Summary not specified by user.'
            return summary

    def get_education(self):
        header=self.education.find_all('header')
        edu={}
        education_id=1
        for h in header:
            single_edu={}
            institute_name=h.find_next('h4')
            course_name=institute_name.find_next('h5')
            start=h.find_next("time")
            course_end=h.find_next("time").find_next('time')
            single_edu['Institute Name ']=institute_name.text
            single_edu['Course Name'] = course_name.text
            single_edu['Course Started'] = start.text
            end_course = course_end.text.replace("–", "-")
            single_edu['Course Completed '] =end_course
            edu['Education_'+str(education_id)]=single_edu
            education_id+=1
        edu['A Total Number of Education']=education_id-1
        return edu

