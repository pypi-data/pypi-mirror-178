from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import json
import os

#To make more portable gets THIS files path and goes down a level to the data folder, This is the folder we want that contains specialties.json. If moved update this
#json_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data")

results_array = []

#convert the array to a dict once formatted with key value pairs to save to a JSON file
results_dict = {}

url = 'https://www.trentu.ca/cois/programs/degree-computer-science/specializations'
html_container = "div"
#The class tag to search (within the container html_container)
class_tag = "field-item even"

#HTML tags we want to keep
header_tags = {"h1", "h2", "h3", "h4", "h5", "h6"}
list_tags = {"li"}

#merge the dictionaries to start with a full list to search by first then sellect one or the other
all_tags = header_tags.copy()
all_tags.update(list_tags)

def Store_Data(dict_to_save):
    with open(os.getcwd() + "/data/specialties.json", "w+") as file:
        json.dump(dict_to_save, file, indent=4)
        print("DUMPED")

#Initialize beautiful soup as an object of the drivers page source
def BeautifulSoupSetup(input_driver):
    return BeautifulSoup(input_driver.page_source, "html.parser")

def update_specialties():
    #if theres an error the driver may stay open
    try:
        specialty_title = ""
        requirements_list = []

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)        
        driver.set_page_load_timeout(5)
        driver.get(url)   

        soup = BeautifulSoupSetup(driver)
        div_container = soup.find(html_container, class_ = class_tag)

        for html_tag in div_container.find_all(all_tags):
            if html_tag.name in header_tags:
                #wait for one full iteration first
                if specialty_title != "":
                    results_dict[specialty_title] = requirements_list 
                requirements_list = []                               
                specialty_title = html_tag.contents[0]
            #if end of loop do the last add last iteration
            elif html_tag == div_container.find_all(all_tags)[-1]:
                requirements_list.append(html_tag.contents[0].text)
                results_dict[specialty_title] = requirements_list
            else:            
                requirements_list.append(html_tag.contents[0].text)            
        driver.quit()
        Store_Data(results_dict)
        return 0
    except:
        print("Error... Terminating Driver")
        driver.quit()
        return 1
        
#do nothing when imported until called
def main():
    pass
if __name__ == "__main__":
    main()