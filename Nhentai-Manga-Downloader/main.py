import requests, os, os.path, threading

URL = "https://t.dogehls.xyz/galleries/"

formats = {
	"jpg": 0,
	"png": 1,
	"jpeg": 2,
}

def readCodes():
	with open("./codes.txt", "r") as file:
		return file.readlines()

def downloadAndSaveHTML(url):
	""" Download the HTML to search useful info later """
	r = requests.get(url = url)

	with open("page.html", "wb") as file:
		file.write(r.content)

def writeImage(imageName, requestImage):
	""" Literaly writes an image """

	with open(imageName, "wb") as output:
		output.write(requestImage.content)

def getInfo():
	""" Open the HTML of the doujinshi and search for useful info """

	with open("page.html", "r") as file:
		file = file.readlines()

	code = file[114].split('"')[1].split("/")[4]
	defaultImgFormat = file[114].split('"')[1].split(".")[-1]
	pages = file[121].split(">")[6][:-6]

	return code, pages, defaultImgFormat

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

	for hentaiCode in file:
		hentaiCode = hentaiCode.rstrip() # Delete a '\n' at the end of the line

		os.mkdir(hentaiCode) if not os.path.exists(hentaiCode) else lambda: 0 # If the folder exist's it will do nothing 

		downloadAndSaveHTML(f"https://nhentai.to/g/{hentaiCode}/1")
		code, pages, defaultImgFormat = getInfo()


		for i in range(1, int(pages) + 1):
			url = f"{URL}{code}/{i}" # Example: https://t.dogehls.xyz/galleries/  1944372  /  1.png

			t = threading.Thread(target = downloadImage, args = (url, f"./{hentaiCode}/{i}", formats[defaultImgFormat]))
			t.start()


	os.remove("page.html")


if __name__ == "__main__":
	main()