import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
import re

dataFrame = pd.read_csv('id_url.csv')
urlList = list(dataFrame.publicyelppageurl)
idList = list(dataFrame.salon_id)
salonList = list(dataFrame.accountname)
csvFile = open('image_urls_temp.csv', 'wt+')
csvFile.write('Salon_ID, Name, Image URLs, Date, Image_ID\n')
homepage = 'https://www.yelp.com'
i = 0

for url in urlList:
    j = 1
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        imagePage = homepage + bs.find('div', {'data-ga-label':'middle_photo'}).a['href']
    except AttributeError as a:
        print(a)
        i = i + 1
        continue
    else:
        try:
            imagePageHTML = urlopen(imagePage)
        except HTTPError as h:
            print(h)
        else:
            imagePageBS = BeautifulSoup(imagePageHTML, 'html.parser')
            firstImageURL = imagePageBS.find('img', {'src':re.compile('\/o\.jpg')})
            firstImageDate = imagePageBS.find('span', {'class':'selected-photo-upload-date time-stamp'})
    try:
        dateText = firstImageDate.get_text()
        formattedDate = dateText.replace(',', '')
        rowString = str(idList[i]) + ', ' + str(salonList[i]) + ', ' + firstImageURL['src'] + ', ' + formattedDate + ', ' + str(j) + '\n'
    except TypeError as t:
        print(t)
    else:
        csvFile.write(rowString)
        print(str(imagePage) + ' written to csv(image ' + str(j) + ')')
        j = j + 1
    nextURL = homepage + imagePageBS.find('link', {'rel':'next'})['href']
    try:
        nextHTML = urlopen(nextURL)
    except HTTPError as h:
        print(h)
    else:
        nextBS = BeautifulSoup(nextHTML, 'html.parser')

    while nextBS.find('link', {'rel':'next'}) is not None:
        nextImage = nextBS.find('img', {'src':re.compile('\/o\.jpg')})
        nextDate = nextBS.find('span', {'class':'selected-photo-upload-date time-stamp'})
        try:
            dateText = nextDate.get_text()
            formattedDate = dateText.replace(',', '')
            rowString = str(idList[i]) + ', ' + str(salonList[i]) + ', ' + nextImage['src'] + ', ' + formattedDate + ', ' + str(j) + '\n'
        except (TypeError, AttributeError) as e:
            print(e)
        else:
            csvFile.write(rowString)
            print(str(nextURL) + ' written to csv(image ' + str(j) + ')')
            j = j + 1
        nextURL = homepage + nextBS.find('link', {'rel':'next'})['href']
        try:
            nextHTML = urlopen(nextURL)
        except HTTPError as h:
            print(h)
        else:
            nextBS = BeautifulSoup(nextHTML, 'html.parser')

        if nextBS.find('link', {'rel':'next'}) is None:
            nextImage = nextBS.find('img', {'src':re.compile('\/o\.jpg')})
            nextDate = nextBS.find('span', {'class': 'selected-photo-upload-date time-stamp'})
            try:
                dateText = nextDate.get_text()
                formattedDate = dateText.replace(',', '')
                rowString = str(idList[i]) + ', ' + str(salonList[i]) + ', ' + nextImage['src'] + ', ' + formattedDate + ', ' + str(j) + '\n'
            except (TypeError, AttributeError) as e:
                print(e)
            else:
                csvFile.write(rowString)
                print(str(nextURL) + ' written to csv(image ' + str(j) + ')')
                j = j + 1
    print('Images from ' + salonList[i] + ' successfully written to csv\n')
    i = i + 1










