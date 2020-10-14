from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk
from PIL import Image, ImageTk
from WindowCreator import WC


class Thumbnail:
    def __init__(self, root, width=1280, height=720):
        self.ref = []
        self.obj_id_ref = {}

        self.root = root
        self.width = width
        self.height = height
        self._screen_width = self.root.winfo_screenwidth()
        self._screen_height = self.root.winfo_screenheight()

        # window

        self.root.title('Thumbnail Editor')
        self._screen_meta = f'{self.width}x{self.height}+' \
                            f'{int((self._screen_width - self.width) / 2)}+' \
                            f'{int((self._screen_height - self.height) / 2)}'
        self.root.geometry(self._screen_meta)

        # Menu

        self.main_menu = Menu(self.root)

        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label='Open Photo', command=None)
        self.file_menu.add_command(label='Add Photo', command=self._add_image)
        self.file_menu.add_command(label='Save Thumbnail', command=lambda: self._save(self._canvas))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=lambda: self.root.destroy())

        self.main_menu.add_cascade(label='File', menu=self.file_menu)

        self.root.config(menu=self.main_menu)

        # Toolbar

        self.toolbar = Frame(self.root, bd=1, bg='white', relief=RAISED)

        # add image
        add_image_icon = Image.open('icons/add_image.png')
        add_image_icon_tk = ImageTk.PhotoImage(add_image_icon)
        add_image_button = Button(self.toolbar, image=add_image_icon_tk, bg='white', command=lambda: self._add_image())
        add_image_button.image = add_image_icon_tk
        add_image_button.pack(side=LEFT, pady=5, padx=2)

        # add text
        '''add_text_icon = Image.open('icons/add_text.png')
        add_text_icon_tk = ImageTk.PhotoImage(add_text_icon)
        add_text_button = Button(self.toolbar, image=add_text_icon_tk, bg='white', command=lambda: self._add_text())
        add_text_button.image = add_text_icon_tk
        add_text_button.pack(side=LEFT, pady=5, padx=2)'''

        # add shapes
        '''add_shapes_icon = Image.open('icons/add_shapes.png')
        add_shapes_icon_tk = ImageTk.PhotoImage(add_shapes_icon)
        add_shapes_button = Button(self.toolbar, image=add_shapes_icon_tk, bg='white',
                                   command=lambda: self._add_shapes())
        add_shapes_button.image = add_shapes_icon_tk
        add_shapes_button.pack(side=LEFT, pady=5, padx=2)'''

        self.toolbar.pack(side=TOP, fill=X)
        # main frame
        self.main_frame = Frame(root, width=self.width)
        self.main_frame.pack(side=LEFT)

        # Editor main body
        # X axis
        self._canvas_x_axis = Canvas(self.main_frame, width=self.width, height=20)
        self._canvas_x_axis.config(bg='white')
        self._canvas_x_axis.pack(side=TOP, anchor=N)
        for i in range(self.width + 1):
            if i % 100 == 0:
                self._canvas_x_axis.create_line(i, 0, i, 15)
            elif i % 5 == 0:
                self._canvas_x_axis.create_line(i, 0, i, 10)

        # Y axis
        self._canvas_y_axis = Canvas(self.main_frame, width=20, height=self.height)
        self._canvas_y_axis.config(bg='white')
        self._canvas_y_axis.pack(side=LEFT)
        for i in range(self.width + 1):
            if i % 100 == 0:
                self._canvas_y_axis.create_line(0, i, 15, i)
            elif i % 5 == 0:
                self._canvas_y_axis.create_line(0, i, 10, i)

        # Real Canvas
        canvas_scrollbar_vertical = Scrollbar(self.main_frame, orient=VERTICAL)
        canvas_scrollbar_horizontal = Scrollbar(self.main_frame, orient=HORIZONTAL)

        self._canvas = Canvas(self.main_frame,
                              width=self.width,
                              height=self.height,
                              yscrollcommand=canvas_scrollbar_vertical.set,
                              xscrollcommand=canvas_scrollbar_horizontal.set,
                              scrollregion=(0, 0, self.width, self.height)
                              )
        self._canvas.config(bg='white')
        canvas_scrollbar_vertical.config(command=self._canvas.yview)
        canvas_scrollbar_vertical.pack(side=RIGHT, fill=Y)
        canvas_scrollbar_horizontal.config(command=self._canvas.xview)
        canvas_scrollbar_horizontal.pack(side=BOTTOM, fill=X)
        self._canvas.pack()

        # Listbox to hold objects and events
        self.listbox_frame = Frame(root, height=30)
        Label(self.listbox_frame, text='Events:').grid(row=0, column=0, sticky=NW)
        listbox_obj_scrollbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.listbox_obj = Listbox(self.listbox_frame, width=30, height=25, yscrollcommand=listbox_obj_scrollbar.set)
        self.listbox_obj.bind("<<ListboxSelect>>", self.select_obj)
        self.listbox_obj.grid(row=1, column=0, columnspan=2, sticky=NE)
        listbox_obj_scrollbar.config(command=self.listbox_obj.yview)
        listbox_obj_scrollbar.grid(row=1, column=2, sticky=N + E + S)
        self.listbox_frame.pack(side=RIGHT, anchor=N)

        edit_button = Button(self.listbox_frame, text='Edit', command=self._add_draggable)
        edit_button.grid(row=2, column=0, sticky=W)
        delete_button = Button(self.listbox_frame, text='Delete', command=self.delete_obj)
        delete_button.grid(row=2, column=1, sticky=W)

        # Canvas motion tracking
        self.coor_label = Label(self.toolbar, text="Coordinates:")
        self.coor_label.pack(side=LEFT, pady=5, padx=2)
        self._canvas.bind('<Motion>', self._motion)

        self._canvas.bind('<B1-Motion>', self._b1_motion)

    def _motion(self, event=None):
        pass

    def _b1_motion(self, event=None):
        self.coor_label['text'] = f'Coordinates: x = {event.x}px, y = {event.y}px'
        self.pic = PhotoImage(file='random.png')
        self.xx = self._canvas.create_image(event.x, event.y, image=self.pic)
        self._canvas.tag_lower(self.xx)


    def select_obj(self, event=None):
        box = event.widget
        try:
            index = int(box.curselection()[0])
            selected_obj = self.listbox_obj.get(index)
        # self._canvas.itemconfigure(self.obj_id_ref[selected_obj], fill='black')
        except:
            pass

    def delete_obj(self, event=None):
        try:
            index = int(self.listbox_obj.curselection()[0])
            selected_obj = self.listbox_obj.get(index)
            self._canvas.delete(self.obj_id_ref[selected_obj])
            self.listbox_obj.delete(index)
            del self.obj_id_ref[selected_obj]
        except:
            pass

    def _add_image(self):
        def add(image, x, y, id=None):

            key = 'image#' + id
            if key in self.obj_id_ref:
                messagebox.showerror("ID conflict",
                                     "There has been a conflict with objects IDs.\nPlease add a unique ID.")
            else:
                self.ref.append(PhotoImage(file=image))
                image_holder = self._canvas.create_image(x, y, image=self.ref[0], anchor=N)
                self._canvas.update()
                self.obj_id_ref[key] = image_holder
                self.obj_id_ref[key] = image_holder
                self.listbox_obj.insert(END, key)

        window = Tk()
        WC(window, 'Add Image')

        img = filedialog.askopenfilename(initialdir='/', title='Add a Photo', filetypes=(('image', '*.*'),))

        Label(window, text='ID for your image:').pack()
        id_entry = Entry(window)
        id_entry.pack()

        Label(window, text='X Coordinate:').pack()
        x_entry = Entry(window)
        x_entry.pack()

        Label(window, text='Y Coordinate:').pack()
        y_entry = Entry(window)
        y_entry.pack()

        add_button = Button(window, text='Add', command=lambda: add(
            img,
            int(x_entry.get()),
            int(y_entry.get()),
            id_entry.get(),
        ))
        add_button.pack()

        window.mainloop()

    def _add_draggable(self):
        index = int(self.listbox_obj.curselection()[0])
        selected_obj = self.listbox_obj.get(index)
        print(type(self._canvas.find_withtag(self.obj_id_ref[selected_obj])))


    @staticmethod
    def _save(canvas):
        canvas.postscript(file="Thumbnail.eps", colormode='color', x=0, y=0, height=720, width=1280)


master = Tk()

Thumbnail(master)

master.mainloop()
