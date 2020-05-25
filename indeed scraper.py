# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:41:36 2020

@author: AGrze
"""

import re
import datetime
import requests
from bs4 import BeautifulSoup
import time


def setUserAgent(pick):
    global s
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36']
    s.headers.update({'user-agent':user_agents[pick%len(user_agents)]})
     
    
def crawlURL(path):
    attempts=0
    pageContent=''
    global s
    while attempts<5:
        try:
            pageContent = s.get(link).text
            attempts = 10 # dummy break condition
        except:
            attempts+=1;    
            print('crawl error URL') 
    return pageContent

def linkGenerator(age):
    URLlist = ['https://de.indeed.com/Jobs?as_and=&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&st=&as_src=&radius=25&l=Deutschland&fromage='+str(days)+'&limit=10&sort=&psf=advsrch&from=advancedsearch' for days in range(0, age)]
    return URLlist

s = requests.Session()
setUserAgent(10)

s.headers.update({'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/web'})
s.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})

# save file
FileOut = open('C:/Users/AGrze/Documents/Data Science Bootcamp/Techlab Project/24-05jobsInfo.txt','w', encoding = 'utf-8') 

counter= 0

for link in linkGenerator(31): 
    counter+=1
    if counter != 1:
        time.sleep(10)

    # crawl URL
    pageContent=crawlURL(link)
    print(counter, 'Website crawled!')
    
    # preparing soup...
    soup = BeautifulSoup(pageContent, 'html.parser') # unzipping and parsing
              
    dn = datetime.datetime.now();
    datestring = '%02d/%02d/%d;'%(dn.month,dn.day,dn.year)+'%02d:%02d;'%(dn.hour,dn.minute)
      
    attributes={}
    attributes['crawl_date']=datestring
    attributes['crawl_url']=link
    attributes['adsAge'] = counter
    
    # extracting number of jobs
    nbJobs = soup.find('div', {'id':'searchCountPages'})
    string = str(nbJobs)
    regex = re.findall(r'Seite 1 von (.*?) Jobs',string)
    attributes['jobs']=regex[0].replace('.','')
          
    # extracting job type info
    jobTypeUndivided=[]
    filter_loc= soup.find('span', {'id':'filter-job-type'})
    for typeWrapper in filter_loc.find_all('li', {'class':'dd-menu-option'}):
        for typeInfo in typeWrapper.find_all('span', class_='rbLabel'):
            if typeInfo.text.find('\xa0') !=-1:
                typeInfo = typeInfo.text.replace('\xa0','').replace('(','').replace(')','')
            else:
                typeInfo = typeInfo.text
            jobTypeUndivided.append(typeInfo)
    
    jobType = jobTypeUndivided[0::2]
    jobTypeNb = jobTypeUndivided[1::2]
    for i in range(len(jobType)):
        attributes[jobType[i]] = jobTypeNb[i]     
    
    # extracting cities
    citiesUndivided=[]
    filter_loc= soup.find('span', {'id':'filter-location'})
    for cityWrapper in filter_loc.find_all('li', {'class':'dd-menu-option'}):
        for cityInfo in cityWrapper.find_all('span', class_='rbLabel'):
            if cityInfo.text.find('\xa0') !=-1:
                cityInfo = cityInfo.text.replace('\xa0','').replace('(','').replace(')','')
            else:
                cityInfo = cityInfo.text
            citiesUndivided.append(cityInfo)
    
    city = citiesUndivided[0::2]
    cityNb = citiesUndivided[1::2]
    for i in range(len(city)):
        attributes[city[i]] = cityNb[i]  
    
    
    # extracting companies info
    
    companiesUndivided=[]
    filter_loc= soup.find('span', {'id':'filter-company'})
    for companyWrapper in filter_loc.find_all('li', {'class':'dd-menu-option'}):
        for companyInfo in companyWrapper.find_all('span', class_='rbLabel'):
            if companyInfo.text.find('\xa0') !=-1:
                companyInfo = companyInfo.text.replace('\xa0','').replace('(','').replace(')','')
            else:
                companyInfo = companyInfo.text
            companiesUndivided.append(companyInfo)
    
    company = companiesUndivided[0::2]
    companyNb = companiesUndivided[1::2]
    for i in range(len(company)):
        attributes['company'+str(i)] = company[i]
        attributes['company'+str(i)+'Ads'] = companyNb[i]
        #attributes[company[i]] = companyNb[i]
    
    # extracting language info
    
    langUndivided=[]
    try:
        filter_loc= soup.find('span', {'id':'filter-language'})
        for langWrapper in filter_loc.find_all('li', {'class':'dd-menu-option'}):
            for langInfo in langWrapper.find_all('span', class_='rbLabel'):
                if langInfo.text.find('\xa0') !=-1:
                    langInfo = langInfo.text.replace('\xa0','').replace('(','').replace(')','')
                else:
                    langInfo = langInfo.text
                langUndivided.append(langInfo)
        
        lang = langUndivided[0::2]
        langNb = langUndivided[1::2]
        for i in range(len(lang)):
            attributes[lang[i]] = langNb[i]
    except:
       print('language info failed')
       break

    print("Crawled!")
    # writing attributes to file   
    FileOut.write(str(attributes)+'\n')


FileOut.close()

import ast
import pandas as pd

dict_list=[]
with open('24-05jobsInfo.txt','r',encoding='utf-8') as crawl_file:
    line= crawl_file.readline()
    while line:
        dict_list.append(ast.literal_eval(line[:-1]))       
        line = crawl_file.readline()

df = pd.DataFrame(dict_list)
df.to_excel('24-05jobsInfo.xlsx')
df.to_csv('24-05jobsInfo.csv')
