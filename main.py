#!/usr/bin/python3

import tkinter as tk
from tkinter import messagebox as mb
from point import *
from vector import *
from algos import *
from functools import partial


class MainApp(tk.Frame):

    MIN_DIST = 6

    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.cv = tk.Canvas(self, bg="white")
        self.menubar = tk.Menu(self.parent, tearoff=0)
        self.select_menu = tk.Menu(self.menubar, tearoff=0)
        self.fig_menu = tk.Menu(self.menubar, tearoff=0)
        self.alg_menu = tk.Menu(self.menubar, tearoff=0)
        self.coords_status = tk.Label(self.parent, text="x: 0, y: 0", font=("default", 8))
        self.nselected = 0
        self.setui()
        self.mod = "none"
        self.figs = []
        self.popup_menu = None

    def del_fig(self):
        f = self.figs.pop()
        f.destroy()
        self.cv.delete("follow_last")
        self.cv.delete("follow_first")
        self.mod = "none"

    def place_point(self, event):
        self.figs[-1].add_vertex(Point(event.x, event.y))

    def pop_point(self, event):
        if len(self.figs[-1].vertexes) == 1:
            self.del_fig()
        else:
            self.figs[-1].pop_vertex()
            self.follow_placing_pg(event)

    def follow_placing_pg(self, event):
        if len(self.figs[-1].vertexes) > 0:
            self.cv.delete("follow_last")
            self.cv.delete("follow_first")
            self.cv.create_line(event.x, event.y,
                                self.figs[-1].vertexes[-1].x, self.figs[-1].vertexes[-1].y,
                                width=1, fill="gray", tag="follow_last")
            self.cv.create_line(event.x, event.y,
                                self.figs[-1].vertexes[0].x, self.figs[-1].vertexes[0].y,
                                width=1, fill="gray", tag="follow_first")
            dx = event.x - self.figs[-1].vertexes[0].x
            dy = event.y - self.figs[-1].vertexes[0].y
            if dx * dx + dy * dy < MainApp.MIN_DIST ** 2:
                self.cv.create_oval(self.figs[-1].vertexes[0].x - MainApp.MIN_DIST,
                                    self.figs[-1].vertexes[0].y - MainApp.MIN_DIST,
                                    self.figs[-1].vertexes[0].x + MainApp.MIN_DIST,
                                    self.figs[-1].vertexes[0].y + MainApp.MIN_DIST,
                                    fill=None, width=MainApp.MIN_DIST - 2, tag="hghlt", outline="lightblue")
            else:
                self.cv.delete("hghlt")

    def start_setting_pg(self):
        if self.mod == "none":
            self.figs.append(Polygon(self.cv))
            self.mod = "placing_pg"

    def stop_setting_pg(self, event):
        if len(self.figs[-1].vertexes) == 1:
            mb.showerror("Ошибка", "Многоугольник из одной точки? Серьезно?")
            return
        self.cv.delete("follow_last")
        self.cv.delete("follow_first")
        self.cv.delete("hghlt")
        self.figs[-1].finish_adding_verts()
        self.mod = "none"
        self.menubar.entryconfigure(1, state=tk.NORMAL)

    def select_fig(self, index):
        res = self.figs[index].select()
        self.nselected += res

    def del_selected(self):
        for f in self.figs:
            if f.selected:
                self.nselected -= 1
                f.destroy()
        self.figs = [f for f in self.figs if not f.destroyed]

    def select_all(self):
        for f in self.figs:
            if not f.selected:
                f.select()
                self.nselected += 1

    def release_selection(self):
        for f in self.figs:
            if f.selected:
                f.select()
                self.nselected -= 1

    def b1_handler(self, event):
        if self.popup_menu is not None:
            self.popup_menu.destroy()
        if self.mod == "placing_pg":
            if len(self.figs[-1].vertexes) > 0:
                dx = event.x - self.figs[-1].vertexes[0].x
                dy = event.y - self.figs[-1].vertexes[0].y
                if dx * dx + dy * dy < MainApp.MIN_DIST ** 2:
                    self.stop_setting_pg(event)
                    return
            self.place_point(event)

    def motion_handler(self, event):
        self.coords_status.config(text="x: " + str(event.x) + ", y: " + str(event.y))
        if self.mod == "placing_pg":
            self.follow_placing_pg(event)

    def b3_handler(self, event):
        if self.mod == "placing_pg":
            # если сразу же передумали добавлять фигуру
            if len(self.figs[-1].vertexes) == 0:
                self.figs.pop()
                self.mod = 'none'
            else:
                self.pop_point(event)
        elif self.mod == 'none':
            self.popup(event)
            pass

    def popup(self, event):
        if self.popup_menu is not None:
            self.popup_menu.destroy()
        self.popup_menu = tk.Menu(self.parent, tearoff=0)
        for i in range(0, len(self.figs)):
            self.popup_menu.add_command(label="Fig " + str(i), command=partial(self.select_fig, i))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Удалить', command=self.del_selected)
        self.popup_menu.add_command(label='Выделить все', command=self.select_all)
        self.popup_menu.add_command(label='Снять выделение', command=self.release_selection)
        self.popup_menu.post(event.x_root, event.y_root)

    def is_conv(self):
        if self.nselected != 1:
            mb.showerror("Ошибка", "Нужно выделить ровно один многоугольник")
            return
        f = None
        for f in self.figs:
            if f.selected:
                break
        res = is_convex(f)
        if res:
            mb.showinfo('Результат', 'Выпуклый')
        else:
            mb.showinfo('Результат', 'Невыпуклый')
        f.select()
        self.nselected -= 1

    def show_sp(self):
        if self.nselected != 1:
            mb.showerror("Ошибка", "Нужно выделить ровно один многоугольник")
            return
        f: Polygon = None
        for f in self.figs:
            if f.selected:
                break
        mb.showinfo("Результат", "Периметр: %.3f \n Площадь: %.3f" % (get_perimeter(f), get_square(f)))
        f.select()
        self.nselected -= 1

    def setui(self):
        self.parent.title("Geometry")
        self.pack(fill=tk.BOTH, expand=1)

        self.cv.pack(expand=True, fill=tk.BOTH)
        self.cv.bind("<1>", self.b1_handler)
        self.cv.bind("<Motion>", self.motion_handler)
        self.cv.bind("<3>", self.b3_handler)

        self.coords_status.pack()

        self.parent.config(menu=self.menubar)
        self.fig_menu.add_command(label="Многоугольник", command=self.start_setting_pg)
        self.alg_menu.add_command(label="Выпуклый?", command=self.is_conv)
        self.alg_menu.add_command(label='S, P', command=self.show_sp)
        self.menubar.add_cascade(label="Фигуры", menu=self.fig_menu)
        self.menubar.add_cascade(label='Алгоритмы', menu=self.alg_menu)


def main():
    root = tk.Tk()
    root.geometry("850x500+200+100")
    MainApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
