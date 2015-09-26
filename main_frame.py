import os
import sys
import pickle

from tkinter import *
import tkinter
import tkinter.ttk as ttk

from options_frame import OptionsFrame
from manager import HentaiDownloadManager

cfg_file = ".frame.config"

class MainFrame( Frame ):
    """
    MainFrame's description.
    """

    def __init__( self, master = None ):
        Frame.__init__( self, master )

        self.value_of_combo = "X"

        self.grid( )
        self.create_widgets( )

        self.download_manager = HentaiDownloadManager()
        # self.update( )

        self.download_manager.task_update_callback = self.download_update_callback
        self.download_manager.task_finish_callback = self.download_finish_callback

        self.update_ui( )
        self.load_config( )

    def load_config( self ):
        try:
            with open( cfg_file, "rb" ) as f:
                self.addr_var.set( pickle.load( f ) )
                # self.gallery_name_var.set( pickle.load( f ) )
                self.save_folder_var.set( pickle.load( f ) )
        except:
            if not os.path.isfile( cfg_file ):
                print( "File(%s) is not exits" % cfg_file )
                return False

            print( "User info file(%s) is broken!" % cfg_file )
            os.remove( cfg_file )
    def save_config( self ):
        with open( cfg_file, "wb" ) as f:
            pickle.dump( self.addr_var.get( ), f )
            # pickle.dump( self.gallery_name_var.get( ), f )
            pickle.dump( self.save_folder_var.get( ), f )
    
    def open_options( self ):
        # wdw = Toplevel()
        # wdw.geometry('+400+400')
        # e = Entry(wdw)
        # e.pack()
        # e.focus_set()
        # wdw.transient(self)
        # wdw.grab_set()
        # self.wait_window(wdw)

        options_frame = OptionsFrame( self )
        options_frame.transient(self)
        options_frame.grab_set()
        options_frame.set_callback( self.login_callback, self.logout_callback )

        user_name = self.download_manager.get_user_name()
        if user_name:
            options_frame.update_ui( {"user_name" : user_name} )
        else:
            options_frame.update_ui( {} )

        self.wait_window( options_frame )

    def create_widgets( self ):

        # gallery info group
        self.group = LabelFrame(self, text="相册信息", padx=5, pady=5)
        self.group.grid(padx=10, pady=10, sticky=W+E+N+S, columnspan=4)

        l = Label( self.group, text="相册地址" )
        l.grid( row=0, column=0 )

        self.addr_var = StringVar()
        self.addr = Entry( self.group, textvariable = self.addr_var )
        self.addr.grid( row=0, column=1, columnspan=3, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="相册名称" )
        l.grid( row=1, column=0 )

        self.gallery_name_var = StringVar()
        self.gallery_name = Entry( self.group, textvariable=self.gallery_name_var )
        self.gallery_name.grid( row=1, column=1, columnspan=3, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="保存地址" )
        l.grid( row=2, column=0 )

        self.save_folder_var = StringVar()
        self.save_folder = Entry( self.group, textvariable=self.save_folder_var )
        self.save_folder.grid( row=2, column=1, columnspan=2, sticky=W+E+N+S, padx=5, pady=3 )

        self.btn_open_dir = Button( self.group, text="打开目录", padx=10, command = self.open_dir )
        self.btn_open_dir.grid( row=2, column=3, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="图片数量" )
        l.grid( row=3, column=0 )

        self.pic_num_var = StringVar()
        self.pic_num = Entry( self.group, width=3, state = "disabled", textvariable=self.pic_num_var )
        self.pic_num.grid( row=3, column=1, sticky=W, padx=5 )

        self.parse_gallery = Button( self.group, text="分析相册", padx=10, command = self.start_parse )
        self.parse_gallery.grid( row=3, column=2, sticky=W+E+N+S, padx=5, pady=3 )

        self.addr_var.trace( "w", lambda name, index, mode: self.parse_gallery.config( state="normal" ) )

        self.btn_download = Button( self.group, text="开始下载", padx=10, command = self.start_download )
        self.btn_download.grid( row=3, column=3, sticky=W+E+N+S, padx=5, pady=3 )

        #self.btn_menu = Button( self, text="选项", command = lambda: self.pic_num_var.set( 1 ))
        self.btn_menu = Button( self, text="选项", command = self.open_options )
        self.btn_menu.grid( row=1, column=0 )

        l = Label( self, text="当前图片" )
        l.grid( row=1, column=1 )

        self.prg_download = ttk.Progressbar(self, orient='horizontal', mode='determinate')
        self.prg_download.grid( row=1, column=2 )
        # self.prg_download.step( 25 *2 )

        # self.lab_download = Label( self, text="尚未开始下载" )
        # self.lab_download.grid( row=1, column=3 )

    def update( self, elapse = 500 ):
        print( "update!" )
        self.after( elapse, self.update )

    def update_ui( self ):
        if not self.download_manager.is_login( ):
            self.open_options( )
            return

        # print( "update_ui", self.download_manager.task_name )
        if self.download_manager.task_name:
            self.gallery_name_var.set( self.download_manager.task_name )
            self.btn_download.config( state="normal" )
            self.parse_gallery.config( state="disabled" )

            ( cur, total ) = self.download_manager.get_progress( )
            # print( "============total", total, self.download_manager.task_status_tab )
            self.pic_num_var.set( len(self.download_manager.task_urls) )
            if total > 0:
                self.prg_download["value"] = cur
                self.prg_download["maximum"] = total
            else:
                self.prg_download["value"] = 0
        else:
            self.gallery_name_var.set( "" )
            self.btn_download.config( state="disabled" )
            self.parse_gallery.config( state="normal" )
            self.pic_num_var.set( "" )
            self.prg_download["value"] = 0

    def start_parse( self ):
        self.download_manager.parse( self.addr_var.get( ) )
        self.update_ui( )

    def start_download( self ):
        self.btn_download.config( state="disabled" )
        save_folder = os.path.join( self.save_folder_var.get( ), self.gallery_name_var.get( ) )
        self.download_manager.download( save_folder )
        self.save_config( )

    def open_dir( self ):
        import platform
        if os.path.isdir( self.save_folder_var.get() ):
            if platform.system( ) == "Windows":
                import subprocess
                subprocess.Popen( r'explorer /select,"%s"' % self.save_folder_var.get() )
    

    def login_callback( self, user_name, password ):
        return self.download_manager.login( user_name, password )
        # if self.user_session.get_cookies_from_internet( user_name, password ):
        #     pass
        # else:
        #     pass
        # print( "login", user_name, password )

    def logout_callback( self ):
        self.download_manager.logout( )

    def download_update_callback( self, cur, total ):
        self.prg_download["value"] = cur
        self.prg_download["maximum"] = total


    def download_finish_callback( self ):
        self.btn_download.config( state="normal" )
        tkinter.messagebox.showinfo( "通知", "下载完成！" )
    

if __name__ == "__main__":
    import logging
    # 创建一个logger  
    logger = logging.getLogger()  
    logger.setLevel(logging.DEBUG)  
      
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler('log.txt', "w", "utf-8")  
    fh.setLevel(logging.DEBUG)  

    # 创建一个stream
    ch = logging.StreamHandler( sys.stdout )
    ch.setLevel(logging.DEBUG)
      
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
      
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)
      
    import logger_stdout_handler
    # 将stdout的输入重定向到StreamToLogger对象上
    sys.stdout = logger_stdout_handler.LoggerStdOutHandler( logger, logging.DEBUG )

    app = MainFrame()
    app.mainloop()
