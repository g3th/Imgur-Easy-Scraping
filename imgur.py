import requests
import time
import os
import concurrent.futures
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup

directory = str(Path(__file__).parent) + '/downloaded_images/'
os.makedirs(directory, exist_ok = True)
gallery_links = []
search_parameter = 'cat' #input('Enter a search parameter: ')
#number_of_pages = int(input('Enter number of pages to search: ')
gallery_request = 'https://imgur.com/search?q='+search_parameter
browser_options = Options()
browser_options.add_argument ={'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
#browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.set_window_size(200,600)
browser.get(gallery_request)
time.sleep(0.5)

if browser.find_elements_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'):
	GDPR_disagree_button = browser.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
	GDPR_disagree_button.click()
	
scroll_counter = 0	
page_scrolling = browser.find_element_by_tag_name('html')
print('\rLoading Images         ',end='')
while scroll_counter < 1:
	print('\rFetching Page {}         '.format(str(scroll_counter+1)),end='')
	page_scrolling.send_keys(Keys.END)
	time.sleep(0.5)
	scroll_counter +=1

for link in browser.find_elements_by_tag_name('a'):
	if 'gallery' not in link.get_attribute('href'):
		pass
	else:
		gallery_links.append(link.get_attribute('href'))



def fetch_all_the_image_links(page):
	images_list = []
	for index in range(len(page)):
		request = requests.get(page[index])
		fetch_link = soup(request.content,'html.parser')	
		image_links = fetch_link.find_all('meta',attrs={'name':'twitter:image'})
		images_list.append(page[index])
	return images_list
	
images = []

with concurrent.futures.ThreadPoolExecutor(20) as executor:
	image_links = executor.submit(fetch_all_the_image_links, gallery_links)
	images.append(image_links.result())

print(images)
	
	

'''
video_link = fetch_link.find_all('meta',attrs={'name':'twitter:player:stream'})
'''
		
		
		
		
