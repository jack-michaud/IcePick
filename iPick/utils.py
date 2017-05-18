
from bs4 import BeautifulSoup, element
from IcePick import HTMLStructure, HTMLStructureElt, EmptyHTMLElt


def sculpt_structure(soup, label_attribute=None):
    '''

    :param soup:            The soup object to generate HTMLStructure from
    :type soup:             BeautifulSoup
    :param label_attribute: The attribute of a soup element that becomes an HTMLStructure label.
    :type label_attribute:  str
    :return:                The HTMLStructure to use in an IcePick object
    :rtype:                 HTMLStructure
    '''
    if soup is None or type(soup) == element.NavigableString or type(soup) == str:
        return EmptyHTMLElt()
    if soup.name == u"[document]":
        soup = soup.contents[0]

    temp_soup = soup
    try:
        child_soup = soup.contents[0]
    except IndexError:
        child_soup = None

    sibling_soup = temp_soup.findNextSibling()

    return HTMLStructureElt(soup.name,
                            sculpt_structure(sibling_soup, label_attribute),
                            sculpt_structure(child_soup, label_attribute),
                            soup.get(label_attribute),
                            soup.get('placeholder') is not None)
