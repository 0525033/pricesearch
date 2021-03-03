import tkinter as tk
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import threading
import sys

df=pd.DataFrame({'健保碼':['','','','',''],'名稱':['','','','',''],'A廠品項':['','','','',''],'A品項價格':['','','','',''],'E廠品項':['','','','',''],'E品項價格':['','','','',''],'業務1價':['','','','',''],'業務2價':['','','','',''],'業務3價':['','','','','']})
A_dict={}
E_dict={}

#登入A、E網站============================================
chrome_options=Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()

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
driver.find_element_by_xpath('//*[@id="primptmsg"]/div/div[1]/form/ul/li[1]/span/input').send_keys('fortune77')
driver.find_element_by_xpath('/html/body/header/div[2]/div/div/div[1]/form/ul/li[2]/span/input').send_keys('fortune22477301')
driver.find_element_by_id('urlogin_a').click()
time.sleep(1.5)
driver.find_element_by_class_name('order').click()


#以ID搜尋========================================================
def ID_srch(ID,row):#row:0-4
    #切換到A廠==================================================
    driver.switch_to.window(handles[0])
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.send_keys(ID)
    srch_btn = driver.find_element_by_id('cphContent_ucCT_btnSearch')
    srch_btn.click()
    time.sleep(0.5)
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.clear()
    A_item=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[4]')
    A_price=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[6]')
    A_status=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[2]')
    #初始化項目陣列==============================================
    items=[]
    prices=[]
    status=[]
    if len(A_item)>1:
        for i in range(1,len(A_item)):
            itemName=A_item[i].get_attribute('innerHTML')
            itemName=re.sub('<br>.*','',itemName)
            items.append(itemName)
            price=A_price[i].get_attribute('innerHTML')
            price=re.sub('\.00','',price)
            prices.append(price)
            status.append(A_status[i].get_attribute('innerHTML'))
            item={}
            item['price']=prices[i-1]
            item['status']=status[i-1]
            A_dict[items[i-1]]=item
        A_optchange(A_dict,items,row)
    i=0
    items=[]
    prices=[]
    status=[]
    #切換到E廠==================================================
    driver.switch_to_window('tab2')
    srch = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[2]/span/input')
    srch.send_keys(ID)
    srch_btn = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[4]/a')
    srch_btn.click()
    time.sleep(0.7)
    E_item=driver.find_elements_by_css_selector('.item .name a')
    E_price=driver.find_elements_by_css_selector('.item .sell_price span')
    E_status=driver.find_elements_by_css_selector('.item .status')
    if len(E_item)>0:
        for i in range(0,len(E_item)):
            itemName=E_item[i].get_attribute('innerHTML')
            items.append(itemName)
            prices.append(E_price[i].get_attribute('innerHTML'))
            status.append(E_status[i].get_attribute('innerHTML'))
            item={}
            item['price']=prices[i]
            item['status']=status[i]
            E_dict[items[i]]=item
        #E_dict['實驗項目']=E_dict.pop(items[0])
        E_optchange(E_dict,items,row)
    btn.config(state=tk.NORMAL)

#以名稱搜尋==========================================================
def NAME_srch(NAME,row):#row:0-4
    #切換到A廠==================================================
    driver.switch_to.window(handles[0])
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.send_keys(NAME)
    srch_btn = driver.find_element_by_id('cphContent_ucCT_btnSearch')
    srch_btn.click()
    srch = driver.find_element_by_id('cphContent_ucCT_txtKeyword')
    srch.clear()
    time.sleep(0.3)
    A_item=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[4]')
    A_price=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[6]')
    A_status=driver.find_elements_by_xpath('//*[@id="cphContent_ucCT_gv"]/tbody/tr/td[2]')
    #初始化項目陣列==============================================
    items=[]
    prices=[]
    status=[]
    if len(A_item)>1:
        for i in range(1,len(A_item)):
            itemName=A_item[i].get_attribute('innerHTML')
            itemName=re.sub('<br>.*','',itemName)
            items.append(itemName)
            price=A_price[i].get_attribute('innerHTML')
            price=re.sub('\.00','',price)
            prices.append(price)
            status.append(A_status[i].get_attribute('innerHTML'))
            item={}
            item['price']=prices[i-1]
            item['status']=status[i-1]
            A_dict[items[i-1]]=item
        A_optchange(A_dict,items,row)
    i=0
    items=[]
    prices=[]
    status=[]
    #切換到E廠==================================================
    driver.switch_to_window('tab2')
    srch = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[1]/span/input')
    srch.send_keys(NAME)
    srch_btn = driver.find_element_by_xpath('//*[@id="orderForm"]/ul/li[4]/a')
    srch_btn.click()
    time.sleep(0.5)
    E_item=driver.find_elements_by_css_selector('.item .name a')
    E_price=driver.find_elements_by_css_selector('.item .sell_price span')
    E_status=driver.find_elements_by_css_selector('.item .status')
    if len(E_item)>0:
        for i in range(0,len(E_item)):
            itemName=E_item[i].get_attribute('innerHTML')
            items.append(itemName)
            prices.append(E_price[i].get_attribute('innerHTML'))
            status.append(E_status[i].get_attribute('innerHTML'))
            item={}
            item['price']=prices[i]
            item['status']=status[i]
            E_dict[items[i]]=item
        #E_dict['實驗項目']=E_dict.pop(items[0])
        E_optchange(E_dict,items,row)
    btn.config(state=tk.NORMAL)

