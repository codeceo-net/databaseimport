# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# 主页
import base64
import datetime
import os
import platform
import sqlite3
import tkinter
import tkinter as tk  # 装载tkinter模块,用于Python3
from tkinter import *  # 装载tkinter.ttk模块,用于Python3
import subprocess
import threading
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import time
from turtle import circle

import openpyxl
import pandas
import pandas as pd
from configobj import ConfigObj
from utils.icon import img
from utils.newEntry import newEntry


class MainFrame:
    def __init__(self):
        self.win = tk.Tk()  # 创建窗口对象
        self.win.title(string='sqlite import')  # 设置窗口标题
        self.win.resizable(False, False)  # 禁用窗口缩放
        # self.root.geometry('800x600+200+200')
        self.init_position(800, 420)
        self.win.update_idletasks()  #
        # self.root.iconbitmap('icon.ico')
        # 使用icon.py设置图标，兼容pyinstaller打包
        platformName = platform.platform().lower()
        #window平台
        if "win" in platformName:
            tmp = open("tmp.ico", "wb+")
            tmp.write(base64.b64decode(img))
            tmp.close()
            self.win.iconbitmap("tmp.ico")
            os.remove("tmp.ico")

        # 导入主界面
        self.testMain()

    def testMain(self):

        frame = tk.Frame(self.win, width=780, height=420)  # 把frame放在canvas里
        # frame.configure(background="#ffffff")
        # frame.place(width=780, height=600)  # frame的长宽，和canvas差不多的
        frame.pack(side="top", fill=tk.BOTH)

        # 基础操作
        frame_left = tk.LabelFrame(frame, text="基础操作", labelanchor="nw")
        # frame_left.configure(background="#ffffff",fg="#333333")
        frame_left.place(x=10, y=10, width=778, height=400)
        #每列宽度一样
        for i in range(4):
            frame_left.columnconfigure(i,weight=1)

        # sqlite路径
        labelEvent = Label(frame_left, text='sqlite路径：')
        # labelEvent.configure(background="#ffffff",fg="#333333")
        # east E 东/右   west W 西/左   south S 南/下   north N 北/上
        labelEvent.grid(row=1, column=0, sticky=W, padx=10, pady=20)
        # self.entryAdbPath = tk.Entry(frame_left, width=30)
        self.entryAdbPath = newEntry(frame_left, "请导入sqlite地址")
        self.entryAdbPath.configure(
            # relief=RIDGE 边框样式
            # justify  LEFT, RIGHT, CENTER 多行显示效果
            # fg="#333333", #文本颜色
            # bg="#cccccc", #背景颜色
            # bd=1, #边框大小
            # selectforeground="#333333", #选择时候文字颜色
            # selectborderwidth=1 #选择时边框宽度
        )
        # self.entryAdbPath.bind("<Button-1>", self.get_adb_path)
        self.entryAdbPath.grid(row=1, column=1, sticky=W, padx=20)

        # 选择sqlite路径
        btnselectSqlite = Button(frame_left, text='选择', command=self.getSliqtePath, font="Arial, 16", anchor="c",
                                 background="#ffffff")
        btnselectSqlite.grid(row=1, column=2, sticky=W, padx=10, pady=20)

        # 清空sqlite表
        btnselectSqlite = Button(frame_left, text='清空sqlite表', command=self.clearSqliteTbale, font="Arial, 16",
                                 anchor="c",
                                 background="#ffffff")
        btnselectSqlite.grid(row=1, column=3, sticky=W, padx=10, pady=20)

        labelTableType = Label(frame_left, text='选择导入的表格数据类型：一体机2.0数据字典表.xlsx 和 一体机2.0数据库设计表.xlsx')
        labelTableType.grid(row=2, column=0, columnspan=4, sticky=W, padx=10, pady=20)

        labelTablePath = Label(frame_left, text='表格地址：')
        labelTablePath.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entrytablePath = newEntry(frame_left, "请导入excel表格地址")
        self.entrytablePath.grid(row=3, column=1, sticky=W, padx=10, pady=20)
        # 选择excel表格路径
        btnselectSqlite = Button(frame_left, text='选择表格', command=self.getExcelTbalePath, font="Arial, 16", anchor="c",
                                 background="#ffffff")
        btnselectSqlite.grid(row=3, column=2, sticky=W, padx=10, pady=20)

        # 导入数据库
        btnselectSqliteFrame = Frame(frame_left)
        btnselectSqliteFrame.grid(row=4, column=0, columnspan=4, sticky=(N, S, E, W), padx=10, pady=50)

        btnselectSqlite = Button(btnselectSqliteFrame, text='开始导入到sqlite数据库', command=self.startSqliteTbale, font="Arial, 16",
                                 anchor="c",
                                 background="#ffffff")
        btnselectSqlite.pack()

        version = Label(frame_left, text='Copyright©2022-lion', foreground="#eeeeee")
        version.grid(row=5, column=0, columnspan=4, sticky=(N, S, E, W), padx=10, pady=10)

    # 选择表格的路径
    def getExcelTbalePath(self):
        result = filedialog.askopenfile(filetypes=[("excel表格", ".xlsx")])
        if result:
            self.entrytablePath.delete(0, END)
            self.entrytablePath.insert(0, result.name)

    # 选择sqlite数据库路径
    def getSliqtePath(self):
        result = filedialog.askopenfile()
        if result:
            self.entryAdbPath.delete(0, END)
            self.entryAdbPath.insert(0, result.name)

    # 清空sqlite表
    def clearSqliteTbale(self):
        sqlitePath = self.entryAdbPath.get().strip()
        if sqlitePath == "请导入sqlite地址" or sqlitePath == "":
            messagebox.showwarning("提示", "请选择sqlite数据库")
            return
        conn = sqlite3.connect(sqlitePath)  # 建立一个基于硬盘的数据库实例
        # cursor = conn.execute("drop table if exists Aio_Dict")
        # 查询所有的表
        cursor = conn.execute("select name from sqlite_master where type = 'table' order by name;")
        for row in cursor.fetchall():
            tableName = row[0]
            #print( tableName )
            if "sqlite_sequence" == tableName or "sqlite_master" == tableName:
                continue
            _cursor = conn.execute("drop table if exists " + tableName)
            _cursor.close()
        cursor.close()
        conn.close()
        messagebox.showwarning("提示", "清空sqlite数据库表成功")

    # 开始导入解析excel数据到数据库表
    def startSqliteTbale(self):
        sqlitePath = self.entryAdbPath.get().strip()
        if sqlitePath == "请导入sqlite地址" or sqlitePath == "":
            messagebox.showwarning("提示", "请选择sqlite数据库")
            return
        tablePath = self.entrytablePath.get().strip()
        if tablePath == "请导入excel表格地址" or tablePath == "":
            messagebox.showwarning("提示", "请选择excel表格地址")
            return
        # getdata = pd.read_excel(tablePath,header=None) #sheet_name不设置默认第一个表格
        data = pd.read_excel(tablePath,
                             header=None,
                             converters={0: str},
                             na_values='未知')
        if data is None:
            messagebox.showwarning("提示", "没有读取到可用数据")
            return
        infodata = pandas.DataFrame(data).values
        tagTitle = infodata[0][0]
        # 创建表的判断
        if "一体机2.0数据字典表" in tagTitle:
            self.processDict(infodata)
            pass
        elif "一体机2.0数据库设计表" in tagTitle:
            self.processTables(infodata)
            pass
        else:
            messagebox.showwarning("提示", "导入的excel表格式不正确")
            return

    # 处理数据库表
    def processTables(self, infodata):
        sqlitePath = self.entryAdbPath.get().strip()
        conn = sqlite3.connect(sqlitePath)  # 建立一个基于硬盘的数据库实例
        length = len(infodata)
        currentTableName = ''
        dict = {}
        # 转成数组
        for i in range(0, length):  # 循环获取每行数据
            # 获取表名称
            if "table_" in infodata[i][0]:
                currentTableNames = infodata[i][0].split("@")
                if len(currentTableNames) > 1:
                    currentTableName = str(currentTableNames[1]).strip()
                    dict[currentTableName] = []
                    continue
            # 如果没有表名 继续轮询
            if currentTableName is None or currentTableName == "":
                continue
            #存储数据
            dict[currentTableName].append( tuple( infodata[i]) )

        #遍历字典
        dictSql = {}
        for table_name,table_field in dict.items():
            #删除表
            cursor = conn.execute("drop table if exists "+table_name.replace(" ","").strip())
            cursor.close()

            #组装创建表的数据
            createSql = "create table if not exists "+(table_name.replace(" ","").strip())
            createSql += "("

            createSql += "Id INTEGER PRIMARY KEY autoincrement NOT NULL,"

            for fields in table_field:
                createSql += str(fields[1]).replace(" ","") + " TEXT,"

            createSql = createSql.strip(",")

            createSql += ");"

            dictSql[table_name] = createSql

        #创建表
        for table_name,createSql in  dictSql.items():
            cursor = conn.execute(createSql)
            cursor.close()

        #关闭数据库连接
        conn.close()
        messagebox.showwarning("提示", "导入数据库数据成功")

    #处理字典
    def processDict(self,infodata):
        #新建数据库表
        sqlitePath = self.entryAdbPath.get().strip()
        conn = sqlite3.connect(sqlitePath)  # 建立一个基于硬盘的数据库实例
        cursor = conn.execute("drop table if exists aio_dict")
        cursor.close()
        #创建表
        createSql = '''create table if not exists  aio_dict
        (
        Ad_Id INTEGER  primary key autoincrement NOT NULL,
        Table_Name TEXT,
        Field_Name TEXT,
        Field_Des TEXT,
        Field_Value Text,
        Create_Time TEXT
        );'''
        cursor = conn.execute( createSql )
        cursor.close()
        # 转成数组向数据库插入数据
        currentTableName = ''
        length = len(infodata)
        Create_Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(0, length):  # 循环获取每行数据
            #结束
            if "@end@" in infodata[i][0]:
                break
            #获取表名称
            if "table_" in infodata[i][0]:
                currentTableNames = infodata[i][0].split("@")
                if len( currentTableNames ) > 1:
                    currentTableName = str( currentTableNames[1] ).strip()
                    continue
            #如果没有表名 继续轮询
            if currentTableName is None or currentTableName == "":
                continue
            #插入数据库
            if infodata[i][2] is not None and str(infodata[i][2]) != "nan":
                items = infodata[i][2].split("@")
                jsonStr = "["
                for item in items:
                    values = str(item).strip().split(" ")
                    if values is not None and len( values )>1:
                        jsonStrItem = "{'key':'" + str(values[0]).strip() + "','value':'" + str(values[1].replace("\"","")).strip() + "'},"
                        jsonStr += jsonStrItem
                jsonStr = jsonStr.strip(",")
                jsonStr += "]"
                sql = '''INSERT INTO Aio_Dict (Table_Name, Field_Name, Field_Des,Field_Value,Create_Time) VALUES ("{}","{}","{}","{}","{}");'''
                sql = sql.format(currentTableName,infodata[i][0],infodata[i][1],jsonStr,Create_Time)
                cursor = conn.execute(sql)
                conn.commit()
                #print(sql)
        cursor.close()
        #关闭数据库连接
        conn.close()
        messagebox.showwarning("提示", "导入字段数据成功")

    # 初始化窗口大小，居中显示
    def init_position(self, curWidth='', curHight=''):
        '''
              设置窗口大小，并居中显示
              :param root:主窗体实例
              :param curWidth:窗口宽度，非必填，默认200
              :param curHight:窗口高度，非必填，默认200
              :return:无
            '''
        if not curWidth:
            '''获取窗口宽度，默认200'''
            curWidth = self.win.winfo_screenwidth()
        if not curHight:
            '''获取窗口高度，默认200'''
            curHight = self.win.winfo_screenheight()
        # print(curWidth, curHight)
        # 获取屏幕宽度和高度
        # scn_w, scn_h = self.win.maxsize()
        # 以像素为单位
        scn_w = self.win.winfo_screenwidth()
        scn_h = self.win.winfo_screenheight()
        # 以毫米为单位
        # length_2 = self.win.winfo_screenmmheight()
        # width_2 = self.win.winfo_screenmmwidth()
        # 计算中心坐标
        cen_x = (scn_w - curWidth) / 2
        cen_y = (scn_h - curHight) / 2
        # 设置窗口初始大小和位置
        size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
        self.win.geometry(f'{size_xy}')

    def mainloop(self):
        # 进入消息循环
        self.win.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = MainFrame()
    app.mainloop()
