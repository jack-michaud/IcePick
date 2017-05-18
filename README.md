# IcePick
IcePick offers a highly accurate method of scraping. It's a new way to scrape HTML - sorting by structure instead of classes and IDs.

## What do I use IcePick for?

I scrape social media data in my webapp [Harrow Search](https://harrowsearch.com). **IcePick is instrumental in scraping Facebook** because of the myriad of similarly structured data items that appear on the site. (The Facebook API does not offer what I need, no. IcePick helped me construct an ad hoc API!)

## Usage

Check out the [IcePick documentation README](https://github.com/jack-michaud/IcePick/blob/master/docs/README.md) for an example of scraping the Python docs.

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

