import requests
import pprint
from bs4 import BeautifulSoup
import re
import pandas as pd
#import urllib3

url = 'https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters'
#soup = BeautifulSoup(urllib3.urlopen(url).read())
page = requests.get(url)
#pprint.pprint(page.content)
soup = BeautifulSoup(page.content,'html.parser')
#body =  soup.find(id='bodyContent')
#tables = body.find_all(class_='wikitable')
##   print(table)
#print(table.prettify())
#row_array = []
chracter_names = []
for i in range(2):
    rows = soup.findAll(class_='wikitable')[i].tbody.findAll('tr')[2:]
    for row in rows:
        #row_array.append(row)
        char_name = row.findAll('td')[1].string
        chracter_names.append(char_name)

new_chars = []
for name in chracter_names:
    name = re.sub("\"\w+?\s*?\w*?\" ", "", name)
    name = re.sub("[-,']", "", name)
    new_chars.append(name)
#print(new_chars)

"""with open("outfile", "w") as outfile:
    outfile.write("\n".join(new_chars))"""

new_chars_df = pd.DataFrame(new_chars)
new_chars_df.to_csv(r'C:\Users\mheme\Desktop\GOT Names.csv',header=None, index=None)