# Final Project Intermediate Python
# Snake Coders 
# Lucas Falivene - Lfaliven
# Fabio Beltran Vasquez - fbeltran
# Muhammad Bin Oiad - mbinoiad

import requests
from bs4 import BeautifulSoup
import re

#%%

# gettravel()
# Parameters: None
# Get common info for travelers from the Pennsylvania Department 
# of Health website by scrapping the site. Returns a dictionary
# with the scrapped organized information.
# Returns: travelq - Dict
def gettravel():
    # Create the http request and request the page
    httpString ='https://www.health.pa.gov/topics/disease/coronavirus/Pages/Travelers.aspx'
    
    travelpage = requests.get(httpString)
        # Scraping:
    # Parse the page
    travelsoup = BeautifulSoup(travelpage.content, 'html.parser')
    # Find the required tag. All the travelers questions
    current_travel = travelsoup.find(id="ctl00_PlaceHolderMain_PageContent__ControlWrapper_RichHtmlField")
    # Find the sub-tag - Subsections in the site. questions are in
    # strong and answers are in 'li'
    travel_sections = current_travel.find_all('h4')
    travel_sections2 = current_travel.find_all('strong')
    travel_sections3 = current_travel.find_all('li')
    pattern=r'\?$'
    travelq=dict()
    # Get the sections, questions and answers.
    for i in range(len(travel_sections)):
        
        if re.search(pattern,travel_sections[i].text) != None:
            para = travel_sections[i].find_next_sibling('p')
            travelq[i]=[travel_sections[i].text,para.text]
    
    x=len(travelq.keys())
    
    for i in range(len(travel_sections2)):
        
        if re.search(pattern,travel_sections2[i].text) != None:
            travelq[i+x]=[travel_sections2[i].text,travel_sections3[i-1].text]
    
    return travelq
#%%
# getcovidcdc()
# Parameters: None
# Get Frequently Asked Questions about COVID  from the CDC Site.
# It returns a dictionary with the scrapped organized information
# Returns: cdc_faq_section - Dict
def getcovidcdc():
    
    # Create the http request and request the page
    httpString ='https://www.cdc.gov/coronavirus/2019-ncov/faq.html'
    
    cdcpage = requests.get(httpString)
    
        # Scraping:
    # Parse the page
    cdcsoup = BeautifulSoup(cdcpage.content, 'html.parser')
    # Find the required tag. All the CDC FAQ sections
    cdc_faq = cdcsoup.find_all(class_="col-md-12")
    # Find the sub-tag - All the CDC subsections and questions
    cdc_faq_section=dict()
    # Get the sections, questions and answers.
    for section in range(len(cdc_faq)):
        
        if cdc_faq[section].find('h3'):
            cdc_faq_section[cdc_faq[section].find('h3').text]=dict()
            temp=cdc_faq[section].find_all(class_="card bar")
            for j in range(len(temp)):
                if temp[j].find(class_="card-header"):
                    cdc_faq_section[cdc_faq[section].find('h3').text][temp[j].find(class_="card-header").text]=temp[j].find(class_="card-body").text
                
    return cdc_faq_section
        
        