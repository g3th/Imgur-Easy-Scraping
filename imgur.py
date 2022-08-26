import requests
import time
import os
import concurrent.futures
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup

images_directory = str(Path(__file__).parent) + '/downloaded_images/'
videos_directory = str(Path(__file__).parent) + '/downloaded_videos_or_gifs/'
os.makedirs(images_directory, exist_ok = True)
os.makedirs(videos_directory, exist_ok = True)
gallery_links = []
search_parameter = 'cat' #input('Enter a search parameter: ')
#number_of_pages = int(input('Enter number of pages to search: ')
gallery_request = 'https://imgur.com/search?q='+search_parameter
browser_options = Options()
browser_options.add_argument ={'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
browser_options.headless = True
browser = webdriver.Chrome(options = browser_options)
browser.set_window_size(200,600)
print('Opening Page')
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
browser.close()

def fetch_all_the_image_links(index, page):
	progress_bar = round(index / len(page) * 100 , 2)
	print('\rFetchin image {} out of {} images - Progress: {}%   '.format(str(index+1), str(len(page)+1), str(progress_bar), end=''))
	request = requests.get(page[index])
	fetch_link = soup(request.content,'html.parser')	
	images_links = fetch_link.find_all('meta',attrs={'name':'twitter:image'})
	return images_links

def fetch_all_the_video_links(index, page):
	progress_bar = round(index / len(page) * 100 , 2)
	print('\rFetchin video {} out of {} images - Progress: {}%   '.format(str(index+1), str(len(page)+1), str(progress_bar), end=''))
	request = requests.get(page[index])
	fetch_link = soup(request.content,'html.parser')	
	video_link = fetch_link.find_all('meta',attrs={'name':'twitter:player:stream'})
	return video_link

def threaded_download_videos(directory, filename, index, videos):
	with open(directory + filename, 'wb') as videos:
		request = requests.get(videos[index])
		videos.write(request.content)

#def threaded_download_imges(index, videos):

galleries = []
videos =[]
future_results_images = []
future_results_videos = []
image_links=[]
videos_links=[]
with concurrent.futures.ThreadPoolExecutor(30) as executor:
	for index in range(len(gallery_links)):
		galleries.append(executor.submit(fetch_all_the_image_links, index, gallery_links))
	for index in range(len(gallery_links)):
		videos.append(executor.submit(fetch_all_the_video_links, index, gallery_links))
	for future in concurrent.futures.as_completed(galleries):
		future_results_images.append(future.result())
	for future in concurrent.futures.as_completed(videos):
		if future != '':
			future_results_videos.append(future.result())
		else:
			pass

print(future_results_videos)
			
