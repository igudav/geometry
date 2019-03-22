import tkinter as tk
from point import *
from vector import *
from algos import *


class MainApp(tk.Frame):

    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.cv = tk.Canvas(self, bg="white")
        self.setui()
        self.mod = "none"
        self.figs = []

    def del_fig(self):
        self.figs.pop()
        self.cv.delete("follow_last")
        self.cv.delete("follow_first")
        self.mod = "none"

    def place_point(self, event):
        if self.mod == "placing_pg":
            self.figs[-1].add_vertex(Point(event.x, event.y))
            self.cv.create_oval(event.x - 3,
                                event.y - 3,
                                event.x + 3,
                                event.y + 3,
                                fill="yellow", outline="black",
                                tag=str(self.figs[-1].myid) + "v" + str(self.figs[-1].vertexes[-1].myid))
            if len(self.figs[-1].vertexes) > 1:
                self.cv.create_line(event.x, event.y,
                                    self.figs[-1].vertexes[-2].x, self.figs[-1].vertexes[-2].y,
                                    width=2, fill="black",
                                    tag=str(self.figs[-1].myid) + "e" + str(self.figs[-1].edges[-2].myid))

    def pop_point(self):
        self.cv.delete(str(self.figs[-1].myid) + "v" + str(self.figs[-1].vertexes[-1].myid))
        if len(self.figs[-1].vertexes) == 1:
            self.del_fig()
        else:
            self.cv.delete(str(self.figs[-1].myid) + "e" + str(self.figs[-1].edges[-2].myid))
            self.figs[-1].pop_vertex()

    def follow_placing_pg(self, event):
        if self.mod == "placing_pg" and len(self.figs[-1].vertexes) > 0:
            self.cv.delete("follow_last")
            self.cv.delete("follow_first")
            self.cv.create_line(event.x, event.y,
                                self.figs[-1].vertexes[-1].x, self.figs[-1].vertexes[-1].y,
                                width=1, fill="gray", tag="follow_last")
            self.cv.create_line(event.x, event.y,
                                self.figs[-1].vertexes[0].x, self.figs[-1].vertexes[0].y,
                                width=1, fill="gray", tag="follow_first")

    def start_setting_pg(self):
        if self.mod == "none":
            self.figs.append(Polygon())
            self.mod = "placing_pg"

    def stop_setting_pg(self, event):
        if self.mod == "placing_pg":
            self.cv.delete("follow_last")
            self.cv.delete("follow_first")
            self.cv.create_line(self.figs[-1].vertexes[-1].x, self.figs[-1].vertexes[-1].y,
                                self.figs[-1].vertexes[0].x, self.figs[-1].vertexes[0].y,
                                width=2, fill="black",
                                tag=str(self.figs[-1].myid) + "e" + str(self.figs[-1].edges[-1].myid))
            self.mod = "none"

    def b1_handler(self, event):
        if self.mod == "placing_pg":
            self.place_point(event)

    def motion_handler(self, event):
        if self.mod == "placing_pg":
            self.follow_placing_pg(event)

    def b3_handler(self, event):
        if self.mod == "placing_pg":
            self.pop_point()

    def setui(self):
        self.parent.title("Geometry")
        self.pack(fill=tk.BOTH, expand=1)

        self.cv.pack(expand=True, fill=tk.BOTH)
        self.cv.bind("<1>", self.b1_handler)
        self.cv.bind("<Motion>", self.motion_handler)
        self.cv.bind("<2>", self.stop_setting_pg)
        self.cv.bind("<3>", self.b3_handler)

        menubar = tk.Menu(self.parent, tearoff=0)
        self.parent.config(menu=menubar)
        fig_menu = tk.Menu(menubar, tearoff=0)
        fig_menu.add_command(label="Polygon", command=self.start_setting_pg)
        # alg_menu = tk.Menu(menubar, tearoff=0)
        # alg_menu.add_command(label="Is convex?", command = )
        menubar.add_cascade(label="Figures", menu=fig_menu)


def main():
    root = tk.Tk()
    root.geometry("850x500+200+100")
    app = MainApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
