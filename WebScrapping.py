from bs4 import BeautifulSoup
import time
import csv
import requests
 
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
planet_data = []
new_planet_data = []

headers = ["name", "distance", "mass", "radius"]

def Scrape():
    for i in range(1, 198):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs = {"class", "List of Brightest Stars"}):
            li_tags = ul_tag.find_all("li")
            templist = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    templist.append(li_tag.find_all("a")[0].contents[0])

                else:
                    try:
                        templist.append(li_tag.contents[0])
                    
                    except:
                        templist.append("")
                templist.append("https://en.wikipedia.org/wiki/"+li_tags[0].find_all("a",href=True )[0]["href"])
            
            planet_data.append(templist)
            print("page done", i)
            browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
def scrape_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attr={"class", "fact_row"}):
        td_tags= tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attr={"class", "value"})[0].contents[0])
            except: 
                temp_list.append("")
        
        new_planet_data.append(temp_list)

Scrape()

with open("name.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)

final_planet_data=[]
for (index, data) in enumerate(planet_data):
    final_planet_data.append(data+ new_planet_data[index])

with open("final.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)