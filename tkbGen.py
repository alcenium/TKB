#! /home/codeer/anaconda3/bin/python3
import random
import sqlite3 as sq
import json
import pdb

class tkbGen:
    def __init__(self):
        self.thuHai, self.thuBa, self.thuTu, self.thuNam, self.thuSau, self.thuBay = {}, {}, {}, {}, {}, {}
        self.dic = self.dbToDic()

        self.taoTKB()
        final = {'Thu hai':self.thuHai, 'Thu ba':self.thuBa, 'Thu tu':self.thuTu, 'Thu nam':self.thuNam, 'Thu sau':self.thuSau, 'Thu bay':self.thuBay}

        with open("Test.json", 'w') as f:
            json.dump(final, f, indent=4)
        f.close()

        
    def dbToDic(self):
        dic = {}
        for clas in self.runAppQuery("SELECT name FROM sqlite_master", receive=True):
            classValues = self.runAppQuery("SELECT * FROM \"{}\"".format(clas[0]), receive=True)
            dicT = {f'{clas[0]}':list(list(values) for values in classValues)}
            dic.update(dicT)
        return dic
    
    def raendom(self, lop, mon, isThuHai=False, isThuBay=False):
        inserted = []
        END = 4 if isThuBay else 5
        START = 1 if isThuHai else 0
            
        if isThuHai:
            inserted.append(("Chao co", "GVCN"))

        for i in range(START, END):
            monDC = []
            for j in mon:
                if j[1] not in self.temp[i] and j[2] > 0:
                    monDC.append(j)
                    
            rand = random.choice(monDC)
            self.dic[lop][self.dic[lop].index(rand)][2] -1

            inserted.append((rand[0], rand[1]))
            self.temp[i].append(rand[1])

        if isThuBay:
            inserted.append(("Sinh hoat", "GVCN"))
        return inserted

    def taoTKB(self):
        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon, isThuHai=True)
            self.thuHai.update({f"{lop}":listed})

        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon)
            self.thuBa.update({f"{lop}":listed})

        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon)
            self.thuTu.update({f"{lop}":listed})

        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon)
            self.thuNam.update({f"{lop}":listed})

        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon)
            self.thuSau.update({f"{lop}":listed})

        self.temp = [[], [], [], [], []]
        for lop, mon in self.dic.items():
            listed = self.raendom(lop, mon, isThuBay=True)
            self.thuBay.update({f"{lop}":listed})

    @staticmethod
    def runAppQuery(sql, data=None, receive=False):
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

if __name__ == "__main__":
    tk1 = tkbGen()
