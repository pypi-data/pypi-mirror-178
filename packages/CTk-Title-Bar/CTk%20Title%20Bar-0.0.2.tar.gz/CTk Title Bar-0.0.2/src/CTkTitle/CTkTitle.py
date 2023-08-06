import ctypes
import os
from tkinter import Label, Frame, font
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk


class CTkTitlebar:
    """
           This class developed to create customize title bar for window(Tkinter)

    """

    def __init__(self):
        self.CTkwindow = None

    def __CTkstartMove(self, event):
        global x, y
        x = event.x
        y = event.y

    def __CTkstopMove(self, event):
        global x, y
        x = None
        y = None

    def __CTkmoving(self, event):
        global x, y
        try:
            x_ = (event.x_root - x)
            y_ = (event.y_root - y)
        except:
            x_ = 0
            y_ = 0

        self.CTkwindow.geometry("+%s+%s" % (x_, y_))

    def __CTkminimize(self, event):
        self.CTkwindow.attributes("-alpha", 0)
        self.CTkwindow.minimized = True

    def CTkReposition(self, event, sx=0, sy=0):
        """
        Doubleclick on Titlebar repositon window to screen top (sx :0,sy :0)

        :param sx: Screen x position (:int)
        :param sy: Screen y position (:int)
        """
        self.CTkwindow.geometry(
            '%sx%s+%s+%s' % (self.CTkwindow.winfo_width(), self.CTkwindow.winfo_height(), sx, sy))
        self.CTkwindow.update_idletasks()

    def __CTkhoverMin(self, event):
        event.widget.config(bg="grey25")

    def __CTkunHoverMin(self, event, bg_color):
        self.min_b.config(bg=bg_color)

    def __CTkhoverexit(self, event):
        event.widget.config(bg="red")

    def __CTkunHoverexit(self, event, bg_color):
        self.exit_b.config(bg=bg_color)

    def __CTkexit_bu(self, event):
        self.CTkwindow.destroy()

    def __CTkdeminimize(self, event):
        self.CTkwindow.attributes("-alpha", 1)
        if self.CTkwindow.minimized:
            self.CTkwindow.minimized = False

    def __set_appwindow(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080

        hwnd = ctypes.windll.user32.GetParent(self.CTkwindow.winfo_id())
        ctkwstyle = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctkwstyle = ctkwstyle & ~WS_EX_TOOLWINDOW
        ctkwstyle = ctkwstyle | WS_EX_APPWINDOW
        res = ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ctkwstyle)

        self.CTkwindow.wm_withdraw()
        self.CTkwindow.after(1, lambda: self.CTkwindow.wm_deiconify())

    def Header(self, master, title='CTItleBar', title_font='none 12', title_fg='#200E32', icon_path=None, bg_color='grey',tools_fg='#200E32'):
        """
        The Header method developed to create Customized Titlebar for Master window(Tkinter) with minimize & close option.

        :param master: Tk window : object
        :param title: Title : Str
        :param title_font: font style for title string : str ,ex 'verdana 12 bold' , font.Font(family='verdana',size=12)
        :param title_fg: foreground color for title : str
        :param icon_path: Icon absolute/Relative path : str, .Png format required
        :param bg_color: Header background color : str
        :param tools_fg: Minimize & close button foreground color
        :return: Customized Header Bar
        """
        self.CTkwindow = master
        if self.CTkwindow is not None:
            self.CTkwindow.title(title)
            self.CTkwindow.overrideredirect(1)
            self.CTkwindow.minimized = False
            self.CTkwindow.maximized = False
            self.CTkwindow.bind("<FocusIn>", self.__CTkdeminimize)
            self.CTkwindow.after(0, lambda: self.__set_appwindow())

            # Header Start:
            self.hy = 2
            header_height = 35
            self.CTkwindow.update()
            self.CTkh = Frame(self.CTkwindow, width=self.CTkwindow.winfo_width(), height=header_height, bg=bg_color,
                              )
            self.CTkh.place(x=0, y=0)
            if icon_path is not None:
                pass
                if os.path.exists(icon_path):
                    if icon_path.endswith('.png'):
                        # self.CTkwindow.iconbitmap(icon_path)
                        # Logo
                        CTkh_logo = Image.open(icon_path)
                        CTkh_photo = ImageTk.PhotoImage(CTkh_logo.resize((20, 21), Image.Resampling.LANCZOS))
                        CTkh_logo_lbl = Label(self.CTkh, image=CTkh_photo, background='dark sea green', pady=5, padx=5)
                        CTkh_logo_lbl.hippo_photo = CTkh_photo
                        CTkh_logo_lbl.place(x=10, y=5)
                        CTkh_logo_lbl.bind('<Enter>', lambda x: CTkh_logo_lbl.config(background='dark sea green3'))
                        CTkh_logo_lbl.bind('<Leave>', lambda x: CTkh_logo_lbl.config(background='dark sea green'))
                        # self.hippo_l1.bind('<Button-1>',)

                        Hovertip(CTkh_logo_lbl, title)
            # Title:
            CTkh_logo_lbl = Label(self.CTkh, text=title, foreground=title_fg, background=bg_color, font=title_font,
                                  pady=5, padx=5)
            CTkh_logo_lbl.place(x=40, y=3)

            # Tools
            self.min_b = Label(self.CTkwindow, text="_", bg=bg_color, font="none 13 ", fg=tools_fg, relief="flat",
                               pady=13, padx=10)
            self.min_b.place(x=self.CTkwindow.winfo_width() - 80, y=int(header_height / 2 - 13 / 2) - 25)  # 445
            self.min_b.bind("<Button-1>", self.__CTkminimize)
            self.min_b.bind("<Enter>", self.__CTkhoverMin)
            self.min_b.bind("<Leave>", lambda event=True: self.__CTkunHoverMin(event=True, bg_color=bg_color))
            # Hovertip(self.min_b, 'Minimize')

            self.exit_b = Label(self.CTkwindow, text="X", bg=bg_color, font="none 13 ", fg=tools_fg, padx=15,
                                pady=6,
                                relief="flat")
            self.exit_b.place(x=self.CTkwindow.winfo_width() - 45, y=int(header_height / 2 - 13 / 2) - 11)
            self.exit_b.bind("<Button-1>", self.__CTkexit_bu)
            self.exit_b.bind("<Enter>", self.__CTkhoverexit)
            self.exit_b.bind("<Leave>", lambda event=True: self.__CTkunHoverexit(event=True, bg_color=bg_color))
            # Hovertip(self.exit_b, 'Close')

            # line = Frame(self.window, height=0.1, width=self.width, bg="grey72").place(x=0, y=35)

            self.CTkwindow.bind("<Button-1>", self.__CTkstartMove)
            self.CTkwindow.bind("<ButtonRelease-1>", self.__CTkstopMove)
            self.CTkwindow.bind("<B1-Motion>", self.__CTkmoving)
            self.CTkwindow.bind('<Double-Button-1>', self.CTkReposition)
