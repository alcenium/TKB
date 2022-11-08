#! /bin/python3
import tkinter as tk

root = tk.Tk()

master_frame1 = tk.Frame(root)

frame = tk.Frame(master_frame1)
tk.Label(frame, text="<Tên ứng dụng>").grid(column=0, row=0)
tk.Button(frame, text="Thoát", command=root.destroy).grid(column=1, row=0)

tk.Label(frame, text="Lớp:").grid(column=0, row=1)
tk.Entry(frame).grid(column=1, row=1)
tk.Label(frame, text="Môn học:").grid(column=0, row=2)
tk.Entry(frame).grid(column=1, row=2)

frame.grid(column=0, row=0)

second_frame = tk.Frame(master_frame1)
tk.Button(second_frame, text="Tạo lớp").grid(column=0, row=1)
tk.Button(second_frame, text="Tạo môn học").grid(column=1, row=1)

second_frame.grid(column=0, row=1)
master_frame1.grid(column=0, row=0)

master_frame2 = tk.Frame(root)

ten_lop = tk.Label(master_frame2, text="Các lớp đã tạo").pack(side=tk.TOP)
lb_lop = tk.Listbox(master_frame2).pack(side=tk.TOP)
xoa_lop = tk.Button(master_frame2, text="Xoá").pack(side=tk.LEFT)
xem_lop = tk.Button(master_frame2, text="Xem").pack(side=tk.LEFT)
master_frame2.grid(column=1, row=0)

root.mainloop()
