#! /home/codeer/anaconda3/bin/python3.9
import tkinter as tk
import sqlite3 as sq
import os
from tkbGen import tkbGen
from xlGen import xlGen

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
        self.lbMon = tk.Listbox(self.lietKe, width=11, height=12, yscrollcommand=self.yscroll1)
        self.lbMon.grid(column=1, row=1)

        tk.Label(self.lietKe, text="Giáo viên").grid(column=2, row=0)
        self.lbGV = tk.Listbox(self.lietKe, width=11, height=12, yscrollcommand=self.yscroll2)
        self.lbGV.grid(column=2, row=1)

        tk.Label(self.lietKe, text="Tiết/ tuần").grid(column=3, row=0)
        self.lbSoTiet = tk.Listbox(self.lietKe, width=7, height=12, yscrollcommand=self.yscroll3)
        self.lbSoTiet.grid(column=3, row=1)

        self.monButtons = tk.Frame(self.lietKe)
        tk.Button(self.monButtons, text="Xoá môn", command=self.deleteMon).pack(side=tk.RIGHT)
        tk.Button(self.monButtons, text="Sửa môn", command=self.replaceMon).pack(side=tk.LEFT)
        self.monButtons.grid(column=1, row=2, columnspan=3)
# --------------------------------------

# Phần liệt kê lớp đã tạo
        tk.Label(self.lietKe, text="Liệt kê lớp").grid(column=0, row=0)
        self.lbLop = tk.Listbox(self.lietKe, height=12)
        self.lbLop.grid(column=0, row=1)

        # Nút xoá và chỉnh sửa bảng môn học cho lớp đang chọn
        self.lopButtons = tk.Frame(self.lietKe)
        tk.Button(self.lopButtons, text="Xoá lớp", command=self.deleteLop).pack(side=tk.RIGHT)
        tk.Button(self.lopButtons, text="Xem", command=self.xem).pack(side=tk.LEFT)
        self.lopButtons.grid(column=0, row=2)
        # ---------------------------------------------------

        self.lietKe.pack(side=tk.RIGHT)
# -----------------------

        # Phần tạo lớp mới
        self.lopHoc = tk.Frame(self.slaveFrame)
        tk.Label(self.lopHoc, text="Lớp:").grid(column=0, row=0)
        self.inputLop = tk.Entry(self.lopHoc, width=10)
        self.inputLop.grid(column=1, row=0)
        tk.Button(self.lopHoc, text="Tạo", command=self.insertLop, height=7, width=1).grid(column=2, row=0, rowspan=4)
        self.lopHoc.pack()
        # ---------------

# Phần tạo môn mới
        tk.Label(self.lopHoc, text="Tên môn:").grid(column=0, row=1)
        self.inputMon = tk.Entry(self.lopHoc, width=10)
        self.inputMon.grid(column=1, row=1)

        tk.Label(self.lopHoc, text="Tên GV:").grid(column=0, row=2)
        self.inputGV = tk.Entry(self.lopHoc, width=10)
        self.inputGV.grid(column=1, row=2)

        self.soTietDC = tk.IntVar()
        self.soTiet = tk.Scale(self.lopHoc, from_=1, to=12, label="Số tiết/tuần", length=130, orient=tk.HORIZONTAL, showvalue=1, resolution=1, variable=self.soTietDC)
        self.soTietDC.set(2)
        self.soTiet.grid(column=0, row=3, columnspan=2)
# ---------------

        tk.Button(self.lopHoc, text="Tạo TKB", command=self.createTKB, width=15, height=1).grid(column=0, row=4, columnspan=3)

        self.slaveFrame.pack(side=tk.LEFT)
        self.masterFrame.pack()

        # Đọc danh sách lớp từ CSDL
        currentLop = self.listLop()
        for lop in currentLop:
            value = lop[0]
            self.insertLop(valueInput=value)
        # ---------------------------

        # Keybindings
        self.inputLop.bind("<Return>", self.insertLop)
        self.inputMon.bind("<Return>", self.insertLop)
        self.inputGV.bind("<Return>", self.insertLop)
        self.lbLop.bind("<Double-Button-1>", self.xem)
        self.lbLop.bind("<BackSpace>", self.deleteLop)
        # -----------

