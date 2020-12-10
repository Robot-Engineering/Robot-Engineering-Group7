import json
import tkinter as tk
import turtle as tl
import func
from Stack import *
from tkinter import filedialog, messagebox, colorchooser


class Document:
    def __init__(self, draw_area):
        self.draw_area = draw_area

    def select(self):
        self.draw_area.draw_func = None
        self.draw_area.select = True

    def reset(self, event):
        self.draw_area.click1_pos = None

    def pan(self):
        pass

    def clear(self):
        self.draw_area.graphic_list = Stack()
        self.draw_area.graphics_count = 0
        self.draw_area.turtle.clear()
        self.draw_area.refresh()

    def undo(self, event=None):
        # print(event)
        if self.draw_area.graphics_count > 0:
            recover_graphic = self.draw_area.graphic_list.pop()
            self.draw_area.recover_list.push(recover_graphic)
            self.draw_area.refresh()
            self.draw_area.graphics_count -= 1

    def recover(self, event=None):
        # print(event)
        if len(self.draw_area.recover_list.stack) > 0:
            recover_graphic = self.draw_area.recover_list.pop()
            self.draw_area.graphic_list.push(recover_graphic)
            self.draw_area.refresh()
            self.draw_area.graphics_count += 1

    def exit(self):
        self.draw_area.root.quit()

    def edit(self):
        print('exit')
        self.draw_area.root.quit()

    def save(self):
        file_name = filedialog.asksaveasfilename()
        graphics = []
        if file_name:
            for graphic in self.draw_area.graphic_list.stack:
                t = graphic.__dict__
                t.pop('draw_area')
                graphics.append(json.dumps(t))
            with open(f'{file_name}.json', 'w') as f:
                json.dump(graphics, f)
            self.draw_area.is_saved = True
            print(f'save to{file_name}!~')

    def open(self):
        file = filedialog.askopenfiles()
        data = json.load(file[0])
        file[0].close()
        if data:
            for graphic in data:
                self.draw_area.graphics.append(json.loads(graphic))
            # print(self.draw_area.graphics)
            print(f'read {file[0].name}!~')
            self.draw_area.refresh()

    def close(self):
        self.draw_area.graphics = list()
        self.draw_area.graphic_list = Stack()
        self.draw_area.graphics_count = 0
        self.draw_area.refresh()

    def cancel(self, event=None):
        self.draw_area.select = True
        self.draw_area.draw_func = None
        if self.draw_area.click1_pos is not None and self.draw_area.click2_pos is None:
            self.draw_area.refresh()
            self.draw_area.click1_pos = None

    def function(self):
        self.draw_area.turtle.goto(-300, 50)
        self.draw_area.turtle.pendown()
        self.draw_area.turtle.write('右键画布选择图形绘图;\ncontrol-z撤销，control-a(恢复最多七个);\nesc取消绘制;',
                                    font=("Arial", 25))

    def draw_line(self):
        # print('change to line')
        self.draw_area.select = False
        self.draw_area.draw_func = 'LINE'

    def draw_circle(self):
        self.draw_area.select = False
        self.draw_area.draw_func = 'CIRCLE'

    def draw_rect(self):
        self.draw_area.select = False
        self.draw_area.draw_func = 'RECT'

    def choose_color(self):
        color = colorchooser.askcolor()
        self.draw_area.pen_color = color[1]
        self.draw_area.turtle.pencolor(self.draw_area.pen_color)


class Pan:
    pass


