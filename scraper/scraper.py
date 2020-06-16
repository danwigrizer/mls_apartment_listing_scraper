import requests
import lxml
from bs4 import BeautifulSoup
import pprint
import unicodedata
import re
import csv

# start the requests session

session = requests.Session()

# Log into MLS with user name and password post of payload - Need to send them data

payload = {'user': 'wigrizer@gmail.com',
           'pass': 'chris'}
login = session.post("https://vow.mlspin.com/clients/validate.aspx?id=332068", data=payload)


# pull a csv of each location, url, rent, bed
base_url = 'https://vow.mlspin.com/clients/'
filename = "apartments3.csv"

#f = open(filename, "w")

# Use with statement to open file so you don't need to forget about closing it
with open("/Users/danwigrizer/dev/projects/scraper/data/" + filename, "w") as f:

    # go through each page of the report
    for i in range(1, 2):
        # Get list of apartments
        list_of_apartments = session.get("https://vow.mlspin.com/clients/index.aspx?p=" + str(i))

        # convert listings it into text
        soup = BeautifulSoup(list_of_apartments.text, 'lxml')

        for listing in soup.findAll('tr', {'bgcolor': True}):

            # find all urls tht dont have javascript and make it into a url using base url
            urls = [base_url + a['href'] for a in listing.findAll('a') if not re.compile("javascript").search(a['href'])]

            #remove unicode
            descriptions = ([unicodedata.normalize("NFKD",a.text.strip()) for a in listing.findAll('td')])
            urls.extend(descriptions)

            # seperate each value into comma seperated form
            # add a comma to seperate bathroom and picture count
            # remove the comma in the cost
            # remove blanks
            joined_data = [', '.join([re.sub('(?<=[0-9])[,](?=[0-9])', "", x.replace("(Rental)x", ",")) for x in urls if x != ''])]

            #print(apartment_data[0].replace("apartment (Rental)x", ","))
            #apartment_data = [x for x in urls if x != '']
            apartment_data = [x.split(',') for x in joined_data]

            #print(apartment_data)
            writer = csv.writer(f)
            writer.writerows(apartment_data)







       #if not re.compile("javascript").search(row):
           # print = f'{row not idk == 1}'
# Test prints


