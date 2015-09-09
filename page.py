import sys
import os
import requests
import lxml.html
import time

sleep_time = 0.5

cssselect_page = "img"

# judge is the targe img url
def is_target_img_url( node ):
        parent = node.getparent()
        grandpa = parent.getparent()

        if parent.attrib.get("href") and grandpa.attrib.get("class") and grandpa.attrib["class"] == "sni":
            return True

        return False

def parse_page_doc( doc ):
    image_url = None
    gallery_url = None

    # find image url
    for idx, node in enumerate( doc.cssselect( cssselect_page ) ):
        if is_target_img_url( node ):
            # print( "node", idx, node.attrib.get("src") )
            image_url = node.attrib.get("src")
            break

    # find gallery url
    gallery_url = doc.find_class( "sb" )[0].getchildren()[0].attrib.get("href")

    return ( image_url, gallery_url )

class EHentaiPage:
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.enabled = False

    def is_enabled( self ):
        return self.enabled

    def open( self ):
        try:
            request_obj = self.session.get( self.url )
            page = request_obj.text
            print( "cookie", request_obj.cookies )
            time.sleep( sleep_time )

            doc = lxml.html.document_fromstring( page )
            
            ( self.image_url, self.gallery_url ) = parse_page_doc( doc )
        except Exception as e:
            print( "open page(%s) failed." % self.url )
            print( e )
            self.enabled = False
        else:
            self.enabled = True
            print( "open page(%s) successed." % self.url )

    def save( self, file_name ):
        if not self.is_enabled():
            print( "Page is not enabled! Try to open() first!" )
            return False

        with open( file_name, 'wb' ) as f:
            print( "save ", self.image_url )
            f.write( requests.get( self.image_url ).content )
            return True
        
        return False

if __name__ == "__main__":
    url = "http://g.e-hentai.org/s/a9ce8f9499/849496-1"
    page = EHentaiPage( requests.Session(), url )
    path = os.path.join( "pic", "test.png" )
    page.open( )
    page.save( path )
