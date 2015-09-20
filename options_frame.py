from tkinter import *
import tkinter.messagebox

class OptionsFrame( Toplevel ):
    """
    OptionsFrame's description.
    """

    def __init__( self, master = None ):
        Toplevel.__init__( self, master )

        # self.overrideredirect( True )

        self.grid( )
        self.create_widgets( )

        # self.update( )

        # center the window.
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        if master:
            x = master.winfo_rootx() + (master.winfo_width() // 2) - (width // 2)
            y = master.winfo_rooty() + (master.winfo_height() // 2) - (height // 2)
            print( "master!", master.winfo_x(), master.winfo_y() )
        else:
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.resizable( 0, 0 )
        # print( "help", help( self ) )

    def set_callback( self, login_callback, logout_callback ):
        self.login_callback = login_callback
        self.logout_callback = logout_callback
    

    def update( self, elapse = 500 ):
        print( "update!" )
        self.after( elapse, self.update )

    # def onFormEvent( self, event ):
    #     for key in dir( event ):
    #         if not key.startswith( '_' ):
    #             print( '%s=%s' % ( key, getattr( event, key ) ) )

    #     print( event )
    #     print( "\n" )

    def create_widgets( self ):
        l = Label( self, text="用户名：" )
        l.grid( row=0, column=0 )

        self.user_name_var = StringVar()
        self.entry_user_name = Entry( self, textvariable=self.user_name_var )
        self.entry_user_name.grid( row=0, column=1 )

        l = Label( self, text="密码：" )
        l.grid( row=1, column=0 )

        self.password_var = StringVar()
        self.entry_password = Entry( self, show="*", textvariable=self.password_var )
        self.entry_password.grid( row=1, column=1 )

        self.button_login = Button( self, text="登录", width = 8, command=self.login )
        self.button_login.grid( row=0, column=2, padx=5, pady=3 )
        self.button_logout = Button( self, text="退出", command=self.logout )
        # self.button_logout.grid( row=0, column=2, padx=5, pady=3 )

        l = Label( self, text="限额" )
        l.grid( row=2, column=0 )

        self.limits_var = StringVar()
        self.entry_limits = Entry( self, state = "disabled", textvariable=self.limits_var )
        self.entry_limits.grid( row=2, column=1 )

        self.button_get_limits = Button( self, text="刷新限额", width = 8, command=self.get_limits )
        self.button_get_limits.grid( row=1, column=2, padx=5, pady=3 )

    def login( self ):
        if not self.user_name_var.get() or not self.password_var.get():
            tkinter.messagebox.showinfo( "通知", "请输入用户名/密码!" )
            return

        if hasattr( self, 'login_callback' ):
            if self.login_callback( self.user_name_var.get(), self.password_var.get() ):
                tkinter.messagebox.showinfo( "通知", "登录成功!" )
                self.update_ui( { "user_name" : self.user_name_var.get() } )
            else:
                tkinter.messagebox.showinfo( "通知", "登录失败!" )

    def logout( self ):
        if hasattr( self, 'logout_callback' ):
            self.logout_callback( )
            tkinter.messagebox.showinfo( "通知", "退出登录成功！" )
            self.update_ui( {} )
    
    def get_limits( self ):
        pass

    def update_ui( self, data ):
        # 己登录
        if "user_name" in data:
            self.user_name_var.set( data["user_name"] )
            self.entry_user_name.config( state = "disabled" )
            self.password_var.set( "123456" )
            self.entry_password.config( state = "disabled" )

            self.button_logout.grid( row=0, column=2, padx=5, pady=3 )
            self.button_login.grid_forget()
        # 未登录
        else:
            # self.user_name_var.set( "" )
            self.entry_user_name.config( state = "normal" )

            self.password_var.set( "" )
            self.entry_password.config( state = "normal" )

            self.button_login.grid( row=0, column=2, padx=5, pady=3 )
            self.button_logout.grid_forget()
    
    
    
if __name__ == "__main__":
    app = OptionsFrame()
    app.update_ui( {} )
    app.mainloop()