def A_optchange(A_dict,itemList,row):
    if row==0:
        menu = A_N1["menu"]
        menu.delete(0, "end")
        A_li1=[]
        dict_string=list(A_dict.keys())
        for string in itemList:
            A_li1.append(string)
            varA1.set(A_li1[0])
            menu.add_command(label=string, command=tk._setit(varA1, string))
        item=A_dict[varA1.get()]
        A_P1.config(text=item['price'])
    elif row==1:
        menu = A_N2["menu"]
        menu.delete(0, "end")
        A_li2=[]
        dict_string=list(A_dict.keys())
        for string in itemList:
            A_li2.append(string)
            varA2.set(A_li2[0])
            menu.add_command(label=string, command=tk._setit(varA2, string))
        item=A_dict[varA2.get()]
        A_P2.config(text=item['price'])
    elif row==2:
        menu = A_N3["menu"]
        menu.delete(0, "end")
        A_li3=[]
        dict_string=list(A_dict.keys())
        for string in itemList:
            A_li3.append(string)
            varA3.set(A_li3[0])
            menu.add_command(label=string, command=tk._setit(varA3, string))
        item=A_dict[varA3.get()]
        A_P3.config(text=item['price'])
    elif row==3:
        menu = A_N4["menu"]
        menu.delete(0, "end")
        A_li4=[]
        dict_string=list(A_dict.keys())
        for string in itemList:
            A_li4.append(string)
            varA4.set(A_li4[0])
            menu.add_command(label=string, command=tk._setit(varA4, string))
        item=A_dict[varA4.get()]
        A_P4.config(text=item['price'])
    elif row==4:
        menu = A_N5["menu"]
        menu.delete(0, "end")
        A_li5=[]
        dict_string=list(A_dict.keys())
        for string in itemList:
            A_li5.append(string)
            varA5.set(A_li5[0])
            menu.add_command(label=string, command=tk._setit(varA5, string))
        item=A_dict[varA5.get()]
        A_P5.config(text=item['price'])

def E_optchange(E_dict,itemList,row):
    if row==0:
        menu = E_N1["menu"]
        menu.delete(0, "end")
        E_li1=[]
        for string in itemList:
            E_li1.append(string)
            varE1.set(E_li1[0])
            menu.add_command(label=string, command=tk._setit(varE1, string))
        item=E_dict[varE1.get()]
        E_P1.config(text=item['price'])
    elif row==1:
        menu = E_N2["menu"]
        menu.delete(0, "end")
        E_li2=[]
        for string in itemList:
            E_li2.append(string)
            varE2.set(E_li2[0])
            menu.add_command(label=string, command=tk._setit(varE2, string))
        item=E_dict[varE2.get()]
        E_P2.config(text=item['price'])

    elif row==2:
        menu = E_N3["menu"]
        menu.delete(0, "end")
        E_li3=[]
        for string in itemList:
            E_li3.append(string)
            varE3.set(E_li3[0])
            menu.add_command(label=string, command=tk._setit(varE3, string))
        item=E_dict[varE3.get()]
        E_P3.config(text=item['price'])

    elif row==3:
        menu = E_N4["menu"]
        menu.delete(0, "end")
        E_li4=[]
        for string in itemList:
            E_li4.append(string)
            varE4.set(E_li4[0])
            menu.add_command(label=string, command=tk._setit(varE4, string))
        item=E_dict[varE4.get()]
        E_P4.config(text=item['price'])

    elif row==4:
        menu = E_N5["menu"]
        menu.delete(0, "end")
        E_li5=[]
        for string in itemList:
            E_li5.append(string)
            varE5.set(E_li5[0])
            menu.add_command(label=string, command=tk._setit(varE5, string))
        item=E_dict[varE5.get()]
        E_P5.config(text=item['price'])

