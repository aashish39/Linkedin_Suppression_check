#Import Required Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options


#New Functions Required for Project
# Function to get data from srapped raw data
def get_data(all_info,links):
    df_new = pd.DataFrame()
    full_name =[]
    job_title =[]
    email_all = []
    personnal_phone = []
    # full_info = []
    company_name_list=[]
    company_phone = []
    for item in all_info:
        if item != "#NA":
            item_list = item.split("\n")
            if item_list[6] !="Insta Reveal Email":
                full_name.append(item_list[1])
                job_title.append(item_list[4])
                company_name_list.append(item_list[5])
                email_all.append(item_list[6])
                personnal_phone.append(item_list[9])
                company_phone.append(item_list[11])
            if item_list[6] =="Insta Reveal Email":
                full_name.append(item_list[1])
                job_title.append(item_list[4])
                company_name_list.append(item_list[5])
                email_all.append("#NA")
                personnal_phone.append(item_list[8])
                company_phone.append(item_list[10])                
        else:
            full_name.append("#NA")
            job_title.append("#NA")
            company_name_list.append("#NA")
            email_all.append("#NA")
            personnal_phone.append("#NA")
            company_phone.append("#NA")
    df_new["Full_name_scrapped"] = full_name
    df_new["Job_Title_scrapped"] = job_title
    df_new["Company_name_scrapped"] = company_name_list
    df_new["email_id_scrapped"] = email_all
    df_new["personnal_phone_scrapped"] = personnal_phone
    df_new["company_phone_scrapped"] = company_phone
    df_new["Prospect_slintel_links"] = links
    return df_new


def scrapped_data(driver,df):
    all_info =[]
    for i in df.link.values:
        driver.get(i) 
        time.sleep(1.5)
        try:
            driver.find_elements(By.CLASS_NAME,'ant-btn-link')[2].click()
            time.sleep(2)
            tst = driver.find_elements(By.CLASS_NAME,'ant-drawer-content-wrapper')[0].text
            all_info.append(tst)  
        except:
            all_info.append('#NA')
    received_data = get_data(all_info,df.link)
    new_data = pd.concat([df,received_data],axis=1)
    new_data.to_excel("output.xlsx")
    return new_data    

def driver_launch():
    Options = webdriver.ChromeOptions()
    Options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=Options)
    driver.get("https://dashboard.slintel.com/")
    email = "ikjoozhvd+tb06@gyqj.emlhub.com"
    pass_word = "Bjayla@22"
    username = driver.find_element(By.ID, "email")
    username.send_keys(email)
    password = driver.find_element(By.ID,"password")
    password.send_keys(pass_word)
    driver.find_element(By.XPATH, "//button[@type='button']").click()
    return driver

if __name__ == '__main__':
    print("Process is started...........................................")
    driver=driver_launch()
    time.sleep(6)
    df = pd.read_csv("Book1.csv",names=["Fist Name","last name", "Company name","link"])
    scrapped_data(driver,df)
    driver.quit()
