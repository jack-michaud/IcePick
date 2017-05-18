
## Usage

Let's scrape the homepage of the [Python 2.7 documentation](https://docs.python.org/2.7/).

I'm looking to scrape the "Parts of the documentation", so I look at the source.

![docs](https://github.com/jack-michaud/IcePick/blob/master/docs/Python_2_7_13_documentation.png)

The barebones of the heirarchy is all that we need. You will see this in the "faux_html" in the example...

```python

from iPick.utils import sculpt_structure
from iPick import IcePick

from bs4 import BeautifulSoup
import requests

# Craft up the framework of the HTML you want to scrape.  
# Note the label attribute. These will be used to reference elements with IcePick.dictify (used later).
faux_html = """
  <p>
    <a label="title"></a>
    <br/>
  </p>
"""

# Make the HTML into a soup (no spaces, tabs, or newlines)
faux_soup = BeautifulSoup(faux_html.replace('  ', '').replace('\n',''), 'html.parser')

# Use the "sculpt_structure" utility to make a structure out of that faux soup.
# Note: you CAN manually create the crazy recursive data structure, but I made the utility to make it easier.
documentation_topics_structure = sculpt_structure(faux_soup, label_attribute='label')

```
The setup of IcePick is all done. Now to scrape:

```python

response = requests.get('https://docs.python.org/2.7/')
soup = BeautifulSoup(response.text, 'html.parser')

# Here comes IcePick!
ice = IcePick(soup, documentation_topics_structure)
# It's set up.

```
### ice.find()
Finds the soups of all HTML that match the structure. 

```python

>>> ice.find()
[<p class="biglink"><a class="biglink" href="whatsnew/2.7.html">What's new in Python 2.7?</a><br/>\n<span class="linkdescr">or <a href="whatsnew/index.html">all "What's new" documents</a> since 2.0</span></p>, ..... ]

```

### ice.dictify() (Useful!)
Retrieves the soups of the elements that are labeled in a dict. Also includes the raw soup in the key 'raw'.

```python

>>> ice.dictify()
[{u'description': <span class="linkdescr">or <a href="whatsnew/index.html">all "What's new" documents</a> since 2.0</span>,
  u'title':       <a class="biglink" href="whatsnew/2.7.html">What's new in Python 2.7?</a>,
   'raw':         ... }, .....]
```
Here's an example where we enumerate the titles and descriptions of all the topics in the docs.

```python

for ice_tag in ice.dictify():
    print ice_tag['title'].get_text()
    print ice_tag['description'].get_text()
    print ""

```


#### IMPORTANT Note on the IcePick searching algorithm
If the faux HTML constructed has no specific children or siblings in the HTML tree, IcePick will not check those children or siblings when given a soup to search. 
That means, for example, if the faux HTML is:
```html
<div>
  <p></p>
</div>
```
...IcePick may retrieve both this:
```html
<div>
  <p>
    <span>Yo!</span>
  </p>
</div>
```
...and this:
```html
<div>
  <p>Crank that!</p>
  <p>Quietly :)</p>
</div>
```
(If you have questions, please make an issue and I'll clarify and add it to the docs/readme)