def Dataprocess():
    btn.config(state=tk.DISABLED)
    win.update()
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

    #查資料前初始化===============================
    varA1.set('')
    varA2.set('')
    varA3.set('')
    varA4.set('')
    varA5.set('')

    varE1.set('')
    varE2.set('')
    varE3.set('')
    varE4.set('')
    varE5.set('')

    A_N1["menu"].delete(0, "end")
    A_N2["menu"].delete(0, "end")
    A_N3["menu"].delete(0, "end")
    A_N4["menu"].delete(0, "end")
    A_N5["menu"].delete(0, "end")

    E_N1["menu"].delete(0, "end")
    E_N2["menu"].delete(0, "end")
    E_N3["menu"].delete(0, "end")
    E_N4["menu"].delete(0, "end")
    E_N5["menu"].delete(0, "end")

    A_P1.config(text='0')
    A_P2.config(text='0')
    A_P3.config(text='0')
    A_P4.config(text='0')
    A_P5.config(text='0')

    E_P1.config(text='0')
    E_P2.config(text='0')
    E_P3.config(text='0')
    E_P4.config(text='0')
    E_P5.config(text='0')

    A_S1.config(text='-')
    A_S2.config(text='-')
    A_S3.config(text='-')
    A_S4.config(text='-')
    A_S5.config(text='-')

    E_S1.config(text='-')
    E_S2.config(text='-')
    E_S3.config(text='-')
    E_S4.config(text='-')
    E_S5.config(text='-')

    #優先以健保碼搜尋
    for i in range(0,5):#0-4
        if df['健保碼'][i]!='':
            ID_srch(df['健保碼'][i],i)
        elif df['名稱'][i]!='':
            NAME_srch(df['名稱'][i],i)
        else:
            continue
def A_update(A_P,A_S,varA):
    item=A_dict[varA.get()]
    price=item['price']
    status=item['status']
    A_P.config(text=price)
    A_S.config(text=status)

def E_update(E_P,E_S,varE):
    item=E_dict[varE.get()]
    price=item['price']
    status=item['status']
    E_P.config(text=price)
    E_S.config(text=status)
#生成視窗元件==================================
    

#倒數計時工具================================================
def timeout():
    timer=1200
    while True:
        if timer>0:
            time.sleep(1)
            timer-=1
            countdown.config(text='A、E網站將於'+str(timer)+'秒後重新整理')
        else:
            countdown.config(text='重新整理中，請稍後...')
            timer=1200
            driver.switch_to.window(handles[0])
            driver.refresh()
            driver.switch_to_window('tab2')
            driver.refresh()

#關閉視窗事件==================================================
def on_closing():
    driver.quit()
    win.destroy()
    sys.exit()



win=tk.Tk()
win.title('查價程式')
win.geometry('1500x300')

lbID=tk.Label(win,text='健保碼',width=12).grid(row=0,column=0)
lbNAME=tk.Label(win,text='名稱',width=12).grid(row=0,column=1)
lbA_N=tk.Label(win,text='A廠品項',width=20).grid(row=0,column=2)
lbA_P=tk.Label(win,text='A品項價格',width=10).grid(row=0,column=3)
lbA_S=tk.Label(win,text='A品項庫存',width=10).grid(row=0,column=4)
lbE_N=tk.Label(win,text='E廠品項',width=20).grid(row=0,column=5)
lbE_P=tk.Label(win,text='E品項價格',width=10).grid(row=0,column=6)
lbE_S=tk.Label(win,text='E品項庫存',width=10).grid(row=0,column=7)



#健保碼欄位=====================================
ID1=tk.StringVar(win).set('')
ID2=tk.StringVar(win).set('')
ID3=tk.StringVar(win).set('')
ID4=tk.StringVar(win).set('')
ID5=tk.StringVar(win).set('')

