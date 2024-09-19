from bs4 import BeautifulSoup
import requests
import pandas as pd

def list_printer(input):
    counter = 1
    for element in input:
        print(f"{counter}. {element}")
        counter += 1

# Set up
headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = 'https://www.thejakartapost.com/business'
response = requests.get(url, headers=headers)
parsed_content = BeautifulSoup(response.text, "html.parser")

# Data
article_titles = []
categories = []
page_links = []
dates = []
subscription_required = []

for i in parsed_content.select('div.latestDetail'):
    article_titles.append(i.find('h2', class_='titleNews').get_text().strip())
    categories.append(i.find('span', class_='dt-news').get_text().strip())

    anchors = i.find_all('a')
    page_links.append('https://www.thejakartapost.com' + str(anchors[1]['href']))

    date_spans = i.find_all('span', class_='date')
    dates.append(date_spans[1].get_text().strip())

    if i.select('span.premiumBadge'):
        subscription_required.append(True)
    else:
        subscription_required.append(False)

# Convertion
df = pd.DataFrame(
    {
        'article title': article_titles,
        'categories': categories,
        'article link': page_links,
        'dates': dates,
        'subscription': subscription_required
    }
)

df.to_csv('b.csv', index=False)