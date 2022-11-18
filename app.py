#! /bin/python3
import tkinter as tk
import sqlite3 as sq
import os

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

# Phần liệt kê môn học của lớp đang chọn
        self.lietKe = tk.Frame(self.masterFrame)
        tk.Label(self.lietKe, text="Môn học").grid(column=1, row=0)
        self.lbMon = tk.Listbox(self.lietKe, width=27)
        self.lbMon.grid(column=1, row=1)

        self.inputSet = tk.Frame(self.lietKe)
        tk.Label(self.inputSet, text="Tên môn - GV").grid(column=0, row=0)
        inputMon = tk.Entry(self.inputSet, width=15).grid(column=0, row=1)

        tk.Label(self.inputSet, text="Số tiết/tuần").grid(column=1, row=0)
        soTiet = tk.Scale(self.inputSet, from_=1, to=10, orient=tk.HORIZONTAL, showvalue=2, tickinterval=2, resolution=1)
        soTiet.grid(column=1, row=1)
        self.inputSet.grid(column=1, row=2)


# --------------------------------------

# Phần liệt kê lớp đã tạo
        tk.Label(self.lietKe, text="Liệt kê lớp").grid(column=0, row=0)
        self.lbLop = tk.Listbox(self.lietKe)
        self.lbLop.grid(column=0, row=1)

        # Nút xoá và chỉnh sửa bảng môn học cho lớp đang chọn
        self.buttons = tk.Frame(self.lietKe)
        tk.Button(self.buttons, text="Xoá", command=self.deleteLop).pack(side=tk.RIGHT)
        tk.Button(self.buttons, text="Xem").pack(side=tk.LEFT)
        self.buttons.grid(column=0, row=2)
        # ---------------------------------------------------

        self.lietKe.pack(side=tk.RIGHT)

        # Đọc danh sách lớp từ CSDL
        currentLop = self.listLop()
        for lop in currentLop:
            value = lop[0]
            self.insert(value)
        # ---------------------------

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
    def insert(self, value = None, fromDB = False):
        if value is None:
            value = self.inputLop.get()

        # (Chỉ tạo khi tên không bị trùng)
        if len(value) > 0 and value not in self.lbLop.get(0, tk.END):
            self.lbLop.insert('end', value)

        if fromDB is False:
            self.saveLop(value)
    # -------------------------

    # Xoá lớp
    def deleteLop(self):
        lopPos = self.lbLop.curselection()
        lop = self.lbLop.get(lopPos)

        self.runQuery("DROP TABLE \"{}\"".format(lop))
        self.lbLop.delete(lopPos)
    # ------------------------

    # Lưu lớp vào CSDL
    def saveLop(self, lop):
        self.runQuery("CREATE TABLE IF NOT EXISTS \"{}\" (mon VARCHAR(30), soTiet INT)".format(lop))
    # ------------------------

    # Cập nhật bảng môn dựa theo lớp
#    def updateMon(self):


    # ------------------------------

    # Liệt kê các bảng đang tồn tại trong CSDL
    def listLop(self):
        listLopQuery = "SELECT name FROM sqlite_master"
        listed = self.runQuery(listLopQuery, receive=True)

        return listed
    # ------------------------


    # "function" để giao tiếp với CSDL
    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sq.connect("TKB.db")
        cursor = conn.cursor()

        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()
    # -------------------------------

# ---------

if __name__ == "__main__":
    tkb = TKB()
    tkb.mainloop()