class DrawArea:
    def __init__(self):
        self.size = {'width': 700, 'height': 500}
        self.root = tk.Tk()
        self.root.title('画图')
        self.root.geometry('{0}x{1}+500+100'.format(self.size['width'], self.size['height']))
        self.canvas = tk.Canvas(self.root, width=self.size['width'], height=self.size['height'])
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.turtle = tl.RawTurtle(self.canvas)
        self.turtle.hideturtle()
        self.turtle._tracer(False)
        self.turtle.penup()
        self.pen_color = '#000000'
        self.turtle.pencolor(self.pen_color)
        self.graphics = list()
        self.graphic_list = Stack()
        self.recover_list = Queue(7)
        self.graphics_count = 0
        self.select = True
        self.draw_func = None
        self.click1_pos = None
        self.click2_pos = None
        self._click2_pos = None
        self.is_saved = False
        self.pan = Pan()

    def add_graphic(self, graphic):
        self.graphic_list.push(graphic)
        self.graphics_count += 1

    def refresh(self):
        self.turtle.clear()
        if self.graphics:
            for graphic in self.graphics:
                self.draw(graphic)
        if self.graphic_list is not None:
            for graphic in self.graphic_list.stack:
                graphic.draw()

    def get_pos(self, event):
        if not self.select:
            if self.click1_pos is None:
                # print('坐标：', event.x, event.y)
                self.click1_pos = {
                    'x': event.x - self.size['width']/2,
                    'y': (event.y - self.size['height']/2)*(-1),
                }
            else:
                self.click2_pos = {
                    'x': event.x - self.size['width']/2,
                    'y': (event.y - self.size['height']/2)*(-1),
                }
                self.drawing()
                self.click1_pos = None
                self.click2_pos = None
                self._click2_pos = None

    def mouse_move(self, event):
        if not self.select and self.click1_pos is not None:
            self._click2_pos = {
                'x': event.x - self.size['width'] / 2,
                'y': (event.y - self.size['height'] / 2) * (-1),
            }
            self.drawing()

    def drawing(self):
        if not self.select:
            self.refresh()
            if self.draw_func == 'LINE':
                line = DrawLine(self.click1_pos, self.click2_pos or self._click2_pos, self, self.pen_color)
                line.drawing() if self.click2_pos is not None else self.refresh(), line.draw()
            elif self.draw_func == 'CIRCLE':
                circle = DrawCircle(self.click1_pos, self.click2_pos or self._click2_pos, self)
                circle.drawing() if self.click2_pos is not None else self.refresh(), circle.draw()
            elif self.draw_func == 'RECT':
                rect = DrawRect(self.click1_pos, self.click2_pos or self._click2_pos, self)
                rect.drawing() if self.click2_pos is not None else self.refresh(), rect.draw()

    def draw(self, graphic):
        if graphic['graphic_type'] == 'LINE':
            line = DrawLine(graphic['start_point'], graphic['end_point'], self, graphic['color'])
            line.draw()
        elif graphic['graphic_type'] == 'CIRCLE':
            circle = DrawCircle(graphic['start_point'], graphic['end_point'], self, graphic['color'])
            circle.draw()
        elif graphic['graphic_type'] == 'RECT':
            rect = DrawRect(graphic['_start_point'], graphic['_end_point'], self, graphic['color'])
            rect.draw()


class Graphic:
    def __init__(self, start_point, end_point, draw_area):
        self.start_point = start_point
        self.end_point = end_point
        self.draw_area = draw_area
        self.pen_color = self.draw_area.pen_color
        self.graphic_type = None

    def draw_tracker(self):
        pass

    def draw(self):
        pass

    def drawing(self):
        pass


class DrawLine(Graphic):
    def __init__(self, start_point, end_point, draw_area, color=None):
        super().__init__(start_point, end_point, draw_area)
        self.line_length = func.distance2p(start_point, end_point)
        self.color = color or self.pen_color
        self.graphic_type = 'LINE'

    # def draw_tracker(self):
    #     start_point = self.draw_area.get_pos()

    def draw(self):
        # print('sp', self.start_point['x'], self.start_point['y'],'ep',self.end_point['x'], self.end_point['y'])
        canvas = self.draw_area.turtle
        canvas.pencolor(self.color)
        canvas.goto(self.start_point['x'], self.start_point['y'])
        canvas.pendown()
        canvas.goto(self.end_point['x'], self.end_point['y'])
        canvas.penup()

    def drawing(self):
        self.draw()
        self.draw_area.add_graphic(self)


