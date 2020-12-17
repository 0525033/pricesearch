import tkinter as tk
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

df=pd.DataFrame({'健保碼':['','','','',''],'名稱':['','','','',''],'A廠品項':['','','','',''],'A品項價格':['','','','',''],'E廠品項':['','','','',''],'E品項價格':['','','','',''],'業務1價':['','','','',''],'業務2價':['','','','',''],'業務3價':['','','','','']})

#登入A、E網站============================================
chrome_options=Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()

driver.get('http://ec.k-e.com.tw/LoginView.aspx')
handles = driver.window_handles
driver.switch_to.window(handles[0])
handle1 = driver.current_window_handle
alert = driver.switch_to_alert()
alert.accept()
account_input = driver.find_element_by_id('cphContent_txtAccount')  # cphContent_txtPassword
account_input.send_keys('0401609')  # ysp0613 #cphContent_btnLogin
pass_input = driver.find_element_by_id('cphContent_txtPassword')
pass_input.send_keys('ysp0613')
login_btn = driver.find_element_by_id('cphContent_btnLogin')  # lkbRecipeCatalog
login_btn.click()
All_pro = driver.find_element_by_id('lkbAllCatalog')
All_pro.click()

driver.execute_script("window.open('about:blank', 'tab2');")
driver.switch_to_window('tab2')
driver.get('http://www.chahwa.com.tw/index.php')
driver.find_element_by_xpath('//*[@id="index"]/nav/ul/li[4]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="primptmsg"]/div/div[1]/form/ul/li[1]/span/input').send_keys('fkg20131101')
driver.find_element_by_xpath('/html/body/header/div[2]/div/div/div[1]/form/ul/li[2]/span/input').send_keys('fkg9988')
driver.find_element_by_id('urlogin_a').click()
time.sleep(3)
driver.find_element_by_class_name('order').click()

def ID_srch(ID,row):#row:0-4
    #切換到A廠===========================================
    driver.switch_to.window(handles[0])
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.send_keys(ID)
    srch_btn = driver.find_element_by_id('cphContent_ucCT_btnSearch')
    srch_btn.click()
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.clear()
    A_item=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[4]')
    A_price=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[6]')
    #初始化項目陣列
    items=[]
    prices=[]
    for i in range(1,len(A_item)):
        items.append(A_item[i].get_attribute('innerHTML'))
        prices.append(A_price[i].get_attribute('innerHTML'))
    A_optchange(items,prices,row)

    items=[]
    prices=[]
    #切換到E廠=============================================
    driver.switch_to_window('tab2')
    srch = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[2]/span/input')
    srch.send_keys(ID)
    srch_btn = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[4]/a')
    srch_btn.click()
    time.sleep(2)
    E_item=driver.find_elements_by_css_selector('.item .name a')
    E_price=driver.find_elements_by_css_selector('.item .sell_price span')
    i=0
    for i in range(0,len(E_item)):
        items.append(E_item[i].get_attribute('innerHTML'))
        prices.append(E_price[i].get_attribute('innerHTML'))
    E_optchange(items,prices,row)

def A_optchange(items,prices,row):
    if row==0:
        menu = A_N1["menu"]
        menu.delete(0, "end")
        global A_dict
        A_dict={}
        A_li1=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            A_li1.append(cleaned)
            varA1.set(A_li1[0])
            menu.add_command(label=cleaned, command=tk._setit(varA1, cleaned))
        for i in range(0,len(A_li1)):
            A_dict[A_li1[i]]=prices[i]
    elif row==1:
        menu = A_N2["menu"]
        menu.delete(0, "end")
        A_li2=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            A_li2.append(cleaned)
            varA2.set(A_li2[0])
            menu.add_command(label=cleaned, command=tk._setit(varA2, cleaned))

    elif row==2:
        menu = A_N3["menu"]
        menu.delete(0, "end")
        A_li3=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            A_li3.append(cleaned)
            varA3.set(A_li3[0])
            menu.add_command(label=cleaned, command=tk._setit(varA3, cleaned))

    elif row==3:
        menu = A_N4["menu"]
        menu.delete(0, "end")
        A_li4=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            A_li4.append(cleaned)
            varA4.set(A_li4[0])
            menu.add_command(label=cleaned, command=tk._setit(varA4, cleaned))

    elif row==4:
        menu = A_N5["menu"]
        menu.delete(0, "end")
        A_li5=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            A_li5.append(cleaned)
            varA5.set(A_li5[0])
            menu.add_command(label=cleaned, command=tk._setit(varA5, cleaned))