# Functions
    # Tạo lớp
    def insertLop(self, _event=None, valueInput = None, fromDB = False):
        value = self.inputLop.get() if valueInput is None else valueInput
        self.activeTable = value

        if len(value) <= 0: return
        
        if fromDB is False:
            self.saveLop(value)

        # (Chỉ tạo khi tên không bị trùng)
        if value not in self.lbLop.get(0, tk.END):
            self.lbLop.insert('end', value)

        self.insertMon()
        # -------------------------------

    # -------------------------

    def insertMon(self, monValueInput=None, gvValueInput=None, soTietValueInput=None, fromDB=False):
        monValue = self.inputMon.get() if monValueInput is None else monValueInput
        gvValue = self.inputGV.get() if gvValueInput is None else gvValueInput
        soTietValue = self.soTietDC.get() if soTietValueInput is None else soTietValueInput

        if len(monValue) > 0 and len(gvValue) > 0:
            if monValue not in self.lbMon.get(0, tk.END) or gvValue not in self.lbGV.get(0, tk.END):
                self.lbMon.insert('end', monValue)
                self.lbGV.insert('end', gvValue)
                self.lbSoTiet.insert('end', soTietValue)

                if fromDB is False:
                    self.saveMon(monValue, gvValue, soTietValue)

    # Xoá lớp
    def deleteLop(self, _event=None):
        lopPos = self.lbLop.curselection()
        lop = self.lbLop.get(lopPos)

        self.runQuery("DROP TABLE \"{}\"".format(lop))
        self.lbLop.delete(lopPos)
    # ------------------------

    # Lưu lớp vào CSDL
    def saveLop(self, lop):
        self.runQuery("CREATE TABLE IF NOT EXISTS \"{}\" (mon VARCHAR(30), gv VARCHAR(30), soTiet INT)".format(lop))
    # ------------------------

    def saveMon(self, mon, gv, soTiet):
        self.runQuery("INSERT INTO \"{}\" VALUES (\"{}\", \"{}\", {})".format(self.activeTable, mon, gv, soTiet))

    # Xoá môn học cùng các thông tin liên quan
    def deleteMon(self):
        monPos = self.lbMon.curselection()
        mon = self.lbMon.get(monPos)
        gv = self.lbGV.get(monPos)

        self.runQuery("DELETE FROM \"{}\" WHERE mon='{}' AND gv='{}'".format(self.activeTable, mon, gv))
        self.lbSoTiet.delete(monPos)
        self.lbGV.delete(monPos)
        self.lbMon.delete(monPos)
    # ---------------------------------------

    def deleteAllMon(self):
        self.lbMon.delete(0, tk.END)
        self.lbGV.delete(0, tk.END)
        self.lbSoTiet.delete(0, tk.END)

    def replaceMon(self):
        monPos = self.lbMon.curselection()

        mon = self.lbMon.get(monPos)
        self.inputMon.delete(0, tk.END)
        self.inputMon.insert(0, mon)

        gv = self.lbGV.get(monPos)
        self.inputGV.delete(0, tk.END)
        self.inputGV.insert(0, gv)

        soTiet = self.lbSoTiet.get(monPos)
        self.soTietDC.set(soTiet)

        self.deleteMon()
        

    # Cập nhật bảng môn học khi ấn nút "Xem"
    def xem(self, _event=None, lopInput=None, fromDB=False):
        lopPos = self.lbLop.curselection()
        lop = self.lbLop.get(lopPos) if lopInput is None else lopInput
        self.activeTable = lop

        if self.inputLop.get() != lop:
            self.inputLop.delete(0, tk.END)
            self.inputLop.insert(0, lop)

        self.deleteAllMon()

        for mons in self.loadMon():
            self.insertMon(mons[0], mons[1], mons[2], fromDB=True)
    # -------------------------------------
        
    # Liệt kê các bảng đang tồn tại trong CSDL
    def listLop(self):
        listLopQuery = "SELECT name FROM sqlite_master"
        listed = self.runQuery(listLopQuery, receive=True)

        return listed
    # ------------------------

    def loadMon(self, lop=None):
        if lop is None:
            lop = self.activeTable
        loadMonQuery = "SELECT * FROM \"{}\"".format(lop)
        loaded = self.runQuery(loadMonQuery, receive=True)

        return loaded

    # Giữ môn và số tiết của môn ở cùng một dòng
    def yscroll1(self, *args):
        if self.lbMon.yview() != self.lbGV.yview() or self.lbMon.yview() != self.lbSoTiet.yview():
            self.lbSoTiet.yview_moveto(args[0])

    def yscroll2(self, *args):
        if self.lbGV.yview() != self.lbMon.yview() or self.lbGV.yview() != self.lbSoTiet.yview():
            self.lbMon.yview_moveto(args[0])

    def yscroll3(self, *args):
        if self.lbSoTiet.yview() != self.lbMon.yview() or self.lbSoTiet.yview() != self.lbGV.yview():
            self.lbMon.yview_moveto(args[0])
    # -----------------------------------------

    @staticmethod
    def createTKB():
        tkbGenerator = tkbGen()
        xlGenerator = xlGen()

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
