import sys
import os
import requests
import lxml.html
import time

import page



image_xpath = '//*[@id="i3"]/a/img'
gallery_xpath = '//*[@id="i5"]/div/a/img'

def parse_page_doc( doc ):
    image_url = None
    gallery_url = None

    # find image url
    find_nodes = doc.xpath( image_xpath )
    image_node = find_nodes[0]
    image_url = image_node.attrib.get("src")

    # find gallery url
    find_nodes = doc.xpath( gallery_xpath )
    gallery_node = find_nodes[0]
    gallery_url = gallery_node.get("href")

    print( image_url, gallery_url )

    return ( image_url, gallery_url )

class HentaiPage:
    """
    Parse Ehentai's pages, get image url, and save it.
    """

    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.enabled = False
        self.time_out = 3

    def is_enabled( self ):
        """is_enabled
    
        Args: None

        Returns: Boolean. True if the page is parsed.
    
        Raises:
        """
        return self.enabled

    def open( self ):
        """Download and parse the page.
    
        Args: None

        Returns: None
    
        Raises:
        """
        try:
            request_obj = self.session.get( self.url )
            page = request_obj.text
            with open( "test.html", "w" ) as file_obj:
                file_obj.write( page )
            print( "url:", self.url )
            # print( "page:", page )
            # print( "cookie", request_obj.cookies )

            doc = lxml.html.document_fromstring( page )
            
            ( self.image_url, self.gallery_url ) = parse_page_doc( doc )
        except Exception as e:
            print( "open page(%s) failed." % self.url )
            print( e )
            self.enabled = False
        else:
            self.enabled = True
            print( "open page(%s) successed." % self.url )

    def save( self, fold_name, file_name = None ):
        """save
    
        Args: 
            fold_name: #TODO
            file_name: #TODO

        Returns:
    
        Raises:
        """
        if not self.is_enabled():
            print( "Page is not enabled! Try to open() first!" )
            return False

        print( self.image_url, self.gallery_url )

        # 缺省文件名使用从url中获取的文件史
        if not file_name:
            file_name = os.path.split( self.image_url )[1]

        full_file_name = os.path.join( fold_name, file_name )

        # 当目录不存在时，自动创建目录
        if not os.path.exists( os.path.dirname( full_file_name ) ):
            os.makedirs( os.path.dirname( full_file_name ) )

        with open( full_file_name, 'wb+' ) as f:
            print( "save ", self.image_url )

            max_retry_time = 3
            retry_time = 0
            while retry_time < max_retry_time:
                try:
                    f.write( requests.get( self.image_url, timeout = self.time_out ).content )
                    break
                except requests.exceptions.Timeout as e:
                    print( "[Page] Download %s failed.time out.Retry %d" % ( self.image_url, retry_time ) )
                    retry_time += 1

                    if retry_time > max_retry_time:
                        raise e

            return True
        
        return False

if __name__ == "__main__":
    from hentai_session import HentaiSession

    # url = "http://g.e-hentai.org/s/a9ce8f9499/849496-1"
    url = "http://exhentai.org/g/852948/91d0a78b1c/"

    user_session = HentaiSession( )
    user_session.load_from_file( )

    page = HentaiPage( user_session, url )
    path = os.path.join( "pic", "1" )
    page.open( )
    # print( page.image_url, page.gallery_url )
    page.save( path )
