from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup, element

'''
Parser that takes html structure into account when searching html text.

'''
class IcePick:

    __identity = lambda self, x: x

    def __init__(self, soup, structure, default_stringifier=None):
        '''
        Initializer
        :param soup:      Beautifulsoup object to search
        :param structure: HTMLStructure to search for
        :param default_stringifier: anonymous function to apply to the html content
        '''
        import types
        if type(default_stringifier) != types.LambdaType:
            self.default_stringifier = self.__identity

        if type(soup) != element.Tag and type(soup) != BeautifulSoup:
            raise TypeError("Constructor must take a BeautifulSoup object for 'soup'.")
        self.soup = soup # type: BeautifulSoup

        if type(structure) != HTMLStructure and \
           type(structure) != HTMLStructureElt and \
           type(structure) != EmptyHTMLElt:
            raise TypeError("Constructor must take a HTMLStructure object for 'structure'.")
        self.structure = structure # type: HTMLStructure

        self.elements = []



    def find(self):
        '''

        :return: Array of dicts
        '''

        structure = self.structure
        soup = self.soup

        self.elements = [self.default_stringifier(x) for x in structure.take_soup(soup)]
        return self.elements

    def dictify(self):
        if self.elements == []:
            self.find()
        soups = self.elements

        return [self.structure.dictify_content(elt, {}) for elt in soups]

    def exists(self):
        if self.elements == []:
            self.find()

        return self.elements != []

    def get_label(self, label):


        return [self.structure._get_label(label, element) for element in self.elements]


class HTMLStructure:

    __metaclass__ = ABCMeta

    @abstractmethod
    def pprint(self, indent=0):
        pass

    @abstractmethod
    def take_soup(self, soup):
        pass

    @abstractmethod
    def correct_soup(self, soup):
        '''
        :param soup:  A beautifulsoup object to check if its the right object
        :type soup: BeautifulSoup
        :rtype: bool
        '''
        pass

    @abstractmethod
    def correct_soup_siblings(self, soup):
        pass

    @abstractmethod
    def dictify_content(self, soup, content={}):
        pass

    @abstractmethod
    def _get_label(self, label, soup):
        pass

class EmptyHTMLElt(HTMLStructure):


    def __init__(self):
        pass

    def pprint(self, indent=0):
        return ""

    def take_soup(self, soup):
        return []

    def correct_soup(self, soup):
        return True

    def correct_soup_siblings(self, soup):
        return True

    def dictify_content(self, soup, content={}):
        return content

    def _get_label(self, label, soup):
        pass



class HTMLStructureElt(HTMLStructure):


    def __init__(self, name, sibling, child, label=None, optional=False):
        '''

        :param name:     name of the html element.
        :param sibling:  next element that is the sibling.
        :param child:    the first descendant
        :param label:    a custom name for this element in the structure.
        :param optional: flag saying that this element does not need to be here
                         for a soup to be this structure.
        '''
        self.name = name
        self.sibling = sibling
        self.child = child
        self.label = label
        self.optional = optional

    def pprint(self, indent=0):
        indentation = "\t" * indent
        parens_open = ""
        parens_close = ""

        if self.optional:
            parens_open = "("
            parens_close = ")"

        return indentation + parens_open + "<" + self.name + ">\n" \
               + self.child.pprint(indent=indent + 1) \
            + "\n" + indentation + "</" + self.name + ">" + parens_close +"\n" + self.sibling.pprint(indent=indent)

    def take_soup(self, soup):
        soups = soup.find_all(self.name)

        return filter(lambda s: self.correct_soup(s), soups)

    def correct_soup(self, soup):
        '''

        :type soup: BeautifulSoup
        :return: bool
        '''
        if soup is None:
            if self.optional:
                return True
            return False

        return self.correct_soup_siblings(soup)

    def correct_soup_siblings(self, soup):
        '''

        :type soup: BeautifulSoup
        :return: bool
        '''
        if soup is None:
            return False

        if soup.name == "[document]":
            soup = soup.contents[0]

        try:
            child_soup = soup.contents[0]
        except IndexError:
            child_soup = None
        except AttributeError:
            child_soup = None

        try:
            return self.name == soup.name and self.sibling.correct_soup_siblings(soup.findNextSibling()) and \
                   self.child.correct_soup(child_soup)
        except IndexError:
            return self.name == soup.name and self.sibling.correct_soup_siblings(soup.findNextSibling()) and \
                   self.child.correct_soup(None)

    def dictify_content(self, soup, content={}):
        if soup is None:
            return content
        if soup.name == "[document]":
            soup = soup.contents[0]
        if content.get('raw') is None:
            content['raw'] = soup

        if self.label is not None:
            content[self.label] = soup

        try:
            child_soup = soup.contents[0]
        except IndexError:
            child_soup = None
        except AttributeError:
            child_soup = None

        content = self.child.dictify_content(child_soup, content)
        content = self.sibling.dictify_content(soup.findNextSibling(), content)
        return content

    def _get_label(self, label, soup):
        if soup is None or type(soup) == element.NavigableString:
            return
        if label == self.label:
            return soup

        try:
            child_soup = soup.contents[0]
        except IndexError:
            child_soup = None

        child = self.child._get_label(label, child_soup)

        sibling = self.sibling._get_label(label, soup.findNextSibling())

        if child is not None:
            return child
        return sibling
