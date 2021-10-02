import requests
import bs4
import os

# this script is for www.gocomics.com

# url = 'https://www.gocomics.com/shirley-and-son-classics/2021/01/01'
url = 'https://www.gocomics.com/garfield/2021/01/01'



# download the page
def download_webpage(url):
    count = 0

    while count != 10:
        # select the image
        res = requests.get(url)
        res.raise_for_status()

        soup_text = bs4.BeautifulSoup(res.text, features='html.parser')

        # download the image
        print(f"Downloading {count+1} out of 10.")
        download_image(soup_text)

        # get the next page
        next_page = soup_text.select('.gc-calendar-nav__next a')[0].get('href')
        url = 'https://www.gocomics.com'+ str(next_page)

        # Increment the count
        count += 1



# download the image
def download_image(soup_text):
    comic_elements = soup_text.select('picture.item-comic-image img')
    if comic_elements == []:
        print("Could not find an image...")
    else:
        comic_image_url = comic_elements[0].get('src')
        print("Downloading image...")
        image = requests.get(comic_image_url)
        image.raise_for_status()
    
    # save the image
    image_file = open(os.path.join('garfield', os.path.basename(comic_image_url)) + '.gif', 'wb')
    for chunk in image.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

# let the download begin
download_webpage(url)