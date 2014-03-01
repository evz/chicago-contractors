import scrapelib
from BeautifulSoup import BeautifulSoup
import csv

base_url = 'https://webapps.cityofchicago.org/activegcWeb/'

def parse_row(header, row):
    d = {}
    row = [r.text for r in row.findAll('td')]
    for k,v in zip(header, row):
        d[k] = v
    return d

def parse_page(soup):
    header_row = soup.find('tr', attrs={'class': 'gridStyle-tr-header'})
    headers = [t.text for t in header_row.findAll('td')]
    data_rows = soup.findAll('tr', attrs={'class': 'gridStyle-tr-alt-data'})
    data = []
    for row in data_rows:
        data.append(parse_row(headers, row))
    return data

def scrapeit(s):
    content = s.urlopen(base_url)
    soup = BeautifulSoup(content)
    data = parse_page(soup)
    links = []
    for a in soup.findAll('a'):
        href = a.get('href')
        if 'next' not in a and 'last' not in a:
            links.append(href)
    for link in links:
        content = s.urlopen('%s?%s' %(base_url, link))
        data.extend(parse_page(soup))
    return data

if __name__ == "__main__":
    s = scrapelib.Scraper()
    data = scrapeit(s)
    o = open('contractors.csv', 'wb')
    out = csv.DictWriter(o, fieldnames=data[0].keys())
    out.writeheader()
    out.writerows(data)
