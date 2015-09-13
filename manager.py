import time
import os
import requests
import json

from hentai_session import HentaiSession
from gallery import HentaiGallery
from page import HentaiPage


DATA_FILE_NAME = "hentai.json"

class HentaiDownloadManager:
    """
    HentaiDownloadManager's description.
    """

    def __init__( self ):
        """__init__
    
        Args: None

        Returns:
    
        Raises:
        """

        self.session = HentaiSession( )
        self.session.load_from_file( )

        self.sleep_time = 0.5

    def _check_finished( self, save_folder, urls ):
        """check if which images are always downloaded, and remove them from download list.
    
        Args: None

        Returns:
    
        Raises:
        """
    
        if not os.path.isdir( save_folder ):
            # print( "[HentaiManager]save folder is not exits", save_folder )
            return urls

        
        conf_file_name = os.path.join( save_folder, DATA_FILE_NAME )

        # test if config is exist
        try:
            file_obj = open( conf_file_name, "r" )
            task_status_tab = json.load( file_obj )
        # except requests.exceptions.Timeout as e:
        except:
            answer = input( "Foler(%s) is exist. Are you sure to overwrite it?(y/n):" % os.path.abspath( save_folder ) )
            if answer == "y":
                return urls
            else:
                return []

        remove_table = []
        for i, url in enumerate( urls ):
            # 若文件已下载成功，则不下载
            if url in task_status_tab.keys() and task_status_tab[url] != "False":
                remove_table.append( i )

        for index in sorted( remove_table, reverse=True ):
            print( "[HentaiManager] image %d(%s) is exists " % ( index, urls[index] ) )
            del urls[index]

        # print( "[HentaiManager]urls", urls )
        return urls
        
    def parse( self, url ):
        """parse e-hentai's gallery page, and get target images.
    
        Args:
            url: hentai gallery url

        Returns:
            HentaiGallery obj
    
        Raises:
        """
    
        gallery = HentaiGallery( self.session, url )
        gallery.open( )

        return ( gallery.get_name( ), gallery.get_all_image( ) )

    
    def download( self, url, save_folder ):
        """download
    
        Args: 
            url: #TODO
            save_folder: #TODO

        Returns:
    
        Raises:
        """
    
        print( "parse url", url )
        ( task_name, task_urls ) = self.parse( url )

        save_folder = os.path.join( save_folder, task_name )

        task_urls = self._check_finished( save_folder, task_urls )

        self._start_download( task_urls, save_folder )
    
    def _start_download( self, page_list, save_folder ):
        # open data file.
        conf_file_name = os.path.join( save_folder, DATA_FILE_NAME )
        # file_obj = open( conf_file_name, "w" )

        task_status_tab = {}

        for page_url in page_list:
            task_status_tab[page_url] = str( False )

        is_all_finish = True
        for page_url in page_list:
            try:
                print( "[HentaiManager]start download page %s..." % page_url )
                page = HentaiPage( self.session, page_url )
                page.open( )
                page.save( save_folder )
                print( "[HentaiManager]download page %s succeed." % page_url )

                task_status_tab[page_url] = str( True )

                # file_obj.seek( 0 )
                # file_obj.truncate( )

                with open( conf_file_name, "w" ) as file_obj:
                    json.dump( task_status_tab, file_obj, indent=4 )

                time.sleep( self.sleep_time )
            except requests.exceptions.Timeout as e:
                task_status_tab[page_url] = str( False )

                with open( conf_file_name, "w" ) as file_obj:
                    json.dump( task_status_tab, file_obj, indent=4 )

                is_all_finish = False
                print( "[HentaiManager]download page %s failed!" % page_url )

        if is_all_finish:
            if os.path.isfile( conf_file_name ):
                os.remove( conf_file_name )


if __name__ == "__main__":
    import sys
    if len( sys.argv ) < 2:
        # test_url = "http://g.e-hentai.org/g/849492/eda7c42b07/" 
        test_url = "http://g.e-hentai.org/g/852086/a23483a313/" 
    else:
        test_url = sys.argv[1]

    if len( sys.argv ) < 3:
        save_folder = "download"
    else:
        save_folder = sys.argv[2]

    manager = HentaiDownloadManager()

    manager.download( test_url, save_folder )
