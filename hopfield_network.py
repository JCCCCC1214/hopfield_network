import tkinter as tk
import math
import random
import numpy as np
import easygui
window = tk.Tk()
window.title('hopfield')
window.geometry('900x900')
window.configure(background='white')

scrollbar = tk.Scrollbar()
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)		
text = tk.Text(yscrollcommand=scrollbar.set)
text.pack(side=tk.LEFT,fill=tk.BOTH)	
scrollbar.config(command=text.yview)


w = np.zeros((108,108))
o = np.zeros((1,108))
flag = False
def select_train():
    flag = True
    global w,o
    w = np.zeros((108,108))
    templists1 = []
    templists2 = []
    a = np.zeros((1,108))
    o = np.zeros((108,1))
    linenumber = 0
    trainnumber = 0
    path = easygui.fileopenbox()
    file = open(path, mode="r")
    for line in file:
        templists1 += line
        linenumber += 1
        if(linenumber == 12):
            trainnumber += 1
            for i in range(len(templists1)):
                if(templists1[i] != '\n'):
                    templists2 += templists1[i]
            for i in range(len(templists2)):
                if(templists2[i] == ' '):
                    templists2[i] = '-1'
            for i in range(len(templists2)):
                a[0][i]+=int(templists2[i])
            b = a[0].reshape(a[0].shape[0],1)        
            c = b.dot(a)
            w = w+c
            templists1 = []
            templists2 = []
            a = np.zeros((1,108))
            linenumber = -1
    I = np.identity(108)
    w =  1/108*w - (trainnumber/108*I)
    for i in range(108):
        for j in range(108):
            o[i][0] += w[i][j]
    # print(o)
    # print(w)  
def select_test():
    global w,o
    templists1 = []
    templists2 = []
    linenumber = 0
    a = np.zeros((1,108))
    path = easygui.fileopenbox()
    file = open(path, mode="r")
    for line in file:
        templists1 += line
        linenumber += 1
        if(linenumber == 12):
            for i in range(len(templists1)):
                if(templists1[i] != '\n'):
                    templists2 += templists1[i]
            for i in range(len(templists2)):
                if(templists2[i] == ' '):
                    templists2[i] = '-1'
            for i in range(len(templists2)):
                a[0][i]+=int(templists2[i])
            b = a[0].reshape(a[0].shape[0],1)
            a = a[0].reshape(a[0].shape[0],1)
            number = 0
            for i in range(12):
                for j in range(9):
                    if(a[number][0]==1):
                        text.insert("insert","1")
                    else:
                        text.insert("insert"," ")
                    number+=1
                text.insert("insert",'\n')
            number = 0
            c = w.dot(b)
            while(1):
                falsenumber = True
                for i in range(108):
                    if(c[i][0]<o[i][0]):
                        c[i][0] = -1
                    elif(c[i][0]>o[i][0]):
                        c[i][0] = 1
                    elif(c[i][0] == o[i][0]):
                        c[i][0] = b[i][0]
                for i in range(108):
                    if(b[i][0] != c[i][0]):
                        falsenumber = False
                        break
                if(falsenumber):
                    break
                else:
                    for i in range(108):
                        b[i][0] = c[i][0]
            number = 0
            text.insert("insert","\n")
            text.insert("insert","  回想到\n")
            text.insert("insert","\n")
            for i in range(12):
                for j in range(9):
                    if(c[number][0]==1):
                        text.insert("insert","1")
                    else:
                        text.insert("insert"," ")
                    number+=1
                text.insert("insert",'\n')

            text.insert("insert","***************************************************")
            text.insert("insert",'\n')
            templists1 = []
            templists2 = []
            a = np.zeros((1,108))
            linenumber = -1


b1 = tk.Button(window, text='選擇訓練資料', font=('Arial', 12), width=15, height=1,command = select_train)
b1.place(x=600,y=10)
b2 = tk.Button(window, text='選擇測試資料', font=('Arial', 12), width=15, height=1,command = select_test)
b2.place(x=600,y=50)
window.mainloop()