import sys
import os
import requests
import lxml.html


xpath_gdt = '//div[@id="gdt"]'
xpath_ptb_tr = '//div[@class="gtb"]//tr'

xpath_title = '//*[@id="gn"]/text()'

cssselect_gdtm = 'div.gdtm'

def get_next_tab_url( doc ):
    tab_nodes = doc.xpath( xpath_ptb_tr )[0]
    if tab_nodes is None:
        return None

    next_el = tab_nodes[-1]
    if not next_el.get("onclick") or len( next_el.getchildren() ) == 0:
        return None

    return next_el.getchildren()[0].get("href")

def parse_tab_doc( doc ):
    list = []
    try:
        node = doc.xpath( xpath_gdt )
        for idx, el in enumerate( doc.cssselect( cssselect_gdtm ) ):
            # print( "gdtm ", idx, el.tag )
            img_node = el.getchildren()[0].getchildren()[0]
            # print( "image tab url:", img_node.attrib["href"] )
            list.append( img_node.attrib["href"] )
    except Exception as e:
        print( "function parse_tab_doc() can not parse the doc.\n",  e )
        list = []
        pass

    return list

class EHentaiGallery:
    def __init__( self, session, url, is_exmode = False ):
        self.session = session
        self.url = url
        self.is_exmode = is_exmode
        self.img_urls = []
        self.enabled = False

    # def __str__( self ):
    #     return self

    def is_enabled( self ):
        return self.enabled

    def open( self ):
        self.img_urls = []

        current_url = self.url

        try:
            while current_url:
                tab = self.session.get( current_url ).text
                doc = lxml.html.document_fromstring( tab )
            
                self.title = doc.xpath( xpath_title )
                self.img_urls = self.img_urls + parse_tab_doc( doc )
            
                current_url = get_next_tab_url( doc )
        except Exception as e:
            print( "get current_url error.\n", e )
            self.is_enabled = False
        else:
            self.is_enabled = True

            print( "get all image urls:" )
            for idx, url in enumerate( self.img_urls ):
                print( "url %d: %s" % ( idx, url ) )

    def get_all_image( self ):
        if not self.is_enabled():
            print( "can not open! Gallery is not enabled! Try open() first" )
            return None

        return self.img_urls

if __name__ == "__main__":
    gallery = EHentaiGallery( requests.Session(), "http://g.e-hentai.org/g/849492/eda7c42b07/" )
    gallery.open( )
