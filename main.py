
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

raw_url = 'https://www.charta-der-vielfalt.de'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
info_list = []
total_page_number = 566
for page in range(1,3):
    header = random.choice(user_agents)
    headers={'User-Agent': header}
    url = f'https://www.charta-der-vielfalt.de/en/diversity-charter-association/signatory-data-base/list/seite/{page}/'
    response = requests.get(url, headers=headers,timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        t_default_items = soup.find_all('div', class_='t_default-item')

        for item in t_default_items:
            # Find h2 element within the current div
            h2_element = item.find('h2')

            # Find 'a' element within the h2 element
            a_element = h2_element.find('a')

            # Extract href and text from the 'a' element
            href = a_element.get('href')
            topic_url = raw_url+href
            topic_name = a_element.text.strip()

            # Print or process the extracted information as needed
            data_dict = {'Name (title)':topic_name}

            response = requests.get(topic_url, headers=headers,timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find the table element
                table = soup.find('table')
                address = soup.find('address')

                # Check if the table is found
                if table:
                    # Find all 'tr' elements within the table
                    rows = table.find_all('tr')

                    for row in rows:
                        # Find all 'td' elements within the current row
                        columns = row.find_all('td')
                        # Check if there are at least two 'td' elements in the row
                        if len(columns) >= 2:
                            # Extract text from the first and second 'td' elements
                            key = columns[0].text.strip()
                            value = columns[1].text.strip()

                            # Add the key-value pair to the dictionary
                            data_dict[key] = value

                # Print or process the extracted dictionary as needed
                if address:
                    addr = address.find_all('a')
                    if addr:
                        for adr in addr:
                            href = adr.get('href')
                            if not href.startswith('javascript'):
                                data_dict['Website'] = href
                print(data_dict)
                info_list.append(data_dict)
                print('-'*50)

            else:
                print(f"Failed to fetch the URL. Status code: {response.status_code}")
            time.sleep(10)

    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")

    

df = pd.DataFrame(info_list)
print(df)
df.to_excel('data.xlsx', index=False)
