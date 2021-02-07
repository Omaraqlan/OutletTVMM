import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from azure.storage.blob import BlockBlobService
import requests
from bs4 import BeautifulSoup

# Define website
url = "http://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies"

# assign options and useragent to chromedriver
options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')

# create webdriver object
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/Users/Aqlanoz/Desktop/crm/chromedriver.exe')
driver.implicitly_wait(10)

# get outletmediamarket
driver.get(url)

tvElement = driver.find_elements_by_css_selector('a.child_lv3')[0].text
numberOfTV = ''.join(filter(str.isdigit, tvElement))

# get cookie Element
element = driver.find_element_by_id('cookie-consent')

# create action chain object
action = ActionChains(driver)

# click the item
action.click(on_element=element)

# perform the operation
action.perform()

# open all outlet tvs.
driver.get("http://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies?sort=p.price&order=ASC&limit="+numberOfTV)

# wait for all elements with div have higher than 0 height to download
wait = WebDriverWait(driver, 10)
divsProd = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.product-thumb")))

listofTV = []
listofDamage = []
# needed to put it in dataframe and save it as csv or upload it in data azure
for element in range(len(divsProd)):
    # lstData = divsProd[element].text.splitlines()
    tvURL = divsProd[element].find_elements_by_tag_name("a")[0].get_attribute('href').split("?")[0]
    # lstData.append(tvURL)
    # Details
    listofDmgDetails = []
    page = requests.get(tvURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find(class_="tab-pane active").get_text()
    listofDmgDetails.append(tvURL[tvURL.find("ID"):])
    listofDmgDetails.append(items[items.find("Verpakking"):items.find("Voorkant")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Voorkant"):items.find("Achterkant")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Achterkant"):items.find("Bovenkant")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Bovenkant"):items.find("Onderkant")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Onderkant"):items.find("Zijkant")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Zijkant rechts"):items.find("Zijkant links")].split(":")[1].lstrip())
    listofDmgDetails.append(items[items.find("Zijkant links"):].split(":")[1].lstrip())
    listofDamage.append(listofDmgDetails)

    # listofTV.append(lstData)

# Creating dataframe
df = pd.DataFrame(listofTV, columns=['Title', 'Description', 'OldPrice', 'NewPrice', 'discount', 'link'])
dfdmg = pd.DataFrame(listofDamage,
                     columns=['ProductID', 'Verpakking', 'Voorkant', 'Achterkant', 'Bovenkant', 'Onderkant',
                              'Zijkantrechts', 'Zijkantlinks'])

# saving the dataframe without indexs
df.to_csv('OutletTv.csv', index=False)
dfdmg.to_csv('tvdetails.csv', index=False)

# Providing accountstorage name , account storage key, container name to create the file in blobstorage
# block_blob_service = BlockBlobService(account_name='pythonoqmm', account_key='hmV5qyCNX1CPLGScE3mO1xawQsO3X4BDWxtreB7kmv40RA0cZ3el5skyCKswAKdl+Q/sKPjyleYBkuQ6/BLoVg==')
# block_blob_service.create_blob_from_path(container_name="pythonmm",blob_name="OutletTv.csv",file_path="C:\\Users\\Aqlanoz\\Desktop\\OutletMM\\OutletTv.csv")
# block_blob_service.create_blob_from_path(container_name="pythonmm",blob_name="tvdetails.csv",file_path="C:\\Users\\Aqlanoz\\Desktop\\OutletMM\\tvdetails.csv.csv")
