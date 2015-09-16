from tkinter import *
import tkinter.ttk as ttk

class MainFrame( Frame ):
    """
    MainFrame's description.
    """

    def __init__( self, master = None ):
        Frame.__init__( self, master )

        self.value_of_combo = "X"

        self.grid( )
        self.create_widgets( )

    def create_widgets( self ):

        # gallery info group
        self.group = LabelFrame(self, text="相册信息", padx=5, pady=5)
        self.group.grid(padx=10, pady=10, sticky=W+E+N+S, columnspan=4)

        l = Label( self.group, text="相册地址" )
        l.grid( row=0, column=0 )

        self.addr = Entry( self.group )
        self.addr.grid( row=0, column=1, columnspan=3, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="相册名称" )
        l.grid( row=1, column=0 )

        self.gallery_name = Entry( self.group )
        self.gallery_name.grid( row=1, column=1, columnspan=3, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="保存地址" )
        l.grid( row=2, column=0 )

        self.save_folder = Entry( self.group )
        self.save_folder.grid( row=2, column=1, columnspan=2, sticky=W+E+N+S, padx=5, pady=3 )

        l = Label( self.group, text="图片数量" )
        l.grid( row=3, column=0 )

        self.pic_num = Entry( self.group, width=3 )
        self.pic_num.grid( row=3, column=1, sticky=W, padx=5 )

        self.parse_gallery = Button( self.group, text="分析相册", padx=10 )
        self.parse_gallery.grid( row=3, column=2, sticky=W+E+N+S, padx=5, pady=3 )

        self.btn_download = Button( self.group, text="开始下载", padx=10 )
        self.btn_download.grid( row=3, column=3, sticky=W+E+N+S, padx=5, pady=3 )

        self.btn_menu = Button( self, text="选项", command=self.option)
        self.btn_menu.grid( row=1, column=0 )

        l = Label( self, text="当前图片" )
        l.grid( row=1, column=1 )

        self.prg_download = ttk.Progressbar(self, orient='horizontal', mode='determinate')
        self.prg_download.grid( row=1, column=2 )
        self.prg_download.step( 25 *2 )

        self.lab_download = Label( self, text="尚未开始下载" )
        self.lab_download.grid( row=1, column=3 )

    def option( self ):
        self.prg_download.step( -25 )
    


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
