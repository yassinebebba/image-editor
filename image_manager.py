from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk
from PIL import Image, ImageTk
from WindowCreator import WC


class ImageManager:
    canvas = None
    def __init__(self, img, x, y, id=None):

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


    def _add_image(self):
        def add(image, x, y, id=None):

            key = 'image#' + id
            if key in self.obj_id_ref:
                messagebox.showerror("ID conflict",
                                     "There has been a conflict with objects IDs.\nPlease add a unique ID.")
            else:
                self.ref.append(PhotoImage(file=image))
                image_holder = self._canvas.create_image(x, y, image=self.ref[0], anchor=N)
                self.obj_id_ref[key] = image_holder
                self.listbox_obj.insert(END, key)

master = Tk()

Thumbnail(master)

master.mainloop()
