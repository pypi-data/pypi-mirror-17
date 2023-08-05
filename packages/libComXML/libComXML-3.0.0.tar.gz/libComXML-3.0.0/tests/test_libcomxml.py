# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import six

import unittest
import locale
import re
from libcomxml.core import XmlField, XmlModel, clean_xml


class Cd(XmlModel):

    _sort_order = (
        'artist', 'country', 'company', 'title', 'year', 'price'
    )

    def __init__(self):
        self.data = XmlField('CD')
        self.title = XmlField('TITLE')
        self.artist = XmlField('ARTIST')
        self.country = XmlField('COUNTRY')
        self.company = XmlField('COMPANY')
        self.price = XmlField('PRICE')
        self.year = XmlField('YEAR')
        super(Cd, self).__init__('CD', 'data')


class Catalog(XmlModel):
    def __init__(self):
        self.catalog = XmlField('CATALOG')
        self.cds = []
        super(Catalog, self).__init__('CATALOG', 'catalog')


class TestCleaned(unittest.TestCase):
    def setUp(self):
        self.xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
        self.xml += """
<CATALOG>
    <CD>
        <ARTIST>Bob Dylan</ARTIST>
        <ARTIST>Bob Dylan</ARTIST>
        <COMPANY>Columbia</COMPANY>
        <TITLE>Empire Burlesque</TITLE>
        <YEAR>1985</YEAR>
        <PRICE>10.9</PRICE>
    </CD>
</CATALOG>"""
        self.cleaned_xml = "<?xml version='1.0' encoding='UTF-8'?>"
        self.cleaned_xml += "<CATALOG><CD><ARTIST>Bob Dylan</ARTIST>"
        self.cleaned_xml += "<ARTIST>Bob Dylan</ARTIST>"
        self.cleaned_xml += "<COMPANY>Columbia</COMPANY>"
        self.cleaned_xml += "<TITLE>Empire Burlesque</TITLE><YEAR>1985</YEAR>"
        self.cleaned_xml += "<PRICE>10.9</PRICE></CD></CATALOG>"

    def test_clean(self):
        self.assertEqual(clean_xml(self.xml), self.cleaned_xml)


class TestFields(unittest.TestCase):
    def setUp(self):
        self.field = XmlField('Quantity', '10000', attributes={'uom': 'unit'})

    def test_attributes(self):
        self.assertEqual(self.field.attributes, {'uom': 'unit'})
        self.assertEqual(self.field.element().items(), [('uom', 'unit')])

    def test_str(self):
        self.assertEqual(six.text_type(self.field),
                         '<Quantity uom="unit">10000</Quantity>')

    def test_value(self):
        self.assertEqual(self.field.element().text, '10000')

    def test_value_rep(self):
        formated = locale.format('%i', value=int(self.field.value),
                                 grouping=True)
        self.field.rep = lambda value: locale.format('%i', value=int(value),
                                                     grouping=True)
        self.assertEqual(formated, self.field.element().text)
        self.assertEqual(str(self.field),
                         '<Quantity uom="unit">{0!s}</Quantity>'.format(formated))

    def test_update_attributes(self):
        self.field.attributes.update({'uom': 'kg'})
        self.assertEqual(self.field.attributes, {'uom': 'kg'})
        self.assertEqual(self.field.element().items(), [('uom', 'kg')])


class TestModel(unittest.TestCase):

    def setUp(self):
        self.xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
        self.xml += re.sub('\s+<', '<', """
<CATALOG>
    <CD>
        <ARTIST>Bob Dylan</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>Columbia</COMPANY>
        <TITLE>Empire Burlesque</TITLE>
        <YEAR>1985</YEAR>
        <PRICE>10.9</PRICE>
    </CD>
    <CD>
        <ARTIST>Bonnie Tyler</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>CBS Records</COMPANY>
        <TITLE>Hide your hear</TITLE>
        <YEAR>1988</YEAR>
        <PRICE>9.9</PRICE>
    </CD>
    <CD>
        <ARTIST>Van Morrison</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>Polydor</COMPANY>
        <TITLE>Tupelo Honey</TITLE>
        <YEAR>1971</YEAR>
        <PRICE>8.20</PRICE>
    </CD>
</CATALOG>""")
        self.catalog = Catalog()
        cd = Cd()
        cd.feed({
            'title': 'Empire Burlesque',
            'artist': 'Bob Dylan',
            'country': 'USA',
            'company': 'Columbia',
            'price': 10.90,
            'year': 1985
        })

        self.catalog.cds.append(cd)
        cd = Cd()
        cd.feed({
            'title': 'Hide your hear',
            'artist': 'Bonnie Tyler',
            'country': 'UK',
            'company': 'CBS Records',
            'price': 9.90,
            'year': 1988
        })
        self.catalog.cds.append(cd)
        cd = """<CD>
        <ARTIST>Van Morrison</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>Polydor</COMPANY>
        <TITLE>Tupelo Honey</TITLE>
        <YEAR>1971</YEAR>
        <PRICE>8.20</PRICE>
        </CD>"""
        self.catalog.cds.append(cd)
        self.catalog.build_tree()

    def test_xml(self):
        with open('/tmp/x1.xml', 'wb') as f:
            f.write(self.xml.encode('utf8'))
        with open('/tmp/x2.xml', 'wb') as f:
            f.write(self.catalog.serialize())
        self.assertEqual(self.xml.encode('utf8'), self.catalog.serialize())


