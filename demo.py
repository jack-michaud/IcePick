
from utils import sculpt_structure
from IcePick import IcePick

from bs4 import BeautifulSoup
import requests

faux_html = """
  <p>
    <a label="title"></a>
    <br/>
    <span label="description"></span>
  </p>
"""
faux_soup = BeautifulSoup(faux_html.replace('  ', '').replace('\n',''), 'html.parser')

'''
Labels:
- title
- description
'''
documentation_topics_structure = sculpt_structure(faux_soup, label_attribute='label')


response = requests.get('https://docs.python.org/2.7/')
soup = BeautifulSoup(response.text, 'html.parser')

ice = IcePick(soup, documentation_topics_structure)

for ice_tag in ice.dictify():
    print ice_tag['title'].get_text()
    print ice_tag['description'].get_text()
    print ""
