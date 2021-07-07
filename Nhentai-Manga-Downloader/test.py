import requests
from bs4 import BeautifulSoup

def getInfo(url): # Delete
	""" Search for the internal_code, image_format and pages number """

	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")

	# Search for an image tag like this: <img src="https://t.dogehls.xyz/galleries/1890817/1.jpg" width="1280" height="1807" class="fit-horizontal" />
	# "/3518908175705/" is an internal folder in the server that contains all media of manga
	# As you can see, the url has the code and the image format that images are using. In this case jpg
	# By example, https://t.dogehls.xyz/galleries/1890817/2.jpg should be the root for the image two
	
	info = soup.find("img", {"class": "fit-horizontal"})

	# Split info to something like this: ['https:', '', 't.dogehls.xyz', 'galleries', '1890817', '1.jpg']
	# There we have the code in the index 4 and the image name in the index 5
	splitted_info = info.attrs["src"].split("/")

	internal_code = splitted_info[4]
	image_format = splitted_info[5].split(".")[1]

	# Search for a span tag with "num-pages" class
	pages_number = int(soup.find("span", {"class": "num-pages"}).text)

	return internal_code, image_format, pages_number


getInfo("https://nhentai.to/g/355705/1")