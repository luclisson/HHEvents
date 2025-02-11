from bs4 import BeautifulSoup
import requests
from HHgegenRechts import EventHHgegenRechts

url = "https://vernetztgegenrechts.hamburg/veranstaltungen-2/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

rows =soup.find_all("div", class_="row") #every row is one event, name row is because of the class name in the html doc
# set up default values
description = "no description was found"
linkElement = "no link was found" #this var defines the html element
eventTimeStringValue = "no time was found :("
categories = ["no category was registered"] #default value if no category is found
#use try catch for every web scrape because you cant be sure every info is provided
for i in range(len(rows)):
   try:
        event_content = rows[i].find("div", class_="decm-events-details")
   except:
        continue
   try:
        description = event_content.find("p", class_="decm-show-data-display-block ecs-excerpt")
   except:
       continue
   try:
        linkElement = event_content.find("a", class_="act-view-more et_pb_button et_pb_custom_button_icon et_pb_button_no_hover")
   except:
       continue
   try:
        eventTime = event_content.find("span", class_="decm_date")
        eventTitleH2 = event_content.select('h2[class^= "entry-title"]') #select the h2 first because the a element has no class name and contains the heading value 
        EventTitleValue = eventTitleH2[0].find("a").string
   except:
       continue
   try:
       if (eventTime):
        eventTimeStringValue = eventTime.string
   except:
        continue
   try:
        eventCategoryElement = event_content.select('span[class^="decm_categories ecs_category_"]')
        if (eventCategoryElement):
            categories = []#clear list if categories were detected 
        for element in eventCategoryElement:
            aList = element.find_all("a")
            for a in aList:
                categories.append(a.text)
   except:
        continue
   event = EventHHgegenRechts(
       title = EventTitleValue,
       time = eventTimeStringValue,
       link = linkElement['href'],
       description = description.text,
       categories=categories
   )
   print(event)
   print("----------------")
