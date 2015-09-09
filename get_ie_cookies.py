# from string import lower, find
import sys
import re, os, glob
import win32api, win32con

def _parseIECookieFile( file_name ):
    # IE cookies File Format:
    #     Cookie name
    #     Cookie value
    #     Host/path for the web server setting the cookie
    #     Flags
    #     Exirpation time (low)
    #     Expiration time (high)
    #     Creation time (low)
    #     Creation time (high)
    #     Record delimiter (*)

    # Conversion of the time to the number of seconds elapsed since midnight (00:00:00), January 1, 1970,
    # t = 1e-7*(high*pow(2,32)+low) - 11644473600
    ie_cookie = re.compile('(?P<name>.*)\n(?P<value>.*)\n(?P<host>.*)\n(?P<flags>.*)\n(?P<e_time_low>.*)\n(?P<e_time_high>.*)\n(?P<c_time_low>.*)\n(?P<c_time_high>.*)\n(?P<delimiter>.*)\n' )

    with open( file_name, "r" ) as file_obj:
        current_index = 0
        cookies = []
        file_str = file_obj.read()
        while True:
            # print( "substring:", file_str[current_index:] )
            search_obj = ie_cookie.search( file_str, current_index )
            if search_obj:
                cookie = {}
                cookie['name'] = search_obj.group( 'name' )
                cookie['value'] = search_obj.group( 'value' )
                cookie['host'] = search_obj.group( 'host' )
                cookie['file_name'] = file_name

                cookies.append( cookie )

                current_index = search_obj.span()[1]
                # print( "== find cookie", cookie, current_index )
            else:
                return cookies

def _getLocation():
    ''' Looks through the registry to find the current users Cookie folder. This is the folder IE uses. '''
    key = 'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    regkey = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, key, 0, win32con.KEY_ALL_ACCESS)
    num = win32api.RegQueryInfoKey(regkey)[1]
    for x in range(0, num):
        k = win32api.RegEnumValue(regkey, x)
        if k[0] == 'Cookies':
            return k[1]

def _getCookieFiles(location, name):
    ''' Rummages through all the files in the cookie folder, and returns only the ones whose file name, contains name. 
    Name can be the domain, for example 'activestate' will return all cookies for activestate. 
    Unfortunately it will also return cookies for domains like activestate.foo.com, but thats highly unlikely. '''
    filenm = os.path.join(location, '*%s*' % name)
    files = glob.glob(filenm)
    # print( "_getCookieFiles", filenm, files )
    return files

def _loadCookies( files ):
    ''' Look through a group of files looking for a specific cookie,
    when we find it return, which means the first one found '''
    cookies = []
    for file in files:
        cookie = _parseIECookieFile( file )
        if cookie:
            cookies.extend( cookie )
        else:
            print( "# Error! Parse file(%s) failed!" % file )

    # print( "cookies: ", cookies )
    return cookies

class IECookies:
    def __init__( self ):
        self.open( )

    def open( self ):
        self.cookies = []

        try:
            cookies_folder = _getLocation( )
        except:
            # just print a debug
            print( "Error pulling registry key" )
            return

        cookies_files = _getCookieFiles( cookies_folder, "." )
        if cookies_files: 
            self.cookies = _loadCookies( cookies_files )
        else: 
            print( "No cookies for that domain found" )
            return

    def findCookies( self, name="", host="" ):
        re_name, re_host = None, None

        if name != "":
            re_name = re.compile( name )
        if host != "":
            re_host = re.compile( host )

        result = []
        for cookie in self.cookies:
            if re_name and not re_name.search( cookie['name'] ):
                # print( "re_name not pairs", name, cookie['name'] )
                continue

            if re_host and not re_host.search( cookie['host'] ):
                # print( "re_host not pairs", host, cookie['host'] )
                continue

            result.append( cookie )

        return result

if __name__=='__main__':
    # print( findIECookie(domain='kuro5hin', cookie='k5-new_session') )
    # print( findIECookie(domain='.*', cookie='.*') )

    f_handler=open('out.log', 'w')
    sys.stdout=f_handler

    ie_cookies = IECookies( )
    cookies = ie_cookies.findCookies( host="hentai" )
    for cookie in cookies:
        print( "cookie name(%s), value(%s)" %( cookie['name'], cookie['value'] ) )
