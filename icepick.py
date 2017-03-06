'''
Parser that takes html structure into account when searching html text.

'''
class IcePick:

    def __init__(self, soup, structure):
        '''
        Initializer
        :param soup:      Beautifulsoup object to search
        :param structure: HTMLStructure to search for
        '''
        self.soup = soup # type: BeautifulSoup
        self.structure = structure # type: HTMLStructure



    def find(self):
        '''

        :return: Array of dicts
        '''

        structure = self.structure
        soup = self.soup

        return structure.take_soup(soup)



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
        '''

        :param soup:
        :return:
        '''
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



class HTMLStructureElt(HTMLStructure):


    def __init__(self, name, sibling, child, label=None):
        '''

        :param name:    name of the html element.
        :param sibling: next element that is the sibling.
        :param child:   the first descendant
        :param label:   a custom name for this element in the structure.
        '''
        self.name = name
        self.sibling = sibling
        self.child = child
        self.label = label

    def pprint(self, indent=0):
        indentation = "\t" * indent
        return indentation + "<" + self.name + ">\n" \
               + self.child.pprint(indent=indent + 1) \
            + "\n" + indentation + "</" + self.name + ">\n" + self.sibling.pprint(indent=indent)

    def take_soup(self, soup):
        soups = soup.find_all(self.name)

        return filter(lambda s: self.correct_soup(s), soups)

    def correct_soup(self, soup):
        '''

        :param soup:
        :type soup: BeautifulSoup
        :return:
        '''
        if soup is None:
            return False

        return self.correct_soup_siblings(soup)

    def correct_soup_siblings(self, soup):
        '''

        :type soup: BeautifulSoup
        :return:
        '''
        if soup.name == "[document]":
            soup = soup.contents[0]

        return self.name == soup.name and self.sibling.correct_soup_siblings(soup.next_sibling) and \
               self.child.correct_soup(soup.contents[0])
