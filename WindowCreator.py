class WC:
    def __init__(self, root, title='Window', width=400, height=500, x_pos=None, y_pos=None):
        self.root = root
        self._screen_width = self.root.winfo_screenwidth()
        self._screen_height = self.root.winfo_screenheight()
        if x_pos and y_pos:
            self.root.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        else:
            x_pos = int((self._screen_width - width) / 2)
            y_pos = int((self._screen_height - height) / 2)
            self.root.geometry(f'{width}x{height}+{x_pos}+{y_pos}')

        self.root.title(title)