def E_optchange(items,prices,row):
    if row==0:
        menu = E_N1["menu"]
        menu.delete(0, "end")
        E_li1=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            E_li1.append(cleaned)
            varE1.set(E_li1[0])
            menu.add_command(label=cleaned, command=tk._setit(varE1, cleaned))
    elif row==1:
        menu = E_N2["menu"]
        menu.delete(0, "end")
        E_li2=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            E_li2.append(cleaned)
            varE2.set(E_li2[0])
            menu.add_command(label=cleaned, command=tk._setit(varE2, cleaned))

    elif row==2:
        menu = E_N3["menu"]
        menu.delete(0, "end")
        E_li3=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            E_li3.append(cleaned)
            varE3.set(E_li3[0])
            menu.add_command(label=cleaned, command=tk._setit(varE3, cleaned))

    elif row==3:
        menu = E_N4["menu"]
        menu.delete(0, "end")
        E_li4=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            E_li4.append(cleaned)
            varE4.set(E_li4[0])
            menu.add_command(label=cleaned, command=tk._setit(varE4, cleaned))

    elif row==4:
        menu = E_N5["menu"]
        menu.delete(0, "end")
        E_li5=[]
        for string in items:
            cleaned=re.sub('<br>.*','',string)
            E_li5.append(cleaned)
            varE5.set(E_li5[0])
            menu.add_command(label=cleaned, command=tk._setit(varE5, cleaned))

def Dataprocess():
    df['健保碼'][0]=enID_1.get()
    df['健保碼'][1]=enID_2.get()
    df['健保碼'][2]=enID_3.get()
    df['健保碼'][3]=enID_4.get()
    df['健保碼'][4]=enID_5.get()

    df['名稱'][0]=enNAME_1.get()
    df['名稱'][1]=enNAME_2.get()
    df['名稱'][2]=enNAME_3.get()
    df['名稱'][3]=enNAME_4.get()
    df['名稱'][4]=enNAME_5.get()

    for i in range(0,5):#0-4
        if df['健保碼'][i]!='':
            ID_srch(df['健保碼'][i],i)
        elif df['名稱'][i]!='':
            print('line129',i)
            df['A廠品項'][i]='名稱搜尋'
            df['A品項價格'][i]='名稱搜尋'
            df['E廠品項'][i]='名稱搜尋'
            df['E品項價格'][i]='名稱搜尋'
        else:
            continue
    print(df)

def optchanged(*args):
    print('line209',varA1.get())
    print(A_dict)


#生成視窗元件==================================
win=tk.Tk()
win.geometry('1500x300')

lbID=tk.Label(win,text='健保碼',width=20).grid(row=0,column=0)
lbNAME=tk.Label(win,text='名稱',width=20).grid(row=0,column=1)
lbA_N=tk.Label(win,text='A廠品項',width=20).grid(row=0,column=2)
lbA_P=tk.Label(win,text='A品項價格',width=20).grid(row=0,column=3)
lbE_N=tk.Label(win,text='E廠品項',width=20).grid(row=0,column=4)
lbE_P=tk.Label(win,text='E品項價格',width=20).grid(row=0,column=5)
lbS1=tk.Label(win,text='業務1價',width=10).grid(row=0,column=6)
lbS2=tk.Label(win,text='業務2價',width=10).grid(row=0,column=7)
lbS3=tk.Label(win,text='業務3價',width=10).grid(row=0,column=8)



#健保碼欄位=====================================
ID1=tk.StringVar(win).set('')
ID2=tk.StringVar(win).set('')
ID3=tk.StringVar(win).set('')
ID4=tk.StringVar(win).set('')
ID5=tk.StringVar(win).set('')

enID_1=tk.Entry(win,width=20,textvariale=ID1)
enID_2=tk.Entry(win,width=20,textvariale=ID2)
enID_3=tk.Entry(win,width=20,textvariale=ID3)
enID_4=tk.Entry(win,width=20,textvariale=ID4)
enID_5=tk.Entry(win,width=20,textvariale=ID5)

enID_1.grid(column=0,row=1)
enID_2.grid(column=0,row=2)
enID_3.grid(column=0,row=3)
enID_4.grid(column=0,row=4)
enID_5.grid(column=0,row=5)

