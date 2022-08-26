import requests
import time
import os
import sys
import concurrent.futures
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup

images_directory = str(Path(__file__).parent) + '/downloaded_images/'
videos_directory = str(Path(__file__).parent) + '/downloaded_videos_or_gifs/'
os.makedirs(images_directory,exist_ok = True)
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
while scroll_counter < 5:
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
	sys.stdout.write('Fetching image '+str(index+1)+' out of '+str(len(page)+1)+' images - Progress: '+str(progress_bar)+'% ') 
	sys.stdout.flush()
	sys.stdout.write('\033[2K\033[1G')
	request = requests.get(page[index])
	fetch_link = soup(request.content,'html.parser')	
	images_links = fetch_link.find_all('meta',attrs={'name':'twitter:image'})
	return images_links

def fetch_all_the_video_links(index, page):
	progress_bar = round(index / len(page) * 100 , 2)
	sys.stdout.write('Fetching video '+str(index+1)+' out of '+str(len(page)+1)+' images - Progress: '+str(progress_bar)+'% ') 
	sys.stdout.write('\033[2K\033[1G')
	sys.stdout.flush()
	request = requests.get(page[index])
	fetch_link = soup(request.content,'html.parser')	
	video_link = fetch_link.find_all('meta',attrs={'name':'twitter:player:stream'})
	return video_link

def threaded_download_videos(directory, filename, index, videos):
	with open(directory + filename, 'wb') as downloads:
		progress_bar = round(index / len(page) * 100,1)
		print('\rScraping {} Videos: Progress {}              '.format(len(videos), progress_bar), end='')
		request = requests.get(videos[index])
		downloads.write(request.content)

def threaded_download_imges(directory, filename, index, images):
	with open(directory + filename, 'wb') as downloads:
		progress_bar = round(index / len(page) * 100,1)
		print('\rScraping {} Images: Progress {}              '.format(len(images), progress_bar), end='')
		request = requests.get(images[index])
		downloads.write(request.content)
galleries = []
videos =[]
future_results_images = []
future_results_videos = []
image_links=[]
video_links=[]
with concurrent.futures.ThreadPoolExecutor(30) as executor:
	for index in range(len(gallery_links)):
		galleries.append(executor.submit(fetch_all_the_image_links, index, gallery_links))
	for index in range(len(gallery_links)):
		videos.append(executor.submit(fetch_all_the_video_links, index, gallery_links))
	for gallery in concurrent.futures.as_completed(galleries):
		future_results_images.append(gallery.result())
	for video in concurrent.futures.as_completed(videos):
		if 'meta content' in str(video.result()):
			future_results_videos.append(video.result())
		else:
			continue
	for image in concurrent.futures.as_completed(galleries):
		if 'meta content' in str(image.result()):
			future_results_images.append(image.result())
		else:	
			continue
	for video_link in future_results_videos:
		video_links.append(str(video_link).split('"')[1])
	for image_link in future_results_images:
		image_links.append(str(image_link).split('"')[1])
	for index in range(len(video_links)):
		executor.submit(threaded_download_videos, videos_directory, str(video_links[index]).split('/')[3], index, video_links)
	#for index in range(len(image_links)):
		#executor.submit(threaded_download_imges, images_directory, str(image_links[index]).split('/')[3], index, image_links)

		
