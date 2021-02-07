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
from urllib.request import urlopen

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
    lstData = divsProd[element].text.splitlines()
    tvURL = divsProd[element].find_elements_by_tag_name("a")[0].get_attribute('href').split("?")[0]
    lstData.append(tvURL)
    # Details
    listofDmgDetails = []
    dmgDict = dict()
    dmgDict['Other'] = None
    page = urlopen(tvURL)
    soup = BeautifulSoup(page.read(), 'html.parser')
    table = soup.find(class_="tab-pane active").find("table")
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        if len(columns) == 1:
            dmgDict['Other'] = str(columns[0].text).rstrip()
            continue
        dmgDict[str(columns[0].text).rstrip()] = str(columns[1].text).lstrip(":").lstrip()
    listofDmgDetails.append(tvURL[tvURL.find("ID"):])
    listofDmgDetails.append(dmgDict["Verpakking"])
    listofDmgDetails.append(dmgDict["Voorkant"])
    listofDmgDetails.append(dmgDict["Achterkant"])
    listofDmgDetails.append(dmgDict["Bovenkant"])
    listofDmgDetails.append(dmgDict["Onderkant"])
    listofDmgDetails.append(dmgDict["Zijkant rechts"])
    listofDmgDetails.append(dmgDict["Zijkant links"])
    listofDmgDetails.append(dmgDict["Other"])
    listofDamage.append(listofDmgDetails)
    listofTV.append(lstData)

# Creating dataframe
df = pd.DataFrame(listofTV, columns=['Title', 'Description', 'OldPrice', 'NewPrice', 'discount', 'link'])
dfdmg = pd.DataFrame(listofDamage,
                     columns=['ProductID', 'Verpakking', 'Voorkant', 'Achterkant', 'Bovenkant', 'Onderkant',
                              'Zijkantrechts', 'Zijkantlinks','Other'])

# saving the dataframe without indexs
df.to_csv('OutletTv.csv', index=False)
dfdmg.to_csv('tvdetails.csv', index=False)

driver.close()

print("Check your CSV")
# Providing accountstorage name , account storage key, container name to create the file in blobstorage
block_blob_service = BlockBlobService(account_name='pythonoqmm', account_key='stgAb+W2UIHuXV3elbtAKRrubLsweoYvo4DZ6Mxc3h6/YtT+fdlPtPpfw0C8vKbyQc41FogKek+POaAuo2iCYw==')
block_blob_service.create_blob_from_path(container_name="pythonmm",blob_name="OutletTv.csv",file_path="C:\\Users\\Aqlanoz\\PycharmProjects\\OutletTVMM\\OutletTv.csv")
block_blob_service.create_blob_from_path(container_name="pythonmm",blob_name="tvdetails.csv",file_path="C:\\Users\\Aqlanoz\\PycharmProjects\\OutletTVMM\\tvdetails.csv")
print("finished")
