from django.test import TestCase
from IcePick import HTMLStructureElt, EmptyHTMLElt, IcePick
from bs4 import BeautifulSoup
import requests

class HTMLStructureEltTestCase(TestCase):
    emptystructure = EmptyHTMLElt()
    structure1 = HTMLStructureElt("a", emptystructure, emptystructure)
    structure2 = HTMLStructureElt("div", emptystructure, emptystructure)
    structure3 = HTMLStructureElt("div", structure2, emptystructure)
    structure4 = HTMLStructureElt("h3", structure3, structure1)
    structure5 = HTMLStructureElt("div", emptystructure, structure4)

    soup1 = BeautifulSoup("<div><h3><a href=\"http://google.com\">Jacko</a></h3><div>great</div><div>1 like</div></div>", 'html.parser')
    soup2 = BeautifulSoup("<div><p>Not the right one!</p></div>", 'html.parser')

    def test_pprint(self):
        self.assertEqual(self.structure5.pprint(), '<div>\n\t<h3>\n\t\t<a>\n\n\t\t</a>\n\n\t</h3>\n\t<div>\n\n\t</div>\n\t<div>\n\n\t</div>\n\n</div>\n')

    def test_correct_soup1(self):
        self.assertTrue(self.structure5.correct_soup(self.soup1))

    def test_correct_soup2(self):
        self.assertFalse(self.structure5.correct_soup(self.soup2))

    def test_take_soup(self):
        self.assertEqual([str(self.soup1)], \
                         [str(x) for x in self.structure5.take_soup(self.soup1)])



class IcePickTestCase(TestCase):
    emptystructure = EmptyHTMLElt()
    structure1 = HTMLStructureElt("a", emptystructure, emptystructure)
    structure2 = HTMLStructureElt("div", emptystructure, emptystructure)
    structure3 = HTMLStructureElt("div", structure2, emptystructure)
    structure4 = HTMLStructureElt("h3", structure3, structure1)
    structure5 = HTMLStructureElt("div", emptystructure, structure4)

    
