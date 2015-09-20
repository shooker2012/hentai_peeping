import time
import os
import requests
import json

from hentai_session import HentaiSession
from gallery import HentaiGallery
from page import HentaiPage

# import thread
import threading

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

        self.IsWorking = False
        self.sleep_time = 0.3

        self.task_name = None
        self.task_status_tab = {}

        self.task_update_callback = None
        self.task_finish_callback = None

    def _check_finished( self, save_folder, urls ):
        """check if which images are always downloaded, and remove them from download list.
    
        Args: None

        Returns:
    
        Raises:
        """

        urls = urls[:]
    
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

    def is_login( self ):
        return self.session.is_login

    def login( self, user_name, password ):
        return self.session.get_cookies_from_internet( user_name, password )

    def logout( self ):
        self.session.cookies.clear( )
        self.session.clean_file( )

    def get_user_name( self ):
        return self.session.user_name

    def get_user_info( self ):
        return self.session.get_user_info( )
        
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

        self.task_name = gallery.get_name( )
        self.task_urls = gallery.get_all_image( )

        print( "111", self.task_name, self.task_urls )

        # return ( gallery.get_name( ), gallery.get_all_image( ) )

    
    def download( self, save_folder ):
        """download
    
        Args: 
            url: #TODO
            save_folder: #TODO

        Returns:
    
        Raises:
        """

        if not self.task_name:
            print( "No task to download. Please parse url first!" )
            return

        if self.IsWorking == True:
            return False

        self.IsWorking = True

        self.thread_lock = threading.Lock()
    
        # save_folder = os.path.join( save_folder, self.task_name )

        task_urls = self._check_finished( save_folder, self.task_urls )

        self.task_status_tab = {}
        for page_url in self.task_urls:
            if page_url in task_urls:
                self.task_status_tab[page_url] = str( False )
            else:
                self.task_status_tab[page_url] = str( True )

        # open data file.
        self.conf_file_name = os.path.join( save_folder, DATA_FILE_NAME )

        # self._start_download( task_urls, save_folder )

        self._download_thread_table = []

        thr = threading.Thread( target=self._download_thread, args=(self.session, task_urls, save_folder, self._download_task_update_callback, self._download_task_finished_callback, self.sleep_time) )
        thr.start( )
        self._download_thread_table.append( thr )


    def _download_thread( self, session, page_list, save_folder, update_callback, finish_callback, sleep_time ):
        for page_url in page_list:
            try:
                print( "[HentaiManager]start download page %s..." % page_url )
                page = HentaiPage( session, page_url )
                page.open( )

                # Enter critical section
                self.thread_lock.acquire( )

                page.save( save_folder )
                print( "[HentaiManager]download page %s succeed." % page_url )

                update_callback( page_url, True )

                self.thread_lock.release( )
                # Leave critical section

                time.sleep( sleep_time )
            except requests.exceptions.Timeout as e:
                update_callback( page_url, False )
                print( "[HentaiManager]download page %s failed!" % page_url )


        # Enter critical section
        self.thread_lock.acquire( )

        finish_callback( )

        self.thread_lock.release( )
        # Leave critical section


    def _download_task_update_callback( self, url, is_succeed ):
        if is_succeed:
            self.task_status_tab[url] = str( True )
        else:
            self.task_status_tab[url] = str( False )

        with open( self.conf_file_name, "w" ) as file_obj:
            json.dump( self.task_status_tab, file_obj, indent=4 )

        if self.task_update_callback:
            ( cur, total ) = self.get_progress( )
            self.task_update_callback( cur, total )

    def _download_task_finished_callback( self ):
        thr = threading.currentThread()
        if thr in self._download_thread_table:
            print( "task(%s) is finish" % thr.getName() )
            self._download_thread_table.remove( thr )

        if len( self._download_thread_table ) == 0:
            print( "all task is finish!" )

            if "False" not in self.task_status_tab.values():
                # open data file.
                if os.path.isfile( self.conf_file_name ):
                    os.remove( self.conf_file_name )

        if self.task_finish_callback:
            self.task_finish_callback( )

    def get_progress( self ):
        """get_progress
    
        Args: None

        Returns:
    
        Raises:
        """

        return ( len( [ v for v in self.task_status_tab.values() if v == "True"  ] ), len( self.task_status_tab ) )



if __name__ == "__main__":
    import sys
    if len( sys.argv ) < 2:
        # test_url = "http://g.e-hentai.org/g/852086/a23483a313/" 
        test_url = "http://exhentai.org/g/852726/3e25b3069b/" 
    else:
        test_url = sys.argv[1]

    if len( sys.argv ) < 3:
        save_folder = "download1"
    else:
        save_folder = sys.argv[2]

    manager = HentaiDownloadManager()

    manager.parse( test_url )
    manager.download( save_folder )
