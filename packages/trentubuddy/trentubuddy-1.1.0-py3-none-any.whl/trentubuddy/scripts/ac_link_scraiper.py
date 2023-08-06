#Gets the link to the academic callendar as a direct download
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import json
import os

#convert the array to a dict once formatted with key value pairs to save to a JSON file
results_dict = {}
json_filepath = os.getcwd() + "/data/ac_link.json"

url = 'https://www.trentu.ca/registrar/academic-calendar/undergraduate-calendar'

def Store_Data(dict_to_save):
    try:
        with open(json_filepath, "w") as file:
            json.dump(dict_to_save, file, indent=4)
            file.close()
    except FileNotFoundError:
        print("ac_link.json has been removed since the bot started...")
    except:
        print("Error dumping information from ac_link_scraiper.py")
        
def get_ac_link():
    #if theres an error the driver may stay open so close it.
    try:

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)        
        driver.set_page_load_timeout(5)
        driver.get(url) 

        ac_link = driver.find_element("xpath", "/html/body/div[2]/div/main/div/div/div[1]/div[2]/div/div/div/div/p[1]/a")
        results_dict["Academic Calendar"] = ac_link.get_attribute("href")
        Store_Data(results_dict)

        driver.quit()
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