#名稱欄位========================================
enNAME_1=tk.Entry(win,width=20)
enNAME_2=tk.Entry(win,width=20)
enNAME_3=tk.Entry(win,width=20)
enNAME_4=tk.Entry(win,width=20)
enNAME_5=tk.Entry(win,width=20)

enNAME_1.grid(column=1,row=1)
enNAME_2.grid(column=1,row=2)
enNAME_3.grid(column=1,row=3)
enNAME_4.grid(column=1,row=4)
enNAME_5.grid(column=1,row=5)

#A廠項目欄位======================================
A_li1=['']
A_li2=['']
A_li3=['']
A_li4=['']
A_li5=['']

varA1=tk.StringVar(win)
varA2=tk.StringVar(win)
varA3=tk.StringVar(win)
varA4=tk.StringVar(win)
varA5=tk.StringVar(win)

varA1.trace('w',optchanged)

A_N1=tk.OptionMenu(win,varA1,*A_li1)
A_N2=tk.OptionMenu(win,varA2,*A_li2)
A_N3=tk.OptionMenu(win,varA3,*A_li3)
A_N4=tk.OptionMenu(win,varA4,*A_li4)
A_N5=tk.OptionMenu(win,varA5,*A_li5)

A_N1.grid(column=2,row=1)
A_N2.grid(column=2,row=2)
A_N3.grid(column=2,row=3)
A_N4.grid(column=2,row=4)
A_N5.grid(column=2,row=5)

#A項目價格欄位======================================
A_P1=tk.Label(win,text='20').grid(column=3,row=1)
A_P2=tk.Label(win,text='20').grid(column=3,row=2)
A_P3=tk.Label(win,text='20').grid(column=3,row=3)
A_P4=tk.Label(win,text='20').grid(column=3,row=4)
A_P5=tk.Label(win,text='20').grid(column=3,row=5)

#E廠項目欄位============================================
E_li1=['']
E_li2=['']
E_li3=['']
E_li4=['']
E_li5=['']

varE1=tk.StringVar(win)
varE2=tk.StringVar(win)
varE3=tk.StringVar(win)
varE4=tk.StringVar(win)
varE5=tk.StringVar(win)

E_N1=tk.OptionMenu(win,varE1,*E_li1)
E_N2=tk.OptionMenu(win,varE2,*E_li2)
E_N3=tk.OptionMenu(win,varE3,*E_li3)
E_N4=tk.OptionMenu(win,varE4,*E_li4)
E_N5=tk.OptionMenu(win,varE5,*E_li5)

E_N1.grid(column=4,row=1)
E_N2.grid(column=4,row=2)
E_N3.grid(column=4,row=3)
E_N4.grid(column=4,row=4)
E_N5.grid(column=4,row=5)

#E廠項目價格欄位
E_P1=tk.Label(win,text='20').grid(column=5,row=1)
E_P2=tk.Label(win,text='20').grid(column=5,row=2)
E_P3=tk.Label(win,text='20').grid(column=5,row=3)
E_P4=tk.Label(win,text='20').grid(column=5,row=4)
E_P5=tk.Label(win,text='20').grid(column=5,row=5)

S1_1=tk.Entry(win,width=10).grid(column=6,row=1)
S1_2=tk.Entry(win,width=10).grid(column=6,row=2)
S1_3=tk.Entry(win,width=10).grid(column=6,row=3)
S1_4=tk.Entry(win,width=10).grid(column=6,row=4)
S1_5=tk.Entry(win,width=10).grid(column=6,row=5)

S2_1=tk.Entry(win,width=10).grid(column=7,row=1)
S2_2=tk.Entry(win,width=10).grid(column=7,row=2)
S2_3=tk.Entry(win,width=10).grid(column=7,row=3)
S2_4=tk.Entry(win,width=10).grid(column=7,row=4)
S2_5=tk.Entry(win,width=10).grid(column=7,row=5)

S3_1=tk.Entry(win,width=10).grid(column=8,row=1)
S3_2=tk.Entry(win,width=10).grid(column=8,row=2)
S3_3=tk.Entry(win,width=10).grid(column=8,row=3)
S3_4=tk.Entry(win,width=10).grid(column=8,row=4)
S3_5=tk.Entry(win,width=10).grid(column=8,row=5)

btn=tk.Button(win,width=20,text='查詢',command=Dataprocess)
btn.grid(column=8,row=6)
win.mainloop()