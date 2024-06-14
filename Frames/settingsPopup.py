import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image, ImageDraw
from collections import OrderedDict
from weakref import proxy
from functools import lru_cache
import time

from utils import fonts, Configuration
from Database.Database import DatabaseConnection


class LRUCache(OrderedDict):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def get(self, key):
        value = super().get(key)
        if value is not None:
            self.move_to_end(key)
        return value

    def set(self, key, value):
        super().pop(key, None)
        self[key] = value
        if len(self) > self.max_size:
            super().popitem(False)


class SettingsPopup(ttk.window.Toplevel):
    def __init__(self, parent: ttk.window.Window, employeeID: int, theme: str = 'litera'):

        # Initialise TopLevel
        super().__init__(title="Settings", takefocus=True, size=(1000, 1600))  # , transient=parent)
        self.place_window_center()
        self.config = Configuration()
        self.db_connection = DatabaseConnection()
        self.styleObj = ttk.style.Style.get_instance()
        self.font = fonts()
        name = self.db_connection.query_employee(employeeID)[0]
        role = self.db_connection.query_employee(employeeID)[1]
        email = self.db_connection.query_employee(employeeID)[2]
        self.image_widgets = []
        self.image_cache = LRUCache(6)

        # Application Images
        graphics_path = self.config.getGraphicsPath()
        self.image_paths = (
            f'{graphics_path}/testPFP.png',
            f'{graphics_path}/User_Avatars/pfp_template.png',
            f'{graphics_path}/themes_template.png'
        )

        self.image_objects = []
        for im in self.image_paths:
            self.image_objects += [ImageTk.PhotoImage(image=Image.open(im))]

        # Create Frames
        self.scrollable_frame = ScrolledFrame(self, bootstyle="rounded-secondary", padding=0)
        self.scrollable_frame.configure(bootstyle=theme)

        self.title_frame = ttk.Frame(self.scrollable_frame, bootstyle="warning")
        self.accounts_frame = ttk.Frame(self.scrollable_frame)
        self.pfp_frame = ttk.Frame(self.scrollable_frame)
        self.themes_frame = ttk.Frame(self.scrollable_frame)

        self.scrollable_frame.grid(row=1, column=1, sticky='nwes')
        self.title_frame.grid(row=0, column=1, sticky='nwes')
        self.accounts_frame.grid(row=1, column=1, sticky="nwes")
        self.pfp_frame.grid(row=2, column=1, sticky="nwes")
        self.themes_frame.grid(row=3, column=1, sticky="nwes")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(2, weight=1)
        self.scrollable_frame.rowconfigure(3, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)

        # Title Frame
        ttk.Label(self.title_frame, text="Settings", font=self.font.get_font("header1"),
                  foreground=self.styleObj.colors.get('dark'), bootstyle="inverse-warning").grid(row=1, column=1)
        ttk.Frame(self.title_frame, bootstyle="dark", height=1).grid(row=2, column=1, sticky='wes')
        self.title_frame.rowconfigure(1, weight=1)
        self.title_frame.columnconfigure(1, weight=1)

        # Accounts Frame
        ttk.Label(self.accounts_frame, text="Account", font=self.font.get_font("header2")).grid(
            row=0, column=0, sticky="nw", padx=10)
        self.image_widgets += [ttk.Label(self.accounts_frame, image=self.image_objects[0], bootstyle="light")]
        self.image_widgets[0].grid(row=1, column=0)
        ttk.Label(self.accounts_frame, text=name, font=self.font.get_font('header3')).grid(row=2, column=0)
        ttk.Label(self.accounts_frame, text=f"Warehouse {role}", font=self.font.get_font('regular3')).grid(
            row=3, column=0)
        ttk.Frame(self.accounts_frame, height=25).grid(row=4, column=0, sticky="ns")
        ttk.Label(self.accounts_frame, text=f"Email: {email}", font=self.font.get_font('thin1')).grid(row=5, column=0)
        self.styleObj.configure('font.primary.Link.TButton', font=self.font.get_font('thin2'))
        ttk.Button(self.accounts_frame, text=f"Change Password", style='font.primary.Link.TButton').grid(
            row=6, column=0)
        if role == "Administrator":
            self.styleObj.configure('font.danger.Link.TButton', font=self.font.get_font('thin2'))
            ttk.Button(self.accounts_frame, text="Update Accounts", style='font.danger.Link.TButton').grid(
                row=7, column=0)
        ttk.Frame(self.accounts_frame, height=25).grid(row=8, column=0, sticky="nwes")

        self.accounts_frame.rowconfigure(1, weight=1)
        self.accounts_frame.rowconfigure(2, weight=1)
        self.accounts_frame.rowconfigure(3, weight=1)
        self.accounts_frame.rowconfigure(4, weight=5)
        self.accounts_frame.rowconfigure(5, weight=1)
        self.accounts_frame.rowconfigure(6, weight=1)
        self.accounts_frame.rowconfigure(7, weight=1)
        self.accounts_frame.columnconfigure(0, weight=1)

        # PFP Frame
        ttk.Frame(self.pfp_frame, width=8).grid(row=0, column=1, rowspan=2, sticky="nwes")
        ttk.Label(self.pfp_frame, text="Profile Picture", font=self.font.get_font("header2")).grid(
            row=0, column=0, sticky='nw', padx=10)
        #self.styleObj.configure('font.primary.TLabelframe', font=self.font.get_font('header2'), borderwidth=8)
        label = ttk.Label(self, text="Customize your profile picture", font=self.font.get_font('thin2'))
        pfp_label_frame = ttk.LabelFrame(self.pfp_frame, labelwidget=label, bootstyle="info", padding=10)
        #style='font.primary.TLabelframe', height=100, borderwidth=8)
        pfp_label_frame.grid(row=1, column=0, sticky="nwes", padx=10, pady=10)

        self.pfp_frame.rowconfigure(0, weight=1)
        self.pfp_frame.rowconfigure(1, weight=1)
        self.pfp_frame.columnconfigure(0, weight=1)
        self.pfp_frame.columnconfigure(1, weight=0)

        # PFP Canvas
        self.pfp_canvas = ttk.Canvas(pfp_label_frame)
        self.pfp_canvas.grid(row=0, column=0, sticky="nwes")
        self.image_widgets += [self.pfp_canvas.create_image(0, 0, anchor="nw", image=self.image_objects[1])]

        pfp_label_frame.rowconfigure(0, weight=1)
        pfp_label_frame.columnconfigure(0, weight=1)

        # Theme Frame
        ttk.Frame(self.themes_frame, width=8).grid(row=0, column=1, rowspan=2, sticky="nwes")
        ttk.Label(self.themes_frame, text="Theme", font=self.font.get_font("header2")).grid(
            row=0, column=0, sticky="nw", padx=10)
        label = ttk.Label(self, text="Customize your application theme", font=self.font.get_font('thin2'))
        theme_label_frame = ttk.LabelFrame(self.themes_frame, labelwidget=label, bootstyle="info", padding=10)
        theme_label_frame.grid(row=1, column=0, sticky="nwes", padx=10, pady=10)

        self.themes_frame.rowconfigure(0, weight=1)
        self.themes_frame.rowconfigure(1, weight=1)
        self.themes_frame.columnconfigure(0, weight=1)
        self.themes_frame.columnconfigure(1, weight=0)

        # Theme Canvas
        self.themes_canvas = ttk.Canvas(theme_label_frame)
        self.themes_canvas.grid(row=0, column=0, sticky="nwes")
        self.image_widgets += [self.themes_canvas.create_image(0, 0, anchor="nw", image=self.image_objects[2])]

        theme_label_frame.rowconfigure(0, weight=1)
        theme_label_frame.columnconfigure(0, weight=1)

        # Bindings
        self.bind("<Configure>", lambda event: self._resize_images())
        self.pfp_canvas.bind("<Button-1>", lambda event: self._canvas_command(event))
        self.themes_canvas.bind("<Button-1>", lambda event: self._canvas_command(event))

    def _resize_images(self):
        last_resize = getattr(self, '_last_resize', None)
        current_time = time.time()
        if not last_resize or (current_time - last_resize) > 0.01:
            self._last_resize = current_time

            window_cache = self.image_cache.get(f"{self.winfo_width()} - {self.winfo_height()}")
            if window_cache is None:
                img = ImageTk.PhotoImage(self._make_circular_image(self.image_paths[0], int(self.winfo_width() / 4)))
                self.__redisplay_pfp__(self.image_widgets[0], img)
                self.image_cache.set(f"{self.winfo_width()} - {self.winfo_height()}", img)
            else:
                self.__redisplay_pfp__(self.image_widgets[0], window_cache)

            canvas_cache = self.image_cache.get(f"{self.pfp_canvas} - {self.pfp_canvas.winfo_width()}")
            if canvas_cache is None:
                img = ImageTk.PhotoImage(
                    self._resize_rectangular_image(self.image_paths[1], self.pfp_canvas.winfo_width(), 4 / 3))
                self.__redisplay_canvas__(self.pfp_canvas, img, 4 / 3)
                self.image_cache.set(f"{self.pfp_canvas} - {self.pfp_canvas.winfo_width()}", img)
            else:
                self.__redisplay_canvas__(self.pfp_canvas, canvas_cache, 4 / 3)

            canvas_cache = self.image_cache.get(f"{self.themes_canvas} - {self.themes_canvas.winfo_width()}")
            if canvas_cache is None:
                img = ImageTk.PhotoImage(
                    self._resize_rectangular_image(self.image_paths[2], self.themes_canvas.winfo_width(), 0.608))
                self.__redisplay_canvas__(self.themes_canvas, img, 0.608)
                self.themes_frame.configure(height=self.themes_canvas.winfo_height() + 50)
                self.image_cache.set(f"{self.themes_canvas} - {self.themes_canvas.winfo_width()}", img)
            else:
                self.__redisplay_canvas__(self.themes_canvas, canvas_cache, 0.608)


    @lru_cache(2)
    def _canvas_command(self, event):
        x = float(f"{event.x / event.widget.winfo_width():.3f}")
        y = float(f"{event.y / event.widget.winfo_height():.3f}")

        if event.widget == self.pfp_canvas:
            result = "user_"
            if y < 0.25:
                result += "1"
            elif y < 0.5:
                result += "2"
            elif y < 0.75:
                result += "3"
            else:
                result += "4"

            if x < 1/3:
                result += "a"
            elif x < 2/3:
                result += "b"
            else:
                result += "c"

        elif event.widget == self.themes_canvas:
            if x < 0.5 and y < 0.5:
                result = 'yeti'
            elif y < 0.5:
                result = 'litera'
            elif x < 0.5:
                result = 'pulse'
            else:
                result = 'flatly'

        print(result)

    @staticmethod
    @lru_cache(2)
    def _make_circular_image(image_path, output_diameter):

        img = Image.open(image_path).resize((output_diameter, output_diameter))

        mask = Image.new('L', (output_diameter, output_diameter), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, output_diameter, output_diameter), fill=255)

        output_img = Image.new(img.mode, (output_diameter, output_diameter), 0)
        output_img.paste(img, mask=mask)

        return output_img

    @staticmethod
    @lru_cache(4)
    def _resize_rectangular_image(image_path, output_width, aspect_ratio: float = 1):
        img = Image.open(image_path).resize((max(int(output_width), 1), max(int(output_width * aspect_ratio), 1)))
        return img

    @staticmethod
    @lru_cache(2)
    def __redisplay_pfp__(widget, image):
        widget.configure(image=image)

    @staticmethod
    @lru_cache(4)
    def __redisplay_canvas__(canvas, image, aspect_ratio: float = 1):
        canvas.configure(height=int(canvas.winfo_width() * aspect_ratio))
        canvas.itemconfig(1, image=image)


if __name__ == '__main__':
    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    window.withdraw()

    SettingsPopup(window, 1)

    # Starts Event Main Loop
    window.mainloop()
