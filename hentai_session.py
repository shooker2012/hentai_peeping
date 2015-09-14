import requests
import pickle
import lxml.html
import re
import os, sys
import time

import logger_stdout_handler

from gallery import HentaiGallery
from page import HentaiPage

login_url = 'http://forums.e-hentai.org/index.php?act=Login&CODE=01'
home_url = 'http://g.e-hentai.org/home.php'

user_info_file = ".user.info"

e_hentai_domain = ".e-hentai.org"
ex_hentai_domain = ".exhentai.org"

import random
def genheader(custom = '', referer = ''):
    rrange = lambda a, b, c = 1: str(c == 1 and random.randrange(a, b) or float(random.randrange(a * c, b * c)) / c)
    ua = 'Mozilla/' + rrange(4, 7, 10) + '.0 (Windows NT ' + rrange(5, 7) + '.' + rrange(0, 3) + ') AppleWebKit/' + rrange(535, 538, 10) + \
    ' (KHTML, like Gecko) Chrome/' + rrange(21, 27, 10) + '.' + rrange(0, 9999, 10) + ' Safari/' + rrange(535, 538, 10)
    ip = '%s.%s.%s.%s' % (rrange(0, 255), rrange(0, 255), rrange(0, 255), rrange(0, 255))
    headers = {'User-Agent':ua, 'Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Charset':'utf-8;q=0.7,*;q=0.7', \
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\
               , 'Connection': 'keep-alive'}  # ,'X-Forward-For':ip,'Client_IP':ip}
    # headers['Cookie']='nw=1;'
    # if cooid and coopw:
    #     headers['Cookie'] += 'ipb_member_id=' + cooid + ';ipb_pass_hash=' + coopw + ';'\
    #     # +'uconfig=tl_m-uh_y-sa_y-oi_n-qb_n-tf_n-hp_-hk_-rc_0-cats_0-xns_0-xl_-ts_m-tr_1-prn_y-dm_l-rx_0-ry_0'
    #     if IS_REDIRECT:
    #         headers['Referer'] = referer or _redirect
    #         headers['Cookie'] += 'c[e-hentai.org][/][ipb_member_id]=' + cooid + \
    #         ';c[e-hentai.org][/][ipb_pass_hash]=' + coopw + ';c[exhentai.org][/][ipb_member_id]=' + cooid + \
    #         ';c[exhentai.org][/][ipb_pass_hash]=' + coopw + ';s=' + cooproxy + ';c[exhentai.org][/][nw]=1'
    # if coofetcher:headers['Cookie']+=coofetcher
    if 'form' in custom:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return headers


class HentaiSession(requests.Session):
    """
    A session for visit e-hentai/exhentai.It can login your account, keep cookies and save it to local file.

    Attributes:
        user_name: string type.what your session use for login.
        is_login: bool type.If session is always login with cookies.
    """

    def __init__( self ):
        super().__init__()
        self.is_login = False
        self.user_name = ""

        self.headers.update( genheader() )

    def load_from_file( self ):
        try:
            with open( user_info_file, "rb" ) as f:
                self.user_name = pickle.load( f )
                self.cookies = pickle.load( f )
                self.is_login = True
                print( "Load cookies form file!" )
                print( "cookies", self.cookies )
                # print( "cookie", self.cookies["ipb_member_id"], self.cookies["ipb_pass_hash"] )
                return True
        except:
            if not os.path.isfile( user_info_file ):
                print( "File(%s) is not exits" % user_info_file )
                return False

            print( "User info file(%s) is broken!" % user_info_file )
            os.remove( user_info_file )
            return False

    def save_to_file( self ):
        if not self.is_login:
            print( "Can't save user info.No user login!" )
            return

        with open( user_info_file, "wb" ) as f:
            pickle.dump( self.user_name, f )
            pickle.dump( self.cookies, f )

    def get_cookies_from_internet( self, user_name, password ):
        try:
            logindata = {
                'UserName':user_name,
                'returntype':'8',
                'CookieDate':'1',
                'b':'d',
                'bt':'pone',
                'PassWord':password,
                }

            post_obj = self.post( login_url, data = logindata )
            print( "post_obj", post_obj.text )
            print( "cookie", post_obj.cookies )
            print( "cookie", post_obj.cookies["ipb_member_id"], post_obj.cookies["ipb_pass_hash"] )

            if post_obj.cookies["ipb_member_id"] and post_obj.cookies["ipb_pass_hash"]:
                self.cookies = post_obj.cookies
                self.user_name = user_name
                self.is_login = True

                # copyt e-hentai's cookies to exhentai
                for k,v in self.cookies.get_dict( e_hentai_domain ).items():
                    self.cookies.set( k, v, domain=ex_hentai_domain )

                self.save_to_file( )
                return

            print( "User(%s) login succeeed!" % user_name )
        except Exception as e:
            print( "User(%s) login failed!" % user_name )
            print( e )

    def get_user_info( self ):
        if not self.is_login:
            print( "No user login!Please login first" )
            return

        reg_cost = re.compile( r"You are currently at (\d+) towards a limit of (\d+)." )

        get_obj = self.get( home_url )
        print( "\n\nuser_info:", get_obj.text )
        doc = lxml.html.document_fromstring( get_obj.text )
        homebox = []
        for node in doc.find_class( "homebox" ):
            # print( "home box node text:", node.text_content() )
            content = node.text_content()
            homebox.append( content )

            reg_obj = reg_cost.search( content )
            if reg_obj:
                print( "Find the cost" )
                print( reg_obj.group( 1 ), reg_obj.group( 2 ) )

def down_pages( session, page_list, gallery_name, save_folder ):
    gallery_name = os.path.join( save_folder, gallery_name )
    print( "Save gallery:", gallery_name )

    for i, page_url in enumerate( page_list ):
        if i < 55:
            continue

        print( "start download page %s..." % page_url )
        page = HentaiPage( session, page_url )
        page.open( )
        page.save( gallery_name )
        print( "download page %s succeed." % page_url )
        time.sleep( 0.5 )

if __name__ == "__main__":
    import logging
    # 创建一个logger  
    logger = logging.getLogger()  
    logger.setLevel(logging.DEBUG)  
      
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler('log.txt', "w")  
    fh.setLevel(logging.DEBUG)  

    # 创建一个stream
    ch = logging.StreamHandler( sys.stdout )
    ch.setLevel(logging.INFO)
      
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
      
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)
      
    # 将stdout的输入重定向到StreamToLogger对象上
    sys.stdout = logger_stdout_handler.LoggerStdOutHandler( logger, logging.DEBUG )

    test_user_name = "all4hentai"
    print( "User ID:"+test_user_name )

    # session = requests.Session( )

    user_session = HentaiSession( )
    if not user_session.load_from_file( ):
        import getpass
        password = getpass.getpass( "Please input your password:" )

        user_session.get_cookies_from_internet( test_user_name, password )

    user_session.get_user_info( )
    time.sleep( 0.5 )

    # open gallery
    gallery = HentaiGallery( user_session, "http://g.e-hentai.org/g/849492/eda7c42b07/" )
    gallery.open( )
    print( "titles", gallery.title_gj, gallery.title_gn )

    down_pages( user_session, gallery.get_all_image(), gallery.get_name(), "download" )


    os.stdout = None

    # print( "titles", gallery.title_gj, gallery.title_gn, help( gallery.title_gj ) )
    # print( "titles", gallery.title_gj.items(), gallery.title_gj.text, gallery.title_gj.tag )
    # print( "titles", gallery.title_gj.attrib, gallery.title_gj.label )

