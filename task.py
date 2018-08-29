# Python3.7
import csv
from requests import get
from bs4 import BeautifulSoup
import pandas as pd


url = ('http://www.wegottickets.com/searchresults/page/1/adv#paginate')

page = 0

while True:

    print('--', page, '--')

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    event_containers = html_soup.find_all('div', class_ = 'content block-group chatterbox-margin')

    extracted_data = []

    for container in event_containers:
        if container.find('div', class_ = 'searchResultsPrice') is not None:

            artist = container.h2.a.text
            detail = container.div.find('div', class_ = 'venue-details').text.replace('\n', ' ')
            price = container.find('div', class_ = 'searchResultsPrice').strong.text            
            extracted_data.append({'artist': artist, 'details': detail, 'price': price})

    event_data = pd.DataFrame(extracted_data)

    with open('event_data1.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(extracted_data)

    # Link to next page
    next_page = html_soup.find('a', {'class': 'pagination_link_text nextlink'})

    if next_page:
        url = next_page.get('href')
        page += 1
    else:
        break # exit `while True`
