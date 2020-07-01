from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://www.linkedin.com/login')
sleep(2)
username = driver.find_element_by_id('username')
username.send_keys('your-email-id')
sleep(0.5)
password = driver.find_element_by_id('password')
password.send_keys('your-password')
sleep(0.5)
log_in_button = driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button')
log_in_button.click()
sleep(2)

list_details = []
urls = open('linkedin_urls.txt', 'r')
Lines = urls.readlines()

for line in Lines:
   # driver.get('https://www.linkedin.com/in/barackobama')
    try:
        driver.get(line)
        response = driver.page_source.encode('utf-8').strip()
        soup =  BeautifulSoup(response,'html.parser')
        full_name = soup.find('h1',{'class' : 'top-card-layout__title'})
        filename = full_name.text.strip() + '.json'
        profession = soup.find('h2',{'class' : 'top-card-layout__headline'})
        address = soup.find('span',{'class' : 'top-card__subline-item'})
        connections = soup.find('span',{'class' : 'top-card__subline-item top-card__subline-item--bullet'})
        #educations = soup.find_all('span',{'class' : 'top-card-link__description'})
        websites = soup.find_all('span',{'class' : 'websites__url-text'})
        summary = soup.find('section',{'class' : 'summary pp-section'})
        experience = soup.find_all('li',{'class' : 'experience-item'})
        exp_title = soup.find_all('h3',{'class' : 'result-card__title experience-item__title'})
        exp_title_list = [exp_title[i].text.strip().replace('\n',' ') for i in range(len(exp_title))]
        exp_subtitle = soup.find_all('h4',{'class' : 'result-card__subtitle experience-item__subtitle'})
        exp_subtitle_list = [exp_subtitle[i].text.strip().replace('\n',' ') for i in range(len(exp_subtitle))]
        exp_duration = soup.find_all('span',{'class' : 'date-range__duration'})
        exp_duration_list = [exp_duration[i].text.strip().replace('\n',' ') for i in range(len(exp_duration))]
        exp_date_range = soup.find_all('p', {'class' : 'experience-item__duration experience-item__meta-item'})
        exp_date_range_list = [exp_date_range[i].text.strip().replace(exp_duration_list[i], '') for i in range(len(exp_date_range))]
        websites = [websites[i].text.strip() for i in range(len(websites))]
        #educations = [educations[i].text.strip() for i in range(len(educations)-1)]
        education = soup.find_all('span',{'class' : 'education__item education__item--degree-info'})
        education_list = [education[i].text.strip() for i in range(len(education))]
        #university = soup.find_all('h3',{'class' : 'result-card__title'})
        #university = soup.find_all(lambda tag: tag.name == 'h3' and 
        #                           tag.get('class') == ['result-card__title'])
        university = soup.select('body > main > section.core-rail > section > section.education.pp-section > ul > li > div > h3')
        uni_list = [university[i].text.strip().replace('\n',' ') for i in range(len(university))]
        skills_list = soup.find_all('li',{'class' : 'skills__item'})
        skills_list = [skills_list[i].text.strip() for i in range(len(skills_list))]
        detail = {
                    'full_name' : full_name.text.strip(),
                    'profession': profession.text.strip() if profession.text else 'Not found',
                    'address' : address.text.strip() if type(address) is not None else 'Not found',
                    'connections' : connections.text.strip(),
                    'university' : uni_list,
                    'websites' : websites if type(websites) is not None else 'Not found',
                    'experience' :  [{ 'experience_title' : exp_title_list[i], 'experience_subtitle': exp_subtitle_list[i], 'experience_date_range': exp_date_range_list[i], 'experience_duration': exp_duration_list[i]} for i in range(0, len(exp_duration_list))],
                    'degrees' : education_list,
                    'skills' : skills_list,
                    'summary' : summary.text.strip().replace('About', '') if type(summary) is not None else 'Not found'
        }
        list_details.append(detail)
        sleep(5)

    except Exception as ex:
        pass 

for i in range(1, len(list_details)+1):
    with open(str(i)+'.json', 'w', encoding='utf8') as outfile:
        json.dump(list_details[i-1], outfile, ensure_ascii=False, indent=2)