class TestEmpty(unittest.TestCase):

    def setUp(self):
        self.xml = "<?xml version='1.0' encoding='UTF-8'?>\n<feed>"
        self.xml += "<test>foo</test><link href=\"http://example.com\"/>"
        self.xml += "<entry><val>1</val></entry><entry><val>2</val></entry>"
        self.xml += "</feed>"
        self.xml = self.xml.encode('utf8')

    def test_empty(self):

        class Feed(XmlModel):
            def __init__(self):
                self._sort_order = ('test', 'link', 'entries')
                self.rss_feed = XmlField('feed')
                self.link = XmlField('link')
                self.test = XmlField('test')
                self.entries = []
                super(Feed, self).__init__('feed', 'rss_feed', drop_empty=False)

        class Entry(XmlModel):
            def __init__(self):
                self.entry = XmlField('entry')
                self.val = XmlField('val')
                super(Entry, self).__init__('entry', 'entry')


        feed = Feed()
        feed.link.attributes.update({'href': 'http://example.com'})
        feed.feed({'test': 'foo'})

        for elem in (1, 2):
            entry = Entry()
            entry.feed({'val': elem})
            feed.entries.append(entry)

        feed.build_tree()

        self.assertEqual(self.xml, feed.serialize())


class RootWithAttributes(unittest.TestCase):

    def setUp(self):
        self.xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
        self.xml += "<link href=\"http://example.com\"/>"
        self.xml = self.xml.encode('utf8')

    def test_root_with_attributes(self):

        class Link(XmlModel):

            _sort_order = ('tag', )

            def __init__(self):
                self.tag = XmlField('link')
                super(Link, self).__init__('Link', 'tag', drop_empty=False)

        l = Link()
        l.tag.attributes.update({'href': 'http://example.com'})
        l.build_tree()

        self.assertEqual(self.xml, l.serialize())


class Namespaces(unittest.TestCase):
    def setUp(self):
        self.xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
        self.xml += "<rss "
        self.xml += "xmlns:atom=\"http://www.w3.org/2005/Atom\" "
        self.xml += "xmlns:opensearch=\"http://a9.com/-/spec/opensearch/1.1/\" "
        self.xml += "version=\"2.0\">"
        self.xml += "<channel><link>http://example.com/New+York+history</link>"
        self.xml += "<atom:link "
        self.xml += "href=\"http://example.com/opensearchdescription.xml\" "
        self.xml += "rel=\"search\" "
        self.xml += "type=\"application/opensearchdescription+xml\"/>"
        self.xml += "<opensearch:totalResults>4230000</opensearch:totalResults>"
        self.xml += "</channel>"
        self.xml += "</rss>"
        self.xml = self.xml.encode('utf8')

    def test_namesapces_root(self):

        self.maxDiff = None

        NAMESPACES = {
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'atom': 'http://www.w3.org/2005/Atom'
        }

        class Channel(XmlModel):

            _sort_order = ('link', 'atom_link', 'os_total_results')

            def __init__(self):
                self.channel = XmlField('channel')
                self.link = XmlField('link')
                self.atom_link = XmlField(
                    'link', namespace=NAMESPACES['atom']
                )
                self.os_total_results = XmlField(
                    'totalResults', namespace=NAMESPACES['opensearch']
                )
                super(Channel, self).__init__('Channel', 'channel', drop_empty=False)

        class Rss(XmlModel):

            _sort_order = ('channel', )

            def __init__(self):
                self.tag = XmlField('rss', attributes={
                    'version': '2.0', 'nsmap': NAMESPACES
                })
                self.channel = Channel()
                super(Rss, self).__init__('RSS', 'tag', drop_empty=False)

        rss = Rss()
        rss.channel.atom_link.attributes.update({
            'rel': 'search',
            'type': 'application/opensearchdescription+xml',
            'href': 'http://example.com/opensearchdescription.xml'
        })
        rss.channel.feed({
            'link': 'http://example.com/New+York+history',
            'os_total_results': 4230000,
        })
        rss.build_tree()

        self.assertEqual(
            self.xml, rss.serialize()
        )

