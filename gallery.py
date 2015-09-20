import sys
import os
import requests
import lxml.html
import time

import page

xpath_gdt = '//div[@id="gdt"]'
xpath_ptb_tr = '//div[@class="gtb"]//tr'


cssselect_gdtm = 'div.gdtm'

def get_next_tab_url( doc ):
    print( "get_next_tab_url", doc )
    tab_nodes = doc.xpath( xpath_ptb_tr )[0]
    if tab_nodes is None:
        return None

    print( "get_next_tab_url 2", tab_nodes )
    next_el = tab_nodes[-1]
    if not next_el.get("onclick") or len( next_el.getchildren() ) == 0:
        return None

    print( "get_next_tab_url 2", next_el )
    return next_el.getchildren()[0].get("href")

xpath_title_gn = '//*[@id="gd2"]//*[@id="gn"]'
xpath_title_gj = '//*[@id="gd2"]//*[@id="gj"]'
def parse_gallery_name( doc ):
    gn_node = doc.xpath( xpath_title_gn )
    gj_node = doc.xpath( xpath_title_gj )
    # print( "name node num:", len(gn_node), len(gj_node) )

    return gn_node[0].text, gj_node[0].text

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

class HentaiGallery:
    def __init__( self, session, url, is_exmode = False, sleep_time = 0.5 ):
        self.session = session
        self.url = url
        self.is_exmode = is_exmode
        self.title_gn = "null"
        self.title_gj = "null"
        self.img_urls = []
        self.enabled = False
        self.sleep_time = sleep_time

    # def __str__( self ):
    #     return self

    def is_enabled( self ):
        return self.enabled

    def open( self ):
        self.name = "null"
        self.img_urls = []

        current_url = self.url

        try:
            while current_url:
                # 下载html
                print( "get current url", current_url )
                tab = self.session.get( current_url ).text
                # print( "tab htm:", tab )

                doc = lxml.html.document_fromstring( tab )

                # 从第一页中获取相册名
                if current_url == self.url:
                    ( self.title_gn, self.title_gj ) = parse_gallery_name( doc )

                # 获取当前页的图片url
                self.img_urls = self.img_urls + parse_tab_doc( doc )
                # print( "img_urls", self.img_urls )
            
                # 修眠，防止过快访问被ban
                time.sleep( self.sleep_time )

                # 获取下一页的url
                current_url = get_next_tab_url( doc )
        except Exception as e:
            with open( "failed.html", "w" ) as fo:
                fo.write( tab )

            print( "Get current_url error.\n", e )
            self.enabled = False
        else:
            self.enabled = True

            print( "Get all image urls:" )
            print( self.enabled )
            # for idx, url in enumerate( self.img_urls ):
            #     print( "url %d: %s" % ( idx, url ) )

    def get_name( self ):
        if self.title_gj:
            return self.title_gj
        else:
            return self.title_gn

    def get_all_image( self ):
        if not self.is_enabled():
            print( self.enabled, self.is_enabled() )
            print( "Can not open! Gallery is not enabled! Try open() first" )
            return None

        return self.img_urls

if __name__ == "__main__":
    pass
    from hentai_session import HentaiSession

    user_session = HentaiSession( )
    user_session.load_from_file( )

    url = "http://exhentai.org/g/852948/91d0a78b1c/"

    gallery = HentaiGallery( user_session, url )
    gallery.open( )
