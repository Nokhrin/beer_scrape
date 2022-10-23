import requests
import config
import pandas as pd
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logs/beer.log',
                    filemode='w')

try:
    page_response = requests.get(url=config.URL)
    page_response.raise_for_status()
    # logging.info(msg=page_response.url)
    # logging.info(msg=page_response.status_code)

    page_content_soup = BeautifulSoup(page_response.content, 'html.parser')
    # logging.info(msg=page_content_soup)

    beer_table = page_content_soup.find('div', class_='table-responsive').table
    beer_rows = beer_table.find_all('tr')

    names = []
    types = []
    links = []

    beer_type = 'n/a'
    for beer_row in beer_rows:
        beer_cells = beer_row.find_all('td')

        for beer_cell in beer_cells:
            beer_link = 'no link'

            if 'rowspan' in beer_cell.attrs:
                beer_type = beer_cell.text.split(' – ')[0]

            if beer_cell.a:
                beer_name = beer_cell.text
                beer_link = beer_cell.find('a')['href']

                names.append(beer_name)
                types.append(beer_type)
                links.append(beer_link)

    beer_data = pd.DataFrame({
        'name': names,
        'type': types,
        'link': links
    })

    beer_data.to_csv('output/BJCP_classification.csv', sep=';')

except Exception as e:
    logging.error(msg=e)
