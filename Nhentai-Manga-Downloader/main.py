import requests, os, os.path, threading
from bs4 import BeautifulSoup

URL = "https://t.dogehls.xyz/galleries/" # Url where manga pages are saved

formats = {
	# Image formats
	"jpg": 0,
	"png": 1,
	"jpeg": 2,
}

def readCodes():
	with open("./codes.txt", "r") as file:
		return file.readlines()


def writeImage(imageName, requestImage):
	""" Literaly writes an image """

	with open(imageName, "wb") as output:
		output.write(requestImage.content)


def getInfo(url):
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


def downloadImage(url, imageName, format_):
	""" Download an image from a web server """
	
	formats = [".jpg", ".png", ".jpeg"]

	r = requests.get(url + formats[format_])

	if r.status_code == 200:
		writeImage(imageName + formats[format_], r)
	
	else:
		downloadImage(url, imageName, (format_ - 1))

def main():
	file = readCodes()

	for hentai_code in file:
		hentai_code = hentai_code.rstrip() # Delete a '\n' at the end of the line

		if not os.path.exists(hentai_code):
			os.mkdir(hentai_code)

		internal_code, default_img_format, pages_number = getInfo(f"https://nhentai.to/g/{hentai_code}/1")

		for i in range(1, int(pages_number) + 1):
			url = f"{URL}{internal_code}/{i}" # Example: https://t.dogehls.xyz/galleries/1944372/

			t = threading.Thread(target = downloadImage, args=(url, f"./{hentai_code}/{i}", formats[default_img_format]))
			t.start()


if __name__ == "__main__":
	main()