enID_1=tk.Entry(win,width=12,textvariale=ID1)
enID_2=tk.Entry(win,width=12,textvariale=ID2)
enID_3=tk.Entry(win,width=12,textvariale=ID3)
enID_4=tk.Entry(win,width=12,textvariale=ID4)
enID_5=tk.Entry(win,width=12,textvariale=ID5)

enID_1.grid(column=0,row=1)
enID_2.grid(column=0,row=2)
enID_3.grid(column=0,row=3)
enID_4.grid(column=0,row=4)
enID_5.grid(column=0,row=5)

#名稱欄位========================================
enNAME_1=tk.Entry(win,width=12)
enNAME_2=tk.Entry(win,width=12)
enNAME_3=tk.Entry(win,width=12)
enNAME_4=tk.Entry(win,width=12)
enNAME_5=tk.Entry(win,width=12)

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
A_P1=tk.Label(win,text='0')
A_P2=tk.Label(win,text='0')
A_P3=tk.Label(win,text='0')
A_P4=tk.Label(win,text='0')
A_P5=tk.Label(win,text='0')

A_P1.grid(column=3,row=1)
A_P2.grid(column=3,row=2)
A_P3.grid(column=3,row=3)
A_P4.grid(column=3,row=4)
A_P5.grid(column=3,row=5)

#A項目庫存===========================================
A_S1=tk.Label(win,text='-')
A_S2=tk.Label(win,text='-')
A_S3=tk.Label(win,text='-')
A_S4=tk.Label(win,text='-')
A_S5=tk.Label(win,text='-')

A_S1.grid(column=4,row=1)
A_S2.grid(column=4,row=2)
A_S3.grid(column=4,row=3)
A_S4.grid(column=4,row=4)
A_S5.grid(column=4,row=5)

#E廠項目庫存=============================================
E_S1=tk.Label(win,text='-')
E_S2=tk.Label(win,text='-')
E_S3=tk.Label(win,text='-')
E_S4=tk.Label(win,text='-')
E_S5=tk.Label(win,text='-')

E_S1.grid(column=7,row=1)
E_S2.grid(column=7,row=2)
E_S3.grid(column=7,row=3)
E_S4.grid(column=7,row=4)
E_S5.grid(column=7,row=5)
 
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

E_N1.grid(column=5,row=1)
E_N2.grid(column=5,row=2)
E_N3.grid(column=5,row=3)
E_N4.grid(column=5,row=4)
E_N5.grid(column=5,row=5)

#E廠項目價格欄位==========================================
E_P1=tk.Label(win,text='0')
E_P2=tk.Label(win,text='0')
E_P3=tk.Label(win,text='0')
E_P4=tk.Label(win,text='0')
E_P5=tk.Label(win,text='0')

E_P1.grid(column=6,row=1)
E_P2.grid(column=6,row=2)
E_P3.grid(column=6,row=3)
E_P4.grid(column=6,row=4)
E_P5.grid(column=6,row=5)

#A、E下拉式選單變動======================================
varA1.trace('w',lambda *args: A_update(A_P1,A_S1,varA1))
varA2.trace('w',lambda *args: A_update(A_P2,A_S2,varA2))
varA3.trace('w',lambda *args: A_update(A_P3,A_S3,varA3))
varA4.trace('w',lambda *args: A_update(A_P4,A_S4,varA4))
varA5.trace('w',lambda *args: A_update(A_P5,A_S5,varA5))

varE1.trace('w',lambda *args:E_update(E_P1,E_S1,varE1))
varE2.trace('w',lambda *args:E_update(E_P2,E_S2,varE2))
varE3.trace('w',lambda *args:E_update(E_P3,E_S3,varE3))
varE4.trace('w',lambda *args:E_update(E_P4,E_S4,varE4))
varE5.trace('w',lambda *args:E_update(E_P5,E_S5,varE5))

#業務報價===============================================

countdown=tk.Label(win,text='')
countdown.grid(column=4,row=6,columnspan=2)

btn=tk.Button(win,width=10,text='查詢',command=Dataprocess)
win.bind('<Return>',lambda *args:Dataprocess())
btn.grid(column=6,row=6,columnspan=2)
win.protocol("WM_DELETE_WINDOW", on_closing)


#多線程設定===================================
tList=[]

t2=threading.Thread(target=timeout)
tList.append(t2)

for t in tList:
    t.start()


win.mainloop()