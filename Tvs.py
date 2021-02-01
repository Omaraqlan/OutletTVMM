import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver   
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from azure.storage.blob import BlockBlobService

#Define website
url = "http://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies"
 
#assign options and useragent to chromedriver
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
action.click(on_element = element) 
   
# perform the operation 
action.perform()





#open all outlet tvs.
driver.get("http://outlet.mediamarkt.nl/beeld-geluid/televisie-projectie/televisies?sort=p.price&order=ASC&limit="+numberOfTV)




#wait for all elements with div have higher than 0 height to download
wait = WebDriverWait(driver, 10)
divsProd = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.product-thumb")))





strct = []
#needed to put it in dataframe and save it as csv or upload it in data azure
for element in range(len(divsProd)):
    lstData = divsProd[element].text.splitlines()
    lstData.append(divsProd[element].find_elements_by_tag_name("a")[0].get_attribute('href').split("?")[0])
    strct.append(lstData)
    


#Creating dataframe
df = pd.DataFrame(strct,columns=['Title','Description','OldPrice','NewPrice','discount','link'])


# saving the dataframe without indexs 
df.to_csv('OutletTv.csv',index=False)



#Providing accountstorage name , account storage key, container name to create the file in blobstorage
block_blob_service = BlockBlobService(account_name='pythonoqmm', account_key='hmV5qyCNX1CPLGScE3mO1xawQsO3X4BDWxtreB7kmv40RA0cZ3el5skyCKswAKdl+Q/sKPjyleYBkuQ6/BLoVg==')
block_blob_service.create_blob_from_path(container_name="pythonmm",blob_name="OutletTv.csv",file_path="C:\\Users\\Aqlanoz\\Desktop\\OutletMM\\OutletTv.csv")
