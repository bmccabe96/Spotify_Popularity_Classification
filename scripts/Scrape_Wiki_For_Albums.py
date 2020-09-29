import requests
from bs4 import BeautifulSoup
import pickle

# Create list of albums
albums = []

# Loop first through each wikipedia page of albums, one page per year
# Then, loop through the various HTML tags to grab the album names released in the year

for year in range(2015, 2021):
    url = "https://en.wikipedia.org/wiki/List_of_" + str(year) + "_albums"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for table in soup.find_all('table', class_='wikitable'):
        body = table.find('tbody')
        for tr in body.find_all('tr')[1:]:
            for td in tr.find_all('td'):
                if td.find('i'):
                    album = td.text.strip('\n')
                    albums.append((album, year))

# Save the resulting list in a pickle
pickle_out = open("albums_2015_to_2020.pickle","wb")
pickle.dump(albums, pickle_out)
pickle_out.close()