#-*- coding:utf-8 -*-
'''
创建一个数据表
学生20人（学号、姓名、性别、年龄、电话、email、所属班级）课程3个（课程ID、课程名称、任课教师）
班级2个（班级名称、所属院系）成绩表（学号、课程ID1、分数1、GPA1,课程ID2、分数2、GPA2,课程ID3、分数3、GPA3）
可进行数据的 插入、删除、查找、算总成绩
学生姓名信息的导入
成绩的导入 导出（csv?）
按钮导入文件（交互界面）
输入有效性检查（正则表达式）电话号码？email？长度？
Python版本: Python 3.7.2
'''
import sqlite3
import re
#import csv
from tkinter import *
from tkinter import Label    #?????需重新导入Label
from tkinter.filedialog import askopenfilename        # get standard dialogs

#创建学生数据库及相关表
db = []             #统计创建的不同的数据库
def creatTable():
    up  = Toplevel()
    up.title('新建学生数据库')
    Label(up,text='数据库名称').grid(row=0,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent =Entry(up,width = 30)
    ent.insert(END,'StuManageDatabase')         #默认的database名称
    ent.grid(row=0,column=1,sticky=W+E+N+S, padx=2, pady=2)

    def eget(ent):
        dire = ent.get()
        try:
            conn = sqlite3.connect('{0}.db'.format(dire))
            tableStu = '''CREATE TABLE Student
               (StuID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               SEX            TEXT,
               AGE            TEXT,
               TEL            TEXT,
               eMAIL        TEXT,
               ClASS        TEXT);'''
            tableCourse ='''CREATE TABLE Course
                (COURSEID INT PRIMARY KEY   NOT NULL,
                COURSENAME    TEXT,
                TEACHER       TEXT);
                '''
            tableClass ='''CREATE TABLE Class
                (CLASS TEXT PRIMARY KEY   NOT NULL,
                DEPARTMENT    TEXT    );
                '''
            tableScore ='''CREATE TABLE Score
                (StuID      INT PRIMARY KEY   NOT NULL,
                COURSEID1    INT,
                SCORE1      TEXT,
                GPA1        INT,   
                COURSEID2    INT,
                SCORE2      INT,
                GPA2        TEXT,   
                COURSEID3    INT,
                SCORE3      INT,
                GPA3        TEXT   );
                '''

            cur = conn.cursor()
            cur.execute(tableStu)
            cur.execute(tableCourse)
            cur.execute(tableClass)
            cur.execute(tableScore)
            conn.commit()
            conn.close()

            db.append(dire) 
        except:
            upup = Toplevel(up)
            Label(upup,text ='该数据库已存在相关表，无须重复创建').grid(row=0,column=0,sticky=W+E+N+S, padx=2, pady=2)
            Button(upup,text='确定',command =upup.destroy).grid(row=1,column=0, padx=2, pady=2)

        else:
            upup = Toplevel(up)
            Label(upup,text ='创建成功').grid(row=0,column=0,sticky=W+E+N+S, padx=2, pady=2)
            Button(upup,text='确定',command =upup.destroy).grid(row=1,column=0, padx=2, pady=2)
  

    Button(up,text='确定',height = 1,width = 6,command =(lambda: eget(ent))).grid(row=1,column=0,sticky=W+S, padx=2, pady=2)
    Button(up,text='退出',height = 1,width = 6,command = up.destroy).grid(row=1,column=1,sticky=E+S, padx=2, pady=2)
    up.mainloop()

#插入学生数据
def insertStu(rb,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()
    ins = 'INSERT INTO Student values (?,?,?,?,?,?,?) ' #insert id name sex age tel email class    
    StuID =  ent[0].get()  #主键学号
    name = ent[1].get()
    sex = ent[2].get()
    age = ent[3].get()
    tel = ent[4].get()
    email = ent[5].get()
    cla = ent[6].get()
    lst = [int(StuID),name,sex,age,tel,email,cla]
    cur.execute(ins,lst)
    conn.commit()

#插入课程数据
def insertCourse(rb,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()

    ins = 'INSERT INTO Course values (?,?,?) ' #insert cid cname teacher    
    CID = ent[0].get()   #主键课程ID
    Cname = ent[1].get()
    T = ent[2].get()
    lst = [int(CID),Cname,T]
    cur.execute(ins,lst)
    conn.commit()

#插入班级数据
def insertClass(rb,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()

    ins = 'INSERT INTO Class values (?,?) ' #insert class department    
    Class = ent[0].get()   #主键班级名字
    Dep = ent[1].get()
    lst = [Class,Dep]
    cur.execute(ins,lst)
    conn.commit()

#插入成绩表数据
def insertScore(rb,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()

    lst=[]
    ins = 'INSERT INTO Score values (?,?,?,?,?,?,?,?,?,?) ' #insert     
    Stu = ent[0].get()    #主键学号
    lst.append(int(Stu))
    for i in (1,len(ent)):
        lst.append(int(ent[i].get()))
    cur.execute(ins,lst)
    conn.commit()     

#删除表数据
def delete(rb,table,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()

    key = ent.get()
    if table == 'Student':
        dele =" DELETE FROM {0} WHERE StuID like '%{1}%' ".format(table,key) #delete
    elif table =='Course':
        dele =" DELETE FROM {0} WHERE COURSENAME like '%{1}%' ".format(table,key)
    elif table =='Class':
        dele =" DELETE FROM {0} WHERE CLASS like '%{1}%' ".format(table,key)
    elif table =='Score':
        dele =" DELETE FROM {0} WHERE StuID like '%{1}%' ".format(table,key)
    cur.execute(dele)
    conn.commit()

#查询表数据(返回表中所有数据)
def search(rb,table,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()
    
    #key = ent
    if ent.get() is '': 
        sel  = "SELECT * FROM {0}".format(table)
    else:
        txt = ent.get()
        if table == 'Student':
            sel  = "SELECT * FROM {0} where StuID={1} ".format(table,txt)
        elif table == 'Course':
            sel = "SELECT * FROM {0} where COURSEID={1} ".format(table,txt)
        elif table == 'Class':
            sel = "SELECT * FROM {0} where CLASS={1} ".format(table,txt)
        elif table == 'Score':
            sel = "SELECT * FROM {0} where StuID={1} ".format(table,txt)
    cur.execute(sel)
    lst = cur.fetchall()

    worklist = []
    for record in lst:
        print(record)
        '''
        aaa = Stu.Stu(record[0],record[1],record[2],record[3],record[4],record[5],record[6])
        worklist.append(aaa)
        '''
    conn.commit()

#更新学生数据    
def update(rb,table,ent):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()
    ins = "UPDATE {} SET ".format(table)
    if table =='Student':
        lst = ['StuID','name','sex','age','tel','email','ClASS']
    elif table=='Course':
        lst = ['COURSEID','COURSENAME','TEACHER']
    elif table=='Class':
        lst = ['CLASS','DEPARTMENT']
    else:
        lst = ['StuID','COURSEID','SCORE','GPA']
    enttxt=[]
    for i in range(1,len(lst)):   #从lst第二个字段开始索引迭代 加入到sql语句中
        if ent[i].get()=='':      #若输入框输入内容为空白 则不对增加相应字段的sql语句 不进行更新
            continue
        else:
            ins=ins+lst[i]+'=?,'
            enttxt.append(ent[i].get())
    ins  = ins[:-1] #删除ins语句最后的的"，"号 以便与where拼接
    ins=ins+' WHERE '+lst[0]+'='+ent[0].get()
    #ins = 'UPDATE Student SET name=?,sex=?,age=?,tel=?,email=?,cla=? WHERE StuID = ?' #update data by StuID    
    cur.execute(ins,enttxt)

    conn.commit()


#算总成绩 平均成绩
def sumAvg(rb,num):
    conn = sqlite3.connect('{0}.db'.format(rb.dbs))
    cur = conn.cursor()

    for i in num:
        filed= "SCORE{0}" .format(repr(i))
        stat = "SELECT avg({0}) from Score".format(filed)
        cur.execute(stat)
        lst = cur.fetchone()
        print(f"课程{i}的平均成绩为",lst[0])
    conn.close()
'''
创建GUI窗口 主窗口上有四个表(学生表,课程表,班级表,成绩表)分别的管理按钮控件
单击按钮可打开Top窗口
每个Top窗口又含有 插入、更新、删除、查找 等功能的按钮控件
注意：插入和更新共用输入框 根据需要点击不同的按钮
当进行数据更新时 必须在第一个输入框进行输入 其他字段的输入根据需要输入
系统可自行判断更新的字段
每个Top窗口下方可以通过输入框输入进行操作的数据库 
'''

#创建路径框选择db    
class DB(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        Label(self,text = '设置输入您要进行操作的数据库（默认如下）').grid(row = 0)
        self.ent = Entry(self,width =20)
        self.ent.grid(row = 1,sticky=W)
        self.ent.insert(END,'StuManageDatabase')
        self.dbs = self.ent.get()
        Button(self,text = '确认路径',command = self.onPress).grid(row = 2,sticky=W)

    def onPress(self):
        self.dbs = self.ent.get()
        return self.dbs

#创建 通过读取文件的方式进行数据库操作的输入输出の类
class IO:
    def __init__(self,rb):
        self.conn = sqlite3.connect('{0}.db'.format(rb.dbs))
        self.cur = self.conn.cursor()
   
    def I(self,table):
        self.filename = askopenfilename()
        with open(self.filename,'r',encoding='utf-8') as fi:
            l1 = fi.readlines()
            del l1[0]
            l2=[]
            for i in l1:
                l2.append(i.strip().split())
            if table == 'Student':
                ins = "INSERT INTO Student values (?,?,?,?,?,?,?)"
            elif table == 'Course':
                ins = "INSERT INTO Course values (?,?,?)"
            elif table =='Class':
                ins = "INSERT INTO Class values (?,?) "
            elif table =='Score':
                ins ="INSERT INTO Score values (?,?,?,?,?,?,?,?,?,?)"                
            for i in range(len(l2)):
                    self.cur.execute(ins,l2[i])
            self.conn.commit()
    
    def O(self,table):
        top = Toplevel()
        Label(top,text ='请输入导出的csv文件名').grid(row=0,column=0,sticky=W+E+N+S, padx=2, pady=2)
        ent = Entry(top,width = 20)
        ent.grid(row=1,column=0,sticky=W+E+N+S, padx=2, pady=2)
        Button(top,text='确定',command = (lambda:destroy(ent,top))).grid(row=2,column=0, padx=2, pady=2)
        def destroy(ent,top):
            self.opname = ent.get()
            top.destroy()
            with open("{0}.csv".format(self.opname),'w') as fo:
                sq = "select * from {0} ".format(table)
                self.cur.execute(sq)
                lst = self.cur.fetchall()
                if table == 'Student':
                    fo.write('stuid,name,sex,age,tel,email,class\n')
                elif table == 'Course':
                    fo.write('courseid,coursename,teacher\n')
                elif table =='Class':
                    fo.write('class,department\n')
                elif table =='Score':
                    fo.write('stuid,courseid1,score1,gpa1,courseid2,score2,gpa2,courseid3,score3,gpa3\n')
                for i in lst:
                    nlst = []
                    # i is a tuple #exp: (1001,'数据结构与算法','李治洪' )
                    for item in i:
                        nlst.append(repr(item))
                    fo.write(','.join(nlst)+'\n')
                self.conn.commit()

#使用正则对部分输入字段进行判断
class reCheck:
    def __init__(self,root):
        self.root = root

    def toplevel(self,flags):
        upup = Toplevel(self.root)
        Label(upup,text =f'您的输入{flags}规范').grid(row=0,column=0,sticky=W+E+N+S, padx=2, pady=2)
        Button(upup,text='确定',command =upup.destroy).grid(row=1,column=0, padx=2, pady=2)

    def StuCheck(self,ent): #学生表对学号和邮箱进行判断
        self.StuID = ent[0].get()
        self.eMAIL = ent[5].get()
        res1 = re.match(r'^[0-9]{11}$',self.StuID)
        res2 = re.match(r"[A-Za-z0-9_]+@(?!\.)[A-Za-z0-9\.]+(com|org|edu|net|cn)|(null)$",self.eMAIL)
        if (res1 and res2) is not None:
            self.toplevel('符合')
        else:
            self.toplevel('不符合')

    def CourseCheck(self,ent):
        self.CourseID = ent[0].get()
        res = re.match(r'^[0-9]+$',self.CourseID)
        #print(res)
        if (res is not None):
            self.toplevel('符合')
        else:
            self.toplevel('不符合')

    def ScoreCheck(self,ent):
        self.can = []
        self.StuID = ent[0].get()
        self.can.append(ent[1].get())
        self.can.append(ent[2].get())
        self.can.append(ent[4].get())
        self.can.append(ent[5].get())
        self.can.append(ent[7].get())
        self.can.append(ent[8].get())
        res1 = re.match(r'^[0-9]{11}$',self.StuID)
        flag = True
        for item in self.can:
            res2 = re.match(r'^[0-9]+(\.)+[0-9]+$',item)
            if res2 is not None:
                        continue
            else:
                        flag = False
                        break
        if ((res1 is not None)\
            and (flag != True)):
            self.toplevel('符合')
        else:
            self.toplevel('不符合')


#学生表管理界面
def creat1():
    top1 = Toplevel(root)
    top1.title('学生表管理')
    rb = DB(top1)

    lb1 = Label(top1)
    lb1.config(text = '学生信息',bg='lightblue',width = 30)
    lb1.grid(row=0,column=0,rowspan=7,sticky=W+E+N+S, padx=2, pady=2)
    ent=[]
    #创建7个学生信息标签
    label = [('学号(11位)','darkgrey'),('姓名','lightgrey'),('性别','darkgrey'),('年龄','lightgrey'),('电话','darkgrey'),('email','lightgrey'),('班级','darkgrey')]
    i = 0
    for (tex, bg) in label:
        Label(top1,text = tex,bg=bg,width = 10).grid(row=i,column=1,sticky=W+E+N+S,padx=2, pady=2)
        entry = Entry(top1,width = 20)
        entry.grid(row = i,column=2)
        ent.append(entry)
        i = i+1
                        
    che = reCheck(top1)
    lb2 = Label(top1)
    lb2.config(text = '删除学生信息(by StuID)',bg='lightblue',width = 30)
    lb2.grid(row=7,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent2 = Entry(top1,width = 20)
    ent2.grid(row=7,column=1,columnspan=2,sticky = W+E+N+S,padx=2,pady=2)

    lb3 = Label(top1)
    lb3.config(text = '查找学生信息(默认查找所有信息)',bg='lightblue',width = 30)
    lb3.grid(row=8,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent3 = Entry(top1,width = 20)
    ent3.grid(row=8,column=1,columnspan=2,sticky = W+E+N+S,padx=2,pady=2)
###
    Button(top1,text = '插入(insert)学生数据',command = (lambda: insertStu(rb,ent)),width = 20).grid(row=0,column=3,rowspan=7,sticky=W+E+N+S, padx=2, pady=2)
    Button(top1,text = '更新(update)学生数据',command = (lambda: update(rb,'Student',ent)),width = 20).grid(row=0,column=4,rowspan=7,sticky=W+E+N+S, padx=2, pady=2)
    Button(top1,text = '输入验证（学号与Email）',command = (lambda: che.StuCheck(ent)),width = 20).grid(row=0,column=5,rowspan=7,sticky=W+E+N+S, padx=2, pady=2)
    Button(top1,text = '删除学生数据',command = (lambda: delete(rb,'Student',ent2))).grid(row=7,column=3,sticky=W+E+N+S,padx=2,pady=2)
    Button(top1,text = '查找学生数据(关键字：学号)',command = (lambda: search(rb,'Student',ent3))).grid(row=8,column=3,sticky=W+E+N+S,padx=2,pady=2)
    #qt = Button(top1,text = Quit,command = top1.destroy) 
    
    rb.grid(row=9,column=0,columnspan = 4,sticky=W+E+N+S, padx=2, pady=2)

#课程表管理界面
def creat2():
    top2 = Toplevel(root)
    top2.title('课程表管理')
    rb = DB(top2)

    lb11 = Label(top2)
    lb11.config(text='课程ID',bg='darkgrey')
    lb11.grid(row = 0,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent11 = Entry(top2,width=20)
    ent11.grid(row = 0,column = 1,sticky = W+E+N+S,padx=2,pady=2)

    lb12 = Label(top2)
    lb12.config(text='课程名称',bg='lightgrey')
    lb12.grid(row = 1,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent12 = Entry(top2,width=20)
    ent12.grid(row = 1,column = 1,sticky = W+E+N+S,padx=2,pady=2)

    lb13 = Label(top2)
    lb13.config(text='任课教师',bg='darkgrey')
    lb13.grid(row = 2,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent13 = Entry(top2,width=20)
    ent13.grid(row = 2,column = 1,sticky = W+E+N+S,padx=2,pady=2)

    ent = [ent11,ent12,ent13]
    che = reCheck(top2)
    Button(top2,text = '插入(insert)课程信息',command = (lambda: insertCourse(rb,ent))).grid(row=0,column=2,rowspan =3,sticky=W+E+N+S, padx=2, pady=2)
    Button(top2,text = '更新(update)课程信息',command = (lambda: update(rb,'Course',ent))).grid(row=0,column=3,rowspan =3,sticky=W+E+N+S, padx=2, pady=2)
    Button(top2,text = '输入验证（课程ID）',command = (lambda: che.CourseCheck(ent))).grid(row=0,column=4,rowspan =3,sticky=W+E+N+S, padx=2, pady=2)   
    
    lb2 = Label(top2)
    lb2.config(text='删除课程信息(by coursename)',bg='lightgrey')
    lb2.grid(row = 3,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent2 = Entry(top2,width=20)
    ent2.grid(row = 3,column = 1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top2,text = '删除课程信息',command = (lambda: delete(rb,'Course',ent2))).grid(row=3,column=2,sticky=W+E+N+S, padx=2, pady=2)

    lb3 = Label(top2)
    lb3.config(text = '查找课程信息(默认查找所有信息)',bg='darkgrey')
    lb3.grid(row=4,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent3 = Entry(top2,width = 20)
    ent3.grid(row=4,column=1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top2,text = '查找课程信息(关键字：课程ID)',command = (lambda: search(rb,'Course',ent3))).grid(row=4,column=2,sticky=W+E+N+S, padx=2, pady=2)

    rb.grid(row=5,column=0,columnspan = 3,sticky=W+E+N+S, padx=2, pady=2)
    dbs = rb.dbs

#班级表管理界面
def creat3():
    top3 = Toplevel(root)
    top3.title('班级表管理')
    rb = DB(top3)

    lb11 = Label(top3)
    lb11.config(text='班级名称',bg='darkgrey')
    lb11.grid(row = 0,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent11 = Entry(top3,width=20)
    ent11.grid(row = 0,column = 1,sticky = W+E+N+S,padx=2,pady=2)

    lb12 = Label(top3)
    lb12.config(text='所属院系',bg='lightgrey')
    lb12.grid(row = 1,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent12 = Entry(top3,width=20)
    ent12.grid(row = 1,column = 1,sticky = W+E+N+S,padx=2,pady=2)

    ent = [ent11,ent12]
    Button(top3,text = '插入(insert)班级信息',command = (lambda: insertClass(rb,ent))).grid(row=0,column=2,rowspan =2,sticky=W+E+N+S, padx=2, pady=2)
    Button(top3,text = '更新(update)班级信息',command = (lambda: update(rb,'Class',ent))).grid(row=0,column=3,rowspan =2,sticky=W+E+N+S, padx=2, pady=2)

    lb2 = Label(top3)
    lb2.config(text='删除班级信息(by CLASS)',bg='darkgrey')
    lb2.grid(row = 2,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent2 = Entry(top3,width=20)
    ent2.grid(row = 2,column = 1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top3,text = '删除班级信息',command = (lambda: delete(rb,'Class',ent2))).grid(row=2,column=2,sticky=W+E+N+S, padx=2, pady=2)

    lb3 = Label(top3)
    lb3.config(text = '查找班级信息(默认查找所有信息)',bg='lightgrey')
    lb3.grid(row=3,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent3 = Entry(top3,width = 20)
    ent3.grid(row=3,column=1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top3,text = '查找班级信息(关键字：班级名称)',command = (lambda: search(rb,'CLASS',ent3))).grid(row=3,column=2,sticky=W+E+N+S, padx=2, pady=2)

    rb.grid(row=4,column=0,columnspan = 3,sticky=W+E+N+S, padx=2, pady=2)
    dbs = rb.dbs

#创建成绩表管理
def creat4():
    top4 = Toplevel(root)
    top4.title('成绩表管理')
    rb = DB(top4)

    ent=[]
    label = [('学号(11位)','darkgrey'),('课程ID1','darkgrey'),('分数1','lightgrey'),('绩点1','lightgrey'),\
        ('课程ID2','darkgrey'),('分数2','lightgrey'),('绩点2','lightgrey'),\
        ('课程ID3','darkgrey'),('分数3','lightgrey'),('绩点3','lightgrey')]
    i = 0
    for (tex, bg) in label:
        Label(top4,text = tex,bg=bg,width = 20).grid(row=i,column=0,sticky=W+E+N+S,padx=2, pady=2)
        entry = Entry(top4,width=20)
        entry.grid(row = i,column = 1,sticky = W+E+N+S,padx=2,pady=2)
        ent.append(entry)
        i = i+1
    che = reCheck(top4)
    Button(top4,text = '插入(insert)成绩信息',command = (lambda: insertScore(rb,ent))).grid(row=0,column=2,rowspan =10,sticky=W+E+N+S, padx=2, pady=2)
    Button(top4,text = '更新(update)成绩信息',command = (lambda: update(rb,'Score',ent))).grid(row=0,column=3,rowspan =10,sticky=W+E+N+S, padx=2, pady=2)
    Button(top4,text = '输入验证（学生ID、课程ID、分数）',command = (lambda: che.ScoreCheck(ent))).grid(row=0,column=3,rowspan =10,sticky=W+E+N+S, padx=2, pady=2)    

    lb2 = Label(top4)
    lb2.config(text='删除成绩信息(by StuID)',bg='darkgrey')
    lb2.grid(row = 10,column = 0,sticky = W+E+N+S,padx=2,pady=2)
    ent2 = Entry(top4,width=20)
    ent2.grid(row = 10,column = 1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top4,text = '删除成绩信息',command = (lambda: delete(rb,'Score',ent2))).grid(row=10,column=2,sticky=W+E+N+S, padx=2, pady=2)

    lb3 = Label(top4)
    lb3.config(text = '查找成绩信息(默认查找所有信息)',bg='lightgrey')
    lb3.grid(row=11,column=0,sticky=W+E+N+S, padx=2, pady=2)
    ent3 = Entry(top4,width = 20)
    ent3.grid(row=11,column=1,sticky = W+E+N+S,padx=2,pady=2)
    Button(top4,text = '查找成绩信息(关键字：学号)',command = (lambda: search(rb,'Score',ent3))).grid(row=11,column=2,sticky=W+E+N+S, padx=2, pady=2)
    Button(top4,text = '计算平均分',command = (lambda: sumAvg(rb,(1,2,3)))).grid(row=11,column=3,sticky=W+E+N+S, padx=2, pady=2)

    rb.grid(row=12,column=0,columnspan = 3,sticky=W+E+N+S, padx=2, pady=2)

#文件导入输出界面
def creat5():
    top5 = Toplevel(root)
    top5.title('文件导入与输出界面')
    rb = DB(top5)
    interf = IO(rb)

    Button(top5,text = '选择学生txt文件导入学生表',command = (lambda: interf.I('Student'))).grid(row=0,column=0,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '选择课程txt文件导入课程表',command = (lambda: interf.I('Course'))).grid(row=1,column=0,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '选择班级txt文件导入班级表',command = (lambda: interf.I('Class'))).grid(row=2,column=0,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '选择成绩txt文件导入成绩表',command = (lambda: interf.I('Score'))).grid(row=3,column=0,sticky=W+E+N+S, padx=5, pady=5)
    
    Button(top5,text = '导出学生表（csv）',command = (lambda: interf.O('Student'))).grid(row=0,column=1,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '导出课程表（csv）',command = (lambda: interf.O('Course'))).grid(row=1,column=1,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '导出班级表（csv）',command = (lambda: interf.O('Class'))).grid(row=2,column=1,sticky=W+E+N+S, padx=5, pady=5)
    Button(top5,text = '导出成绩表（csv）',command = (lambda: interf.O('Score'))).grid(row=3,column=1,sticky=W+E+N+S, padx=5, pady=5)

    rb.grid(row=4,column=0,sticky=W+E+N+S, padx=5, pady=5)
    top5.mainloop()

#创建主GUI

root = Tk()
root.title("学生管理系统")
root.geometry('850x850')
Button(root,text='创建新学生管理数据库',command=creatTable,height=4,width=30,bg='pink').grid(row = 0,column=0,sticky=W+E+N+S,padx=2,pady=2)
Button(root,text='学生表管理',command=creat1,height=4,width=30,bg='lightpink').grid(row = 1,column=0,sticky=W+E+N+S,padx=2,pady=2)
Button(root,text='课程表管理',command=creat2,height=4,width=30,bg='lightpink').grid(row = 2,column=0,sticky=W+E+N+S,padx=2,pady=2)
Button(root,text='班级表管理',command=creat3,height=4,width=30,bg='lightpink').grid(row = 3,column=0,sticky=W+E+N+S,padx=2,pady=2)
Button(root,text='成绩表管理',command=creat4,height=4,width=30,bg='lightpink').grid(row = 4,column=0,sticky=W+E+N+S,padx=2,pady=2)
Button(root,text='文件IO',command=creat5,height=4,width=30,bg='lightpink').grid(row = 5,column=0,sticky=W+E+N+S,padx=2,pady=2)
img_python1 = PhotoImage(file = 'python.gif')
img_python2 = PhotoImage(file = 'python2.gif')
img_python3 = PhotoImage(file = 'python3.gif')
canvas = Canvas(root, width=300, height=300,bg='grey')
canvas.grid(row = 1,column=1,rowspan = 3,sticky=W)
canvas.create_image(150,150,image=img_python1)
canvas2 = Canvas(root, width=600, height=200,bg='grey')
canvas2.grid(row = 4,column=1,rowspan = 2,columnspan=2)
canvas2.create_image(300,100,image=img_python2)
canvas = Canvas(root, width=300, height=300,bg='grey')
canvas.grid(row = 1,column=2,rowspan = 3,sticky=W)
canvas.create_image(150,150,image=img_python3)
guide='''                   学生管理系统
使用指南：
第一个按钮可创建新数据库，第二到第五个按钮分别是对
"学生表"、"课程表"、"班级表"、"成绩表"进行插入、更新、删除、查找操作，
且可在相应界面选择需要操作的数据库，成绩表管理界面还可选择统计三门课程的平均分输出
第六个按钮可进行文件交互，将txt文件导入数据库或者将数据库中数据导出为csv文件
感谢使用 欢迎批评指正
'''
text = Text(root,font = ('msyh',12),bg='lightpink',height=20,width=100)
text.grid(row=6,column=0,columnspan = 3,padx=2,pady=2)
text.insert(INSERT,guide)

