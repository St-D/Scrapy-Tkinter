#  -*- coding: cp1251 -*-                                                                                             #
# Python 3.x.x
#


import os
import tkinter as tk
import json
from sys import path
path.append('../../up_w')
from settings import FILE_RESULT, USER_AGENT_LIST


class WinUpwork(tk.Frame):

    total_butt = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="#F0F0F0")
        self.parent = parent

        self.canvas = tk.Canvas(parent, borderwidth=0, background="#E5E5E5", height=250, width=500)
        self.frame = tk.Frame(self.canvas, background="#E5E5E5", height=250, width=500, relief="solid")

        # foot block
        self.frame_foot = tk.Frame(parent, background="#E5E5E5", height=100, width=500, relief="solid")
        self.frame_foot.place(x=0, y=250, width=500, height=100)
        self.btn_foot = tk.Button(self.frame_foot, relief="ridge", justify='center', state='disabled', bd=3, bg="#E5E5E5")
        self.btn_foot.pack(side="bottom", fill="both", expand=True)
        # **********

        # if WinUpwork.total_butt <= 6:
        self.vsb = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.place(x=460, y=41, width=20, height=205)
        self.canvas.place(x=0, y=0, height=250, width=500, bordermode='inside')

        self.win = self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.reset_scroll_region)

        self.init_ui()
        self.create_footer()

    def init_ui(self):
        self.parent.title("upwork.com")

        tk.Label(self.frame, text='Результаты прохода в категории <Python> :', bg="#E5E5E5") \
            .grid(row=0, column=0, padx=100, pady=10)

    def create_but(self, text=None):
        WinUpwork.total_butt += 1

        i = 0
        for butt in range(1, WinUpwork.total_butt + 1):
            i += 1

        url_btn = tk.Button(self.frame, text=text, relief="ridge", justify='left', wraplength=390)
        chk_on_btn = tk.Checkbutton(self.frame)

        url_btn.grid(row=i, column=0, ipadx=2, ipady=2, padx=2, sticky="nw, ne")
        chk_on_btn.grid(row=i, column=0, padx=5, pady=3, sticky="ne")

    def reset_scroll_region(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_footer(self):
        variable = tk.StringVar(self.frame_foot)
        variable.set(USER_AGENT_LIST[0])  # default value
        combobox = tk.OptionMenu(self.frame_foot, variable, *USER_AGENT_LIST, )

        tk.Label(self.frame_foot, text='User agent', bg="#E5E5E5").place(x=10, y=5, width=75, height=40)
        combobox.place(x=60, y=10, width=425, height=25)

        tk.Label(self.frame_foot, text='Сканировать сайт', bg="#E5E5E5", wraplength=75).\
            place(x=10, y=40, width=75, height=40)

        start_btn = tk.Button(self.frame_foot, text='СТАРТ', relief="raised", justify='center', command=start_spider).\
            place(x=85, y=45, width=150, height=30)

        self.hid_btn()

    def hid_btn(self):
        tk.Label(self.frame_foot, text='Скрыть отмеченное', bg="#E5E5E5", wraplength=75).\
            place(x=260, y=40, width=75, height=40)

        hidden_btn = tk.Button(self.frame_foot, text='СКРЫТЬ', relief="raised", justify='center').\
            place(x=335, y=45, width=150, height=30)


def window_deleted(root):
    print('Окно закрыто')
    root.quit()


def start_spider():
    os.system('scrapy crawl tst')
    # pass

def main():
    # root.title('upwork.com')
    root = tk.Tk()
    root.geometry('500x350-10-50')
    root.protocol('WM_DELETE_WINDOW', window_deleted(root=root))  # обработчик закрытия окна
    root.resizable(False, False)  # Горизонталь, Вертикаль

    app = WinUpwork(root)
    with open(file=FILE_RESULT, mode='r') as res_file:
        # head = [next(res_file) for x in range(6)]
        for line in res_file.readlines():
            j_dict = json.loads(line)
            text_butt = str(j_dict.get('name_project')) + ' / ' + str(j_dict.get('level')) + ' / ' + str(j_dict.get('price'))
            app.create_but(text=text_butt)

    root.mainloop()


if __name__ == "__main__":
    print('\t~~~ GUI запущена основным скриптом ~~~')

    main()