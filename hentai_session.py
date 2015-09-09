import requests
import pickle
import lxml.html
import re
import os

login_url = 'http://forums.e-hentai.org/index.php?act=Login&CODE=01'
home_url = 'http://g.e-hentai.org/home.php'

user_info_file = ".user.info"

class HentaiSession(requests.Session):
    def __init__( self ):
        super().__init__()
        self.is_login = False
        self.user_name = ""

    def load_from_file( self ):
        with open( user_info_file, "rb" ) as f:
            try:
                self.user_name = pickle.load( f )
                self.cookies = pickle.load( f )
                self.is_login = True
                print( "Load cookies form file!" )
            except:
                print( "User info file(%s) is broken!" % user_info_file )
                os.remove( user_info_file )

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

if __name__ == "__main__":
    user_name = "all4hentai"
    password = "powerful"

    # session = requests.Session( )

    user = HentaiSession( )
    user.load_from_file( )
    # user.get_cookies_from_internet( user_name, password )

    user.get_user_info( )

