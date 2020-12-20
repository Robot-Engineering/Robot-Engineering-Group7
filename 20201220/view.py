import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk


class View:
    def __init__(self, data=None):
        self.root = tk.Tk()
        self.root.title('哈哈')
        self.root.geometry('700x500+500+100')
        self.box = tk.Label(self.root, text='学生列表')
        self.c_box = ttk.Combobox(self.root)
        self.data = data
        self.parse_json()
        self.c_box['value'] = [r'101.jpg'] if not data else [datum['name'] for datum in data]
        self.get_images = None if not data else [[datum['name'],
                                                  datum['image']+'/' + datum['image'][-3:] + '.jpg'] for datum in data]
        self.show_image = None
        self.image = None
        self.c_box.current(0)
        self.c_box.pack()

    def get(self, event):
        try:
            self.get_images = self.c_box.get()
            self.image = ImageTk.PhotoImage(Image.open(self.get_images))
            self.show_image = tk.Label(self.root, image=self.image)
        except Exception as e:
            print('get', e)
        self.show_image = tk.Label(self.root, image=self.image)
        self.show_image.pack()

    def show(self, event):
        name = self.c_box.get()
        try:
            for image in self.get_images:
                if name in image[0] and len(image[1]) > 5:
                    if self.image:
                        self.show_image.destroy()
                    self.image = ImageTk.PhotoImage(Image.open(image[1]))
                    self.show_image = tk.Label(self.root, image=self.image)
                    self.show_image.image = ImageTk.PhotoImage(Image.open(image[1]))
                    self.show_image.pack()
                    break
            else:
                self.show_image.destroy()
                self.show_image = tk.Label(self.root, text=name+'没交照片')
                self.show_image.pack()
        except Exception as e:
            print('show', e)

    def to_json(self):
        pass

    def parse_json(self):
        self.data = json.dumps(self.data)


if __name__ == '__main__':
    view = View()
    view.c_box.bind("<<ComboboxSelected>>", view.show)
    view.root.mainloop()
