#! /bin/python3
import tkinter as tk
import sqlite3 as sq

class TKB(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("TKB-12A1")

        self.masterFrame = tk.Frame(self)
        self.slaveFrame = tk.Frame(self.masterFrame)

# Phần tên và nút thoát
        self.intro = tk.Frame(self.slaveFrame)
        tk.Label(self.intro, text="TKB-12A1").grid(column=0, row=0)
        tk.Button(self.intro, text="Thoát", command=self.destroy).grid(column=1, row=0)
        self.intro.pack()
# --------------------

# Phần liệt kê lớp đã tạo
        self.lietKe = tk.Frame(self.masterFrame)
        tk.Label(self.lietKe, text="Các lớp đã tạo").pack(side=tk.TOP)
        self.lb = tk.Listbox(self.lietKe)
        self.lb.pack(side=tk.TOP)
    # Nút xoá và chỉnh sửa bảng môn học cho lớp đang chọn
        tk.Button(self.lietKe, text="Xoá", command=self.delete).pack(side=tk.RIGHT)
        tk.Button(self.lietKe, text="Xem").pack(side=tk.LEFT)
    # ---------------------------------------------------
        self.lietKe.pack(side=tk.RIGHT)
# -----------------------

# Phần tạo lớp mới
        self.lopHoc = tk.Frame(self.slaveFrame)
        tk.Label(self.lopHoc, text="Tạo lớp:").grid(column=0, row=0)
        self.inputLop = tk.Entry(self.lopHoc, width=10)
        self.inputLop.grid(column=1, row=0)
        tk.Button(self.lopHoc, text="Tạo", command=self.insert).grid(column=2, row=0)
        self.lopHoc.pack()
# ---------------

        self.slaveFrame.pack(side=tk.LEFT)
        self.masterFrame.pack()

# Functions
    # Tạo lớp
    # (Chỉ tạo khi tên không bị trùng)
    def insert(self):
        value = self.inputLop.get()

        if len(value) > 0 and value not in self.lb.get(0, tk.END):
            self.lb.insert('end', value)

    # Xoá lớp
    def delete(self):
        self.lb.delete(self.lb.curselection())
# ---------

if __name__ == "__main__":
    tkb = TKB()
    tkb.mainloop()
