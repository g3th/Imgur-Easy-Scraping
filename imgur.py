import requests
from bs4 import BeautifulSoup as soup

metadata = {'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}

gallery_links = []

search_parameter = input('Enter a search parameter:')

gallery_request = requests.get('https://imgur.com/search?q='+search_parameter, headers = metadata)
fetch_gallery_html = soup(gallery_request.content,'html.parser')
fetch_gallery_links = fetch_gallery_html.find_all('a',{'class':'image-list-link'})

for links in fetch_gallery_links:
	gallery_links.append('https://imgur.com' + links['href'])


print('Found {} galleries from inputted query.'.format(len(gallery_links)))


while True:
	if len(gallery_links) > 0:
		gallery_image_index = input('Enter an index number: ')
		try:			
			image_request_html = requests.get(gallery_links[int(gallery_image_index)-1])
			fetch_link = soup(image_request_html.content,'html.parser')	
			image_link = fetch_link.find_all('meta',attrs={'name':'twitter:image'})
			video_link = fetch_link.find_all('meta',attrs={'name':'twitter:player:stream'})
			for images in image_link:
				print(images['content'])
			for videos in video_link:
				print(videos['content'])
			break
		except (IndexError, ValueError):
			print('\x1bc')
			continue
	else:
		print('No Results, Ending')
		break
		
		
		
		