class DrawRect(DrawLine):
    def __init__(self, start_point, end_point, draw_area, color=None):
        super().__init__(start_point, end_point, draw_area)
        self.line_length = func.distance2p(start_point, end_point)
        self._start_point = self.start_point
        self._end_point = self.end_point
        self.color = color or self.pen_color
        self.graphic_type = 'RECT'
        # print(start_point, end_point)

    def draw(self):
        steps = [
            {'x': self._start_point['x'], 'y': self._start_point['y']},
            {'x': self._end_point['x'], 'y': self._start_point['y']},
            {'x': self._end_point['x'], 'y': self._end_point['y']},
            {'x': self._start_point['x'], 'y': self._end_point['y']},
        ]
        # print(steps)
        for i in range(5):
            self.start_point = steps[i % 4]
            self.end_point = steps[(i+1) % 4]
            super().draw()

    def drawing(self):
        self.draw()
        self.draw_area.add_graphic(self)


class DrawCircle(Graphic):
    def __init__(self, start_point, end_point, draw_area, color=None):
        super().__init__(start_point, end_point, draw_area)
        self.r = func.distance2p(self.start_point, self.end_point)
        self.origin = self.start_point
        self.graphic_type = 'CIRCLE'
        self.color = color or self.pen_color

    # def draw_tracker(self):
    #     start_point = self.draw_area.get_pos()

    def draw(self):
        canvas = self.draw_area.turtle
        canvas.pencolor(self.color)
        canvas.goto(self.start_point['x'], self.start_point['y'] - self.r)
        canvas.pendown()
        canvas.circle(self.r)
        canvas.penup()

    def drawing(self):
        self.draw()
        self.draw_area.add_graphic(self)


class View(Document):
    def __init__(self, draw_area):
        super().__init__(draw_area)
        self.menu = tk. Menu(self.draw_area.root)
        self.file_menu = tk. Menu(self.menu, tearoff=False)
        self.file_menu.add_command(label='open', command=self.open)
        self.file_menu.add_command(label='close', command=self.close)
        self.file_menu.add_command(label='save', command=self.save)
        self.file_menu.add_command(label='exit', command=self.exit)
        self.menu.add_cascade(label='file', menu=self.file_menu)
        self.edit_menu = tk. Menu(self.menu, tearoff=False)
        self.edit_menu.add_command(label='clear', command=self.clear)
        self.edit_menu.add_command(label='undo', command=self.undo)
        self.edit_menu.add_command(label='recover', command=self.recover)
        self.menu.add_cascade(label='edit', menu=self.edit_menu)
        self.help_menu = tk. Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label='function', command=self.function)
        self.menu.add_cascade(label='help', menu=self.help_menu)
        self.draw_area.root.config(menu=self.menu)
        self.quick_menu = tk. Menu(self.draw_area.root, tearoff=0)
        self.quick_menu.add_command(label='select', command=self.select)
        self.quick_menu.add_command(label='insertLine', command=self.draw_line)
        self.quick_menu.add_command(label='insertCircle', command=self.draw_circle)
        self.quick_menu.add_command(label='insertRect', command=self.draw_rect)
        self.quick_menu.add_command(label='chooseColor', command=self.choose_color)

    def q_menu(self, event):
        self.quick_menu.post(event.x_root, event.y_root)

    def show(self):
        messagebox.askquestion(title='功能', message='右键画布选择图形绘图;\n'
                                                   'control-z撤销，control-a恢复最多七个;\nesc取消绘制;')
        self.draw_area.canvas.bind("<Button-1>", self.draw_area.get_pos)
        self.draw_area.canvas.bind("<Motion>", self.draw_area.mouse_move)
        self.draw_area.root.bind("<Button-3>", self.q_menu)
        self.draw_area.root.bind("<Control-z>", self.undo)
        self.draw_area.root.bind("<Control-a>", self.recover)
        self.draw_area.root.bind("<Escape>", self.cancel)
        # self.draw_area.turtle._update()
        self.draw_area.root.mainloop()


if __name__ == '__main__':
    print('运行main')
