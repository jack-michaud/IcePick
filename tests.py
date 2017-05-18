import unittest
import utils
from IcePick import HTMLStructureElt, EmptyHTMLElt, IcePick
from bs4 import BeautifulSoup
import requests

class HTMLStructureEltTestCase(unittest.TestCase):
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



class IcePickTestCase(unittest.TestCase):
    emptystructure = EmptyHTMLElt()
    structure1 = HTMLStructureElt("a", emptystructure, emptystructure, label="name")
    structure2 = HTMLStructureElt("div", emptystructure, emptystructure, label="date")
    structure3 = HTMLStructureElt("div", structure2, emptystructure, label="text")
    structure4 = HTMLStructureElt("h3", structure3, structure1)
    structure5 = HTMLStructureElt("div", emptystructure, structure4, label="container")

    def setUp(self):
        self.response = requests.get('https://mbasic.facebook.com/photo.php?fbid=873660689404554&id=100002818929893&')

        soup = BeautifulSoup(self.response.text, 'html.parser')
        soup = soup.find(id="MPhotoContent")
        self.ice = IcePick(soup, self.structure5)

    def test_comments(self):
        posts = self.ice.find()
        self.assertTrue(all([self.structure5.correct_soup(post) for post in posts]))

    def test_dictify(self):
        posts = self.ice.dictify()

        test1 = all([len(post) == 5 for post in posts])
        test2 = True
        prev_post = {'raw': None}
        posts = self.ice.dictify()
        for ice_post in posts:
            test2 = test2 and ice_post['raw'] != prev_post['raw']
            prev_post = ice_post

        self.assertTrue(test1 and test2)

    def test_label(self):
        label = "name"
        found = self.ice.get_label(label)
        self.assertTrue(found is not None)

    def test_sculpt(self):

        html = """<div><h3 class="br cj"><strong><a href="TESTHREF">Joe Stephenson</a></strong></h3></div>"""
        soup = BeautifulSoup(html, 'html.parser')
        attribute = "href"

        structure = utils.sculpt_structure(soup, attribute)
        ice = IcePick(soup, structure)
        ice.find()

        self.assertTrue(ice.get_label("TESTHREF")[0], BeautifulSoup("""<a href="TESTHREF">Joe Stephenson</a>""", 'html.parser'))

    # TODO - would be cool
    # def test_optional(self):
    #     html = """<div><a optional=""></a><h3 class="br cj"><strong><a href="TESTHREF">Joe Stephenson</a></strong></h3></div>"""
    #     html1 = """<div><h3 class="br cj"><strong><a href="TESTHREF">Joe Stephenson</a></strong></h3></div>"""
    #     soup = BeautifulSoup(html, 'html.parser')
    #     soup1 = BeautifulSoup(html1, 'html.parser')
    #     attribute = "href"
    #
    #     structure = utils.sculpt_structure(soup, attribute)
    #     ice1 = IcePick(soup1, structure)
    #     ice1.find()
    #
    #     self.assertTrue(ice1.find() is not [])


if __name__ == '__main__':
    unittest.main()
