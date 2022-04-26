from distutils.log import debug
import os
import shutil
from PIL import Image
import validators

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

save_images = False
DRIVER_PATH = './chromedriver.exe'
debug = False

while True:
    url = input("Enter URL of main course page on Neso Academy: ")
    if validators.url(url):
        break
    else:
        print('Invalid Response')

url += '/ppts'

while True:
    a = input('Do you want to save the images? (Y/n) ')
    a = a[0].lower()

    if a == 'y':
        save_images = True
        break
    elif a == 'n':
        break
    else:
        print('Invalid Response!')


options = Options()
options.headless = True
options.add_argument("window-size=1366,728")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(url)
title = driver.current_url
actions = ActionChains(driver)

ele = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".free-ppt a"))
)

all_links = driver.find_elements_by_css_selector('.free-ppt a')

links = []
final_imgs = []

for link in all_links:
    links.append(link.get_attribute('href'))

l = 0

folder_name =  'temp' if not save_images else 'images-' + title

try:
    os.mkdir(folder_name)
except:
    pass


for link in links:

    if debug and l == 1:
        break
    
    try:
        os.mkdir(f"./{folder_name}/Chapter {l}")
    except:
        pass

    driver.get(link)

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.react-pdf__Page__canvas'))
    )

    all_images = driver.find_elements_by_css_selector('.react-pdf__Page__canvas')

    i = 0
    for img in all_images:
            
        
        actions.move_to_element(img)
        actions.context_click()
        actions.send_keys(Keys.ENTER)
        actions.perform()
        img.screenshot(f"./{folder_name}/Chapter {l}/Slide {i}.png")
        img_file = Image.open(f"./{folder_name}/Chapter {l}/Slide {i}.png")
        img_file = img_file.convert('RGB')
        final_imgs.append(img_file)
       

        i+=1

    l+=1

im1 = final_imgs[0]
final_imgs = final_imgs[1:]

try:
    os.mkdir('./output')
except:
    print('Cannot create folder')

try:
    im1.save(r'./output/output.pdf', save_all=True, append_images=final_imgs)
except:
    pass

if not save_images:
    shutil.rmtree('./temp')

driver.quit()

print("Done!")