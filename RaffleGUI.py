from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.filedialog import (askopenfilename,askopenfilenames,askdirectory,asksaveasfilename)
import requests #外置库
import json
import linecache
import sys,os
import time
import math
#import re
import random
import qrcode #外置库
import tkinter.messagebox
from tkinter import ttk
from datetime import datetime,timedelta
import secrets
#import _thread
import threading
import pyperclip
#import windnd
#from random import choice
#from random import sample
#上方代码导入所有需要的库

import base64
from iconwin import img
import rc4
#打包成exe所需的库

version='1.1.0.008'
updatetime='2021-03-31'

class NullClass:
    def is_alive(N):
        return False

def setIcon(win):
    #释放icon.py所保存的图标，打包exe时要用
    tmp=open('tmp.ico','wb+')
    tmp.write(base64.b64decode(img))#写入到临时文件中
    tmp.close()
    win.iconbitmap("tmp.ico") #设置图标
    os.remove("tmp.ico")           #删除临时图标

def jsonDataToUrlParams(params_data):
    url_str = ''
    nums = 0
    max_nums = len(params_data)
    for key in params_data:
        nums = nums + 1
        if nums == max_nums:
            url_str += str(key) + '=' + str(params_data[key])
        else:
            url_str += str(key) + '=' + str(params_data[key]) + ';'
    else:
        return url_str
    
EnaRZ=False
RZOFF=False
def printp(text):
    #输出记录到文本框
    #print(text)
    output['state']='normal'
    output.insert('end',nowtm()+str(text)+'\n')
    output['state']='disabled'
    output.see(END)
    window.update()
    if EnaRZ and not RZOFF:
        RZtxt = open(rzpath,'a',encoding='utf-8')
        RZtxt.write(text)
        RZtxt.write('\n')
        RZtxt.close()

def outrb():
    output['state']='normal'
    output.delete('end - 2 lines','end - 1 lines')
    output['state']='disabled'

notime=True
def nowtm():
    #记录列表输出当前时间
    if not notime:
        now = datetime.now()
        nowtime=now.strftime("%H:%M:%S")
        return '['+nowtime+']'
    else:
        return ''

cjthread=NullClass()
updinfo='(更新检测未完成)'
def chkupd():
    global updinfo
    ver=version[version.rfind('.'):]
    head, sep, ver = ver.partition('.')
    #print(ver)
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    }
    try:
        r=requests.get('https://api.github.com/repos/shoyu3/DynamicRaffle-Python/releases/latest',headers=header)
        gitreturn=json.loads(r.text)
        gitversion=gitreturn['name']
        gitver=gitversion[gitversion.rfind('.'):]
        head, sep, gitver = gitver.partition('.')
        #print(gitver)
        if ver<gitver:
            #print('服务器有新版本，请更新！')
            chklbl1.configure(text='有新版本可用！')
            if '\n 'in gitreturn['body']:
                hh='\n'
            else:
                hh=''
            IsGotoupd=tkinter.messagebox.askyesno("提示", '有新版本可用！建议及时更新~\n当前版本：'+str(version)+'\n最新版本：'+str(gitversion)+'\n更新说明：'+hh+gitreturn['body']+'\n点击“是”前往更新，点击“否”继续运行')
            if IsGotoupd:
                os.system('start '+gitreturn['html_url'])
            updinfo='有新版本可用！('+gitversion+' > '+version+')'
        else:
            try:
                chklbl1.configure(text='恭喜~当前版本已是最新!')
            except:
                pass
            time.sleep(0.8)
            updinfo='当前版本已是最新！('+version+')'
        if not cjthread.is_alive():
            printp(updinfo)
    except:
        try:
            chklbl1.configure(text='检测更新时出现了问题!呜呜呜…')
        except:
            pass
        time.sleep(0.8)
        updinfo='检测更新时出现了问题……'
        #print('当前版本已是最新！')
    chkupdwindow.destroy()

#下面1条def在获取数据时会用到，定义链接
def likelisturl(page):
    return 'http://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/spec_item_likes?dynamic_id='+str(dyid)+'&pn='+str(page)

#替换布尔值（true和false）
def repBool(value):
    if value:
        val=str(value).replace('True','√')#✔
    else:
        val=str(value).replace('False','X')#❌
    return val

def repBool2(value):
    if value:
        val=str(value).replace('True','显示')#✔
    else:
        val=str(value).replace('False','隐藏')#❌
    return val

#传入链接，使用requests获取内容，允许超时3次
def gethtml(url, header):
    i = 0
    while i < 3:
        try:
            html = requests.get(url, headers=header, timeout=5)
            html.encoding = "utf-8"
            return html.text
        except requests.exceptions.RequestException:
            printp('警告：超时'+str(i+1)+'次，位于'+str(errortime)+'页')
            i += 1

#===============================================================================================#
#部分实现方法源自项目：https://github.com/LeoChen98/BiliRaffle，点赞判定为芍芋原创（反正很简单）#
#===============================================================================================#

def now_time():
    #输出当前时间
    t = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return t

def _get_offset(data_json):
    #获取转发列表用
    if 'offset' in data_json['data']:
        return data_json['data']['offset']
    else:
        return None

def getZF(dyn_id):
    global RZOFF
    printp('正在获取完整转发列表……')
    RZOFF=True
    printp('Loading...')
    dynamic_api = "http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail"
    info = {
        "time": now_time(),
        "dyn_id": dyn_id
    }
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    }
    # 首次数据获取
    offset = "1:0"
    param = {'dynamic_id': dyn_id, 'offset': offset}
    data = requests.get(dynamic_api, headers=header, params=param, timeout=10)
    data_json = json.loads(data.text)
    total_num = data_json['data']['total']
    info['total'] = total_num

    # 获取全部数据
    uidall=[]
    now_num = 0
    count = 0
    users = []
    while now_num < total_num:  # 循环获取页面
        param = {'dynamic_id': dyn_id, 'offset': offset}
        data = requests.get(dynamic_api, headers=header, params=param, timeout=10)
        data_json = json.loads(data.text)
        for i in range(0, 20):  # 获取单页的所有用户（最多20条）
            if count < total_num:
                count += 1
                try:
                    uid = data_json['data']['items'][i]['desc']['uid']
                    uidall.append(uid)
                    outrb()
                    curusr=len(uidall)
                    percent='%.2f' % float(curusr/total_num*100)
                    BarProgress(40+15*float(curusr/total_num))
                    printp(str(percent)+'% ('+str(curusr)+'/'+str(total_num)+')')
                except:
                    pass
            else:  # 最后一页数量少于20时
                break
        offset = _get_offset(data_json)
        if offset is None:
            break
        now_num += 20
        time.sleep(0.2)
    uidall.sort()
    try:
        uidall.remove(myuid)
    except:
        pass
    output['state']='normal'
    output.delete('end - 2 lines','end - 1 lines')
    output['state']='disabled'
    '''curusr=len(uidall)
    printp('100.00% ('+str(curusr)+'/'+str(curusr)+')')'''
    RZOFF=False
    printp('完成，共有 '+str(len(uidall))+' 位，已存至列表中')
    return uidall

def getPL(Dynamic_id):
    global notime
    global RZOFF
    printp('正在获取完整评论列表……')
    current_page = 1
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/86.0.4324.182 Safari/537.36",
    }
    rid = dyinfo['card']['desc']['rid']
    link1 = 'http://api.bilibili.com/x/v2/reply?&jsonp=json&pn='
    link2 = '&type=11&oid='
    link3 = '&sort=2'#&_=1570498003332'
    comment_list = []
    userlist_1=[]
    pool = {}
    r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
    json_data = json.loads(r)
    #print(json_data)
    if json_data['code']==-404:
        outrb()
        printp('正在获取完整评论列表……(模式二)')
        rid=Dynamic_id
        #print(rid)
        link2 = '&type=17&oid='
        r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
        json_data = json.loads(r)
        #print(json_data)
        if json_data['code']==-404:
            notime=True
            printp('获取评论失败,可能因为此动态没有除UP主自己的评论以外的评论呢')
            notime=False
            return False
    if json_data['code']==-412:
        notime=True
        printp('获取评论失败，调取间隔过短，请过一段时间再试吧~')
        notime=False
        return False
    comments_num = json_data['data']['page']['count']
    pages_num = comments_num // 20 + 1
    RZOFF=True
    printp('Loading...')
    while True:
        r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
        json_data1 = json.loads(r)
        if json_data1['data']['replies']:
            for reply in json_data1['data']['replies']:
                userlist_1.append(int(reply['member']['mid']))
                outrb()
                curusr=len(userlist_1)
                percent='%.2f' % float(curusr/comments_num*100)
                BarProgress(55+15*float(curusr/comments_num))
                printp(str(percent)+'% ('+str(curusr)+'/'+str(comments_num)+')')
        current_page += 1
        if current_page > pages_num:
            break
    userlist_1.sort()
    try:
        userlist_1.remove(myuid)
    except:
        pass
    output['state']='normal'
    output.delete('end - 2 lines','end - 1 lines')
    output['state']='disabled'
    '''curusr=len(userlist_1)
    printp('100.00% ('+str(curusr)+'/'+str(curusr)+')')'''
    RZOFF=False
    printp('完成，共有 '+str(len(userlist_1))+' 位，已存至列表中')
    return userlist_1

def getDZ(dyid):
    global errortime
    global notime
    global RZOFF
    printp('正在获取完整点赞列表……')
    RZOFF=True
    printp('Loading...')
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    }
    r=gethtml(likelisturl(1),header)
    errortime=1
    userlist_dict=json.loads(r)
    jdata=userlist_dict['data']
    jlist=jdata['item_likes']
    totalfans=jdata.get('total_count')
    math2=math.ceil(jdata.get('total_count')/20)*20-totalfans
    pages=math.ceil(totalfans/20)
    times=1
    errortime=1
    userlist_1=[]
    #notime=True
    likes=dyinfo['card']['desc']['like']
    while times < pages+1:
        errortime=times
        r=gethtml(likelisturl(times), header)
        userlist_dict=json.loads(r)
        jdata=userlist_dict['data']
        jlist=jdata['item_likes']
        times2=0
        if times != pages:
            while times2<20:
                userlist_1.append(jlist[times2].get('uid'))
                times2=times2+1
                outrb()
                curusr=len(userlist_1)
                percent='%.2f' % float(curusr/likes*100)
                printp(str(percent)+'% ('+str(curusr)+'/'+str(likes)+')')
        else:
            while times2<20-math2:
                userlist_1.append(jlist[times2].get('uid'))
                times2=times2+1
                outrb()
                curusr=len(userlist_1)
                percent='%.2f' % float(curusr/likes*100)
                printp(str(percent)+'% ('+str(curusr)+'/'+str(likes)+')')
        BarProgress(70+15*float(curusr/likes))
        times=times+1
        time.sleep(0.3)
    userlist_1.sort()
    try:
        userlist_1.remove(myuid)
    except:
        pass
    notime=False
    output['state']='normal'
    output.delete('end - 2 lines','end - 1 lines')
    output['state']='disabled'
    RZOFF=False
    printp('完成，共有 '+str(len(userlist_1))+' 位，已存至列表中')
    return list(userlist_1)

def getname(users):
    #获取用户名
    global ATuser
    times=0
    if NEEDAT:
        ATuser=[]
    while times<len(users):
        url='http://api.bilibili.com/x/space/acc/info?mid='+str(users[times])
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.4324.182 Safari/537.36",
        }
        res = requests.get(url=url,headers=header)
        resback=json.loads(res.text)
        usrinfo=resback.get('data')
        try:
            mid=usrinfo.get('mid')
            uname=str(usrinfo.get('name'))
        except:
            #print(res.text)
            mid=(users[times])
            uname='[获取失败]'
        printp(str(times+1)+' '+uname+' (UID:'+str(mid)+')')
        if NEEDAT:
            ATuser.append('@'+uname)
        times=times+1

def checkGZ(mid):
    if TGZ:
        url='http://api.bilibili.com/x/space/acc/relation?mid='+str(mid)
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        "Cookie":cookie,
        }
        res = requests.get(url=url,headers=header)
        resback=json.loads(res.text)
        rinfo=resback.get('data')
        be_relation=rinfo['be_relation']['attribute']
        if not be_relation==2 and not be_relation==6:
            printp('[UID:'+str(mid)+' 未关注('+str(be_relation)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def checkCJH(mid,condition):
    if GLCJH:
        #false为不通过
        raffle_count=0
        condition=condition
        url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid='+str(mid)+'&offset_dynamic_id=0'
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        }
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        if resback['code']==0:
            rinfo=resback.get('data')
            if resback['code']!=0:
                printp('检测抽奖号'+str(mid)+'时出错，返回值为:'+str(resback['code']))
                return True
            try:
                check_count=len(rinfo['cards'])
            except:
                printp('检测抽奖号'+str(mid)+'时出错，无法获取到动态信息')
                return True
            if check_count>10:
                check_count=10
            times=0
            while times<check_count:
                #print(rinfo['cards'][times]['card'])
                dycont=rinfo['cards'][times]['card']
                if CHKCJDT(dycont):
                    raffle_count=raffle_count+1
                times=times+1
        if raffle_count > condition:
            printp('[UID:'+str(mid)+' 判定为抽奖号('+str(raffle_count)+'/'+str(condition)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def checklvl(mid, HJlvl):
    if GLlvl:
        url='http://api.bilibili.com/x/space/acc/info?mid='+str(mid)
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.4324.182 Safari/537.36",
        }
        res = requests.get(url=url,headers=header)
        resback=json.loads(res.text)
        usrinfo=resback.get('data')
        try:
            usrlvl=usrinfo.get('level')
        except:
            #print(res.text)
            printp('获取UID:'+str(mid)+'的等级信息出错，请自行查看!')
            return True
        if usrlvl<HJlvl:
            printp('[UID:'+str(mid)+' 等级过低('+str(usrlvl)+'/'+str(HJlvl)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def linktodyid(dyid):
    #转换t.bilibili.com格式链接为动态id
    if "t.bilibili.com/" in dyid:
        dyid, sep, tail = dyid.partition('?')
        dyid=dyid[dyid.rfind('/'):]
        head, sep, dyid = dyid.partition('/')
        return dyid
    else:
        return dyid

def clicked():
    btn['state']=DISABLED
    global cjthread
    btn.configure(text="进行中…",bg='ivory')
    cjthread=threading.Thread(target=clicked0,args=())
    cjthread.start()
    thread2=threading.Thread(target=checkthread,args=(cjthread,))
    thread2.start()

def checkthread(thread):
    global notime
    while True:
        if not thread.is_alive():
            break
        time.sleep(0.1)
    if not barval==100:
        bar.stop()
    bar['value']=barval
    #bar['value']=100
    barp.configure(text=str(int(bar['value']))+'%')
    btn['state']=NORMAL
    btn.configure(text="开始抽奖!",bg='deepskyblue')

def BarProgress(num):
    global barval
    bar['value']=barval
    while True:
        #print(barval)
        if bar['value']<num:
            bar.start(2)
        else:
            bar.stop()
            break
        barp.configure(text=str(int(bar['value']))+'%')
        time.sleep(0.01)
        barval=bar['value']
    bar['value']=barval

def checkTJ(dycont):
    ZF=''
    PL=''
    DZ=''
    GZ=''
    if '转' in dycont or '转发' in dycont:
        ZF='转'
    if '评' in dycont or '评论' in dycont or '留言' in dycont:
        PL='评'
    if '赞' in dycont or '点赞' in dycont:
        DZ='赞'
    if '关' in dycont or '关注' in dycont:
        if not '关于' in dycont and '关注' in dycont:
            GZ='关'
    TJ='['+ZF+PL+DZ+GZ+']'
    if CHKCJDT(dycont):
        if not TJ=='[]':
            return TJ+'(可能)'
        else:
            return '[未知]'
    else:
        return '(可能不是抽奖)'

def CHKCJDT(dycont):
    cjkw1='抽' in dycont and '奖' in dycont
    cjkw2='抽' in dycont and '送' in dycont
    cjkw3='关' in dycont and '转' in dycont
    cjkw4='转' in dycont and '评' in dycont
    cjkw5='转' in dycont and '留言' in dycont
    cjkwall=cjkw1 or cjkw2 or cjkw3 or cjkw4 or cjkw5
    return cjkwall

def clicked0():
    #程序开始运行
    global notime
    global dyid
    global dyinfo
    global myuid
    global cookie
    global cookiepath
    global TGZ
    global RZtxt
    global EnaRZ
    global RZOFF
    global rzpath
    global GLCJH
    global GLlvl
    global barval
    bar['value']=0
    barval=0
    barp.configure(text='0%')
    btn4.state(['disabled'])
    #print()
    TZF=bool(chk1_state.get())
    TPL=bool(chk2_state.get())
    TDZ=bool(chk3_state.get())
    TGZ=bool(chk4_state.get())
    TRZ=bool(chk5_state.get())
    global NEEDAT
    NEEDAT=bool(chk7_state.get())
    if True:#chk6_state.get():
        output['state']='normal'
        output.delete(1.0, END)
        output['state']='disabled'
    if txt.get()=='':
        tkinter.messagebox.showwarning("提示", '需要输入动态链接/ID的嗷！')
        return False
    try:
        dyid=linktodyid(txt.get())
        dyid=int(dyid)
    except:
        tkinter.messagebox.showwarning("提示", '输入的动态ID/链接不正确呢！')
        #printp('')
        return False
    if len(str(dyid))<18:
        tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够呢 ('+str(len(str(dyid)))+'/'+'18) ！')
        return False
    LBGZ=[]
    LBZF=[]
    LBPL=[]
    LBDZ=[]
    errortime=1
    notime=False
    isLogin=False
    EnaRZ=False
    RZOFF=False
    notime=True
    if not TGZ and not TZF and not TPL and not TDZ:
        tkinter.messagebox.showwarning("提示", '需要至少选中一个获奖条件呢！')
        #printp()
        return False
    if TGZ and not TZF and not TPL and not TDZ:
        tkinter.messagebox.showwarning("提示", '还需要选择除了关注以外的任一获奖条件嗷！')
        #printp()
        return False
    try:
        HJNUM=int(spin.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的获奖者数量没有意义呢！')
        return False
    if HJNUM<1:
        tkinter.messagebox.showwarning("提示",'输入的获奖者数量小于1，这是不想让小伙伴抽中？')
        return False
    try:
        HJlvl=int(spin3.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的最低等级没有意义呢！')
        return False
    if HJlvl<0 or HJlvl>6:
        tkinter.messagebox.showwarning("提示",'输入的最低等级小于0或大于6！请不要调戏我呢…')
        return False
    try:
        CJHnum=int(spin2.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的过滤抽奖号的值没有意义嗷！')
        return False
    if CJHnum<-1 or CJHnum>10:
        tkinter.messagebox.showwarning("提示",'输入的过滤抽奖号的值小于-1或大于10！请不要调戏我呢…')
        return False
    if TRZ:
        TimeSt=time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
        rzpath='抽奖记录'+TimeSt+'.txt'
        RZtxt = open(rzpath,'a')
        printp('记录文件将保存在:'+rzpath)
        EnaRZ=True
    else:
        EnaRZ=False
    printp(updinfo)
    #bar['value']=10
    if not TGZ:
        bar.start(2)
        barval=0
        BarProgress(10)
    TZF2=repBool(TZF)
    TPL2=repBool(TPL)
    TDZ2=repBool(TDZ)
    TGZ2=repBool(TGZ)
    printp('转发：'+str(TZF2)+' 评论：'+str(TPL2)+' 点赞：'+str(TDZ2)+' 关注：'+str(TGZ2)+'\n最低等级：'+str(HJlvl)+' 抽奖号阈值：'+str(CJHnum))
    if CJHnum!=-1:
        GLCJH=True
    else:
        GLCJH=False
    if HJlvl!=0:
        GLlvl=True
    else:
        GLlvl=False
    notime=False
    if TGZ:
        try:
                cook=open('cookie.txt','r')
                cookie=cook.read()
                cook.close()
                cookiepath='cookie.txt'
        except:
            try:
                cookiepath=askopenfilename(title='选择一个包含cookie的文本文件',initialdir=os.path.dirname(os.path.realpath(sys.argv[0])), filetypes=[('Cookie File','*.txt')])
                cook=open(cookiepath,'r')
                cookie=cook.read()
                cook.close()
            except:
                notime=True
                printp('检测关注需要登录，请点击“登录/Cookie操作”按钮进行登录！')
                #printp('假如还没有自己的cookie的话，可以运行附带的\ngetcookie.exe 或在浏览器打开 t.bili.fan 就能获取')
                return False
        bar.start(2)
        barval=0
        BarProgress(10)
        cook=open(cookiepath,'r')
        cookie=cook.read()
        cook.close()
        if 'ENCRYPTED\n' in cookie:
            #decrycook(cookiepath)
            notime=True
            tkinter.messagebox.showwarning("提示",'需要解密cookie文件！')
            printp('请将cookie文件解密后重试!')
            decrycook(cookiepath)
            return False
        notime=True
        #bar['value']=20
        BarProgress(20)
        printp('尝试使用预设的cookie进行模拟登录……')
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        "Cookie":cookie,
        }
        r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header).text
        userinfo_dict=json.loads(r)
        try:
            jdata=userinfo_dict['data']
            myuid=jdata.get('mid')
            name=jdata.get('name')
            level=jdata.get('level')
            coins=jdata.get('coins')
            if DisplayLogInfo:
                printp('模拟登录成功，UID:'+str(myuid)+'，详情如下\n用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
            else:
                printp('模拟登录成功，UID:'+str(myuid)+'，用户名：'+name)                
            isLogin=True
        except:
            printp('模拟登录失败，可能是cookie过期或未登录，请重新获取cookie!')
            return False
    #dyid=input('输入动态ID：')
    #bar['value']=30
    BarProgress(30)
    dyid=str(dyid)
    notime=False
    printp('正在获取动态详情……')
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        }
        url='https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+dyid
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        dyinfo=resback.get('data')
        if TGZ and dyinfo.get('card').get('desc').get('user_profile').get('info').get('uid')!=myuid:
            notime=True
            printp('动态发送者('+dyinfo.get('card').get('desc').get('user_profile').get('info').get('uname')+')和当前已登录用户不一致!')
            return False
        tmstmp=time.localtime(dyinfo.get('card').get('desc').get('timestamp'))
        notime=True
        printp('-------------------------------------------')
        printp('动态ID:'+dyid+' '+checkTJ(dyinfo['card']['card']))
        printp('动态发送者：'+str(dyinfo['card']['desc']['user_profile']['info']['uname'])+'\n浏览：'+str(dyinfo['card']['desc']['view'])+'，转发：'+str(dyinfo['card']['desc']['repost'])+'，评论：'+str(dyinfo['card']['desc']['comment'])+'，点赞：'+str(dyinfo['card']['desc']['like']))
        printp('发送时间：'+time.strftime("%Y-%m-%d %H:%M:%S", tmstmp))
        printp('-------------------------------------------')
        #抽奖条件：'+str())+'|
        #print(dyinfo)
        try:
            lottdata=json.loads(dyinfo['card']['extension']['lott'])
            printp('此动态已经存在官方抽奖功能!抽奖ID:'+str(lottdata['lottery_id']))
            return False
        except:
            pass
        notime=False
    except Exception as e:
        SHEXIT=False
        try:
            if TGZ and dyinfo.get('card').get('desc').get('user_profile').get('info').get('uid')!=myuid:
                SHEXIT=True
        except:
            pass
        if SHEXIT:
                return False
        notime=True
        printp('获取出错，可能是动态链接/ID输入有误，请检查\n详细报错如下：\n'+str(repr(e))+'\n获取到的信息：\n'+res.text)
        return False
    if not isLogin:
        myuid=dyinfo.get('card').get('desc').get('user_profile').get('info').get('uid')
    printp('准备开始抽取……\n(抽取时将自动过滤UP主自己和重复转发/评论的用户)')
    #bar['value']=40
    notime=True
    if TZF and dyinfo['card']['desc']['repost']>575:
        printp('警告：转发数量超过550的部分可能无法被完全统计!')
    printp('')
    Error=False
    BarProgress(40)
    if TZF:
        if dyinfo['card']['desc']['repost']==0:
            printp('这条动态没有任何用户转发!')
            Error=True
        if dyinfo['card']['desc']['repost']>600:
            printp('转发限制在600次以内!')
            Error=True
        if HJNUM>dyinfo['card']['desc']['repost']:
            printp('设置的获奖者总数大于这条动态的转发数!')
            Error=True
    if TPL:
        if dyinfo['card']['desc']['comment']==0:
            printp('这条动态没有任何用户评论!')
            Error=True
        if dyinfo['card']['desc']['comment']>1000:
            printp('评论限制在1000条以内!')
            Error=True
        if HJNUM>dyinfo['card']['desc']['comment']:
            printp('设置的获奖者总数大于这条动态的评论数!')
            Error=True
    if TDZ:
        if dyinfo['card']['desc']['like']==0:
            printp('这条动态没有任何用户点赞!')
            Error=True
        if dyinfo['card']['desc']['like']>2000:
            printp('点赞限制在2000个以内!')
            Error=True
        if HJNUM>dyinfo['card']['desc']['like']:
            printp('设置的获奖者总数大于这条动态的点赞数!')
            Error=True
    if Error:
        return False
    LBALL=[]
    notime=False
    #BarProgress(40)
    if TZF:
        ZFp=15
        LBZF=getZF(dyid)
        try:
            if not LBZF:
                return False
        except:
            pass
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBZF)
        else:
            LBALL=set(LBZF)
    #bar['value']=50
    BarProgress(55)
    if TPL:
        PLp=15
        LBPL=getPL(dyid)
        try:
            if not LBPL:
                return False
        except:
            pass
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBPL)
        else:
            LBALL=set(LBPL)
    #bar['value']=60
    BarProgress(70)
    if TDZ:
        DZp=15
        LBDZ=getDZ(dyid)
        try:
            if not LBDZ:
                return False
        except:
            pass
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBDZ)
        else:
            LBALL=set(LBDZ)
    #bar['value']=70
    BarProgress(85)
    notime=True
    printp('')
    notime=False
    printp('已获取到符合要求的参与者数量为：'+str(len(list(LBALL))))
    notime=True
    if HJNUM>len(list(LBALL)) or HJNUM<1:
        printp('输入的获奖者数量('+str(HJNUM)+')超出范围!')
        return False
    HJMD=[]
    times=1
    lba=len(LBALL)
    while True:
        while True:
            if not len(LBALL) < HJNUM:
                HJuser=secrets.choice(list(LBALL))#这句是核心功能之一，随机从参与者数组里抽一位
                if not HJuser in HJMD:
                    if checkGZ(HJuser) and checkCJH(HJuser,CJHnum) and checklvl(HJuser,HJlvl):
                        HJMD.append(HJuser)
                        #LBALL.remove(HJuser)
                        #printp('[抽到UID:'+str(HJuser)+']')
                        times=times+1
                    #else:
                    LBALL.remove(HJuser)
                    #print(len(LBALL))
                break
            else:
                printp('')
                printp('警告：参与者列表人数已小于设定的获奖者数量!\n建议：修改或取消抽奖号过滤值，取消部分获奖条件')
                return False
        if times>HJNUM:
            break
        '''if len(HJMD)!=0:
            BarProgress(85+13*len(HJMD)/HJNUM)'''
        numz1=lba-len(LBALL)
        numz2=numz1/lba
        BarProgress(85+13*numz2)
    #bar['value']=90
    BarProgress(98)
    HJMD.sort()
    random.shuffle(HJMD)
    notime=False
    printp('抽取完成！\n获奖名单：(以UID为准)')
    notime=True
    printp('-------------------------------------------')
    getname(HJMD)
    printp('-------------------------------------------')
    #printp('程序即将退出……')
    #bar['value']=100
    btn4['state']=NORMAL
    barval=100
    if NEEDAT:
        #print(ATuser)
        ATmsg0=str(ATuser).replace('[','')
        ATmsg1=ATmsg0.replace(']','')
        ATmsg2=ATmsg1.replace(',',' ')
        ATmsg3=ATmsg2.replace("'",'')
        #print(ATmsg3)
        ATmsg=ATmsg3
        pyperclip.copy(ATmsg)
        printp('已复制at信息，可直接粘贴到动态编辑框')
    printp('提示:可以使用Win+Shift+S快速进行窗口截图')
    notime=False
    return True

def clicked2():
    #关于窗口
    tkinter.messagebox.showinfo("关于", 'B站动态抽奖工具 Python GUI版 '+version+'\n更新日期: '+updatetime+'\nBy: 芍芋\nWebsite: https://shoyu.top')

def clicked3():
    global login1window
    global login2window
    global login3window
    login1window = Toplevel(window)
    login1window.title('登录/Cookie操作')
    login1window.configure(bg='white')
    width = 270
    heigh = 100#136
    screenwidth = login1window.winfo_screenwidth()
    screenheight = login1window.winfo_screenheight()-50
    login1window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login1window.resizable(0,0)
    try:
        login1window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(login1window)
        except:
            pass
    logbtn1 = ttk.Button(login1window, text="登录/获取Cookie", command=clicked4)
    logbtn1.place(x=10, y=12)
    logbtn2 = ttk.Button(login1window, text="退出登录/注销Cookie", command=clicked5)
    logbtn2.place(x=127, y=12)
    logbtn3 = ttk.Button(login1window, text="   加密Cookie   ", command=clicked6)
    logbtn3.place(x=10, y=52)
    logbtn4 = ttk.Button(login1window, text="     "+repBool2(bool(1-DisplayLogInfo))+"登录细节     ", command=lambda:clicked10(logbtn4))#clicked10(loginlbl1))
    logbtn4.place(x=127, y=52)
    '''loginlbl1 = Label(login1window, text=repBool(DisplayLogInfo))
    loginlbl1.configure(bg='white')
    loginlbl1.place(x=255, y=53)'''
    login1window.lift()
    login1window.grab_set()
    login1window.mainloop()

def clicked4():
    login1window.destroy()
    url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
    #print('获取扫码登录请求……')
    response = requests.get(url)
    content = response.text
    json_dict = json.loads(content)
    jdata = json_dict['data']
    oauthlink = jdata.get('url')
    oauthkey = jdata.get('oauthKey')
    qr = qrcode.QRCode(version=5, error_correction=(qrcode.constants.ERROR_CORRECT_M), box_size=6, border=4)
    qr.add_data(oauthlink)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('qrcode.png')
    login2window = Toplevel(window)
    login2window.title('使用B站客户端扫描登录')
    width = 300
    heigh = 300
    screenwidth = login2window.winfo_screenwidth()
    screenheight = login2window.winfo_screenheight()-50
    login2window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login2window.resizable(0,0)
    login2window.configure(bg='white')
    try:
        login2window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(login2window)
        except:
            pass
    photo = PhotoImage(file='qrcode.png')
    w = Label(login2window, image=photo)
    w.pack()
    os.unlink('qrcode.png')
    #_thread.start_new_thread(chklog,(oauthkey,login2window))
    thread = threading.Thread(target=chklog,args=(oauthkey,login2window))
    thread.start()
    login2window.grab_set()
    login2window.mainloop()

def clicked5():
    login1window.destroy()
    cookiepath=''
    #if cookiepath=='':'''
    try:
        if os.path.exists('cookie.txt'):
            Isuse=tkinter.messagebox.askyesno("提示", '确认注销当前目录下的cookie？')
            if Isuse:
                cookiepath='cookie.txt'
        if cookiepath=='':
            cookiepath=askopenfilename(title='选择一个包含cookie的文本文件',initialdir=os.path.dirname(os.path.realpath(sys.argv[0])), filetypes=[('Cookie File','*.txt')])
        cook=open(cookiepath,'r')
        cookie=cook.read()
        cook.close()
    except:
        tkinter.messagebox.showwarning("提示",'需要提供cookie才能注销掉呢……')
        return False
    #try:
    if 'ENCRYPTED\n' in cookie:
        #decrycook(cookiepath)
        notime=True
        tkinter.messagebox.showwarning("提示",'请先将cookie文件解密！')
        decrycook(cookiepath)
        return False
    cookies_dict={}
    cookies = cookie.split(";")
    for co in cookies:
        co = co.strip()
        p = co.split('=')
        value = co.replace(p[0]+'=', '').replace('"', '')
        cookies_dict[p[0]]=value
    #print(cookies_dict)
    csrftoken=cookies_dict['bili_jct']
    url="http://passport.bilibili.com/login/exit/v2"#+oauthkey
    data={
    "biliCSRF":csrftoken,
    }
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    "Cookie":cookie,
    }
    response=requests.post(url, headers=header, data=data)
    content=response.text
    try:
        json_dict = json.loads(content)
        jdata = json_dict
    except:
        tkinter.messagebox.showwarning("提示",'注销失败，可能是cookie无效、已过期或已注销！')
        return False
    if jdata['code']==0:
        if cookiepath=='cookie.txt':
            try:
                os.unlink('cookie.txt')
            except:
                pass
        tkinter.messagebox.showinfo("提示",'文件包含的cookie已经成功从服务器上注销！')
        return True
    else:
        tkinter.messagebox.showwarning("提示",'注销cookie时出现其他错误！('+str(jdata['code'])+')')
        return False

def clicked6():
    global login3window
    global txt2
    global cookiez
    global cookiepathz
    login1window.destroy()
    cookiepathz=''
    try:
        if os.path.exists('cookie.txt'):
            cookiepathz='cookie.txt'
        if cookiepathz=='':
            cookiepathz=askopenfilename(title='选择一个包含cookie的文本文件',initialdir=os.path.dirname(os.path.realpath(sys.argv[0])), filetypes=[('Cookie File','*.txt')])
        cook=open(cookiepathz,'r')
        cookiez=cook.read()
        cook.close()
    except:
        tkinter.messagebox.showwarning("提示",'需要提供cookie才能加密呢……')
        return False
    cook=open(cookiepathz,'r')
    cookiez=cook.read()
    cook.close()
    if 'ENCRYPTED\n' in cookiez:
        tkinter.messagebox.showwarning("提示",'这个cookie已经加密过了！')
        return False
    login3window = Toplevel(window)
    login3window.title('输入加密用密码')
    width = 280
    heigh = 90
    screenwidth = login3window.winfo_screenwidth()
    screenheight = login3window.winfo_screenheight()-50
    login3window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login3window.resizable(0,0)
    login3window.configure(bg='white')
    try:
        login3window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(login3window)
        except:
            pass
    txt2 = ttk.Entry(login3window, width=36)
    txt2.place(x=11, y=10)
    btn = ttk.Button(login3window, text="确定", command=clicked7)
    btn.place(x=96, y=50)
    login3window.lift()
    login3window.grab_set()
    login3window.mainloop()

def clicked7():
    key=txt2.get()
    #print(key)
    if key=='':
        key='Bili-Shoyu'
    login3window.destroy()
    ret=rc4.encrypt_str(cookiez,key)
    #print(ret)
    outtxt = open(cookiepathz, 'w')
    outtxt.write('ENCRYPTED\n'+ret)
    outtxt.close()
    tkinter.messagebox.showinfo('提示','已将该cookie加密！')

def decrycook(cookiepath):
    global login4window
    global cookiepathy
    global txt3
    cookiepathy=cookiepath
    login4window = Toplevel(window)
    login4window.title('输入解密用密码')
    login4window.configure(bg='white')
    width = 280
    heigh = 90
    screenwidth = login4window.winfo_screenwidth()
    screenheight = login4window.winfo_screenheight()-50
    login4window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login4window.resizable(0,0)
    #login4window.configure(bg='white')
    try:
        login4window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(login4window)
        except:
            pass
    txt3 = ttk.Entry(login4window, width=36)
    txt3.place(x=11, y=10)
    btn = ttk.Button(login4window, text="确定", command=clicked8)
    btn.place(x=96, y=50)
    login4window.lift()
    login4window.grab_set()
    #login4window.mainloop()

def clicked8():
    key=txt3.get()
    #print(key)
    if key=='':
        key='Bili-Shoyu'
    login4window.destroy()
    try:
        ret=rc4.decrypt_str(linecache.getline(cookiepathy,2),key)
        #print(ret)
    except:
        tkinter.messagebox.showwarning('提示','密码有误！')
        return False
    tkinter.messagebox.showiinfo('提示','已将该cookie解密！')
    #IsSave=tkinter.messagebox.askyesno('提示','已将该cookie解密！是否需要保存？')
    #if IsSave:
    outtxt = open(cookiepathy, 'w')
    outtxt.write(ret)
    outtxt.close()

def chklog(oauthkey,win):
    while True:
        if win.winfo_exists():
            url="http://passport.bilibili.com/qrcode/getLoginInfo"#+oauthkey
            data = {'oauthKey': oauthkey}
            session = requests.session()
            sessret=session.post(url, data)
            content=sessret.text
            json_dict = json.loads(content)
            jdata = json_dict
            if jdata['data']==-5:
                win.title('请在客户端确认登录！')
            elif jdata['data']==-2:
                win.destroy()
                tkinter.messagebox.showwarning('提示','二维码已过期，请刷新！')
                break
            else:
                try:
                    if jdata['code']==0:
                        html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
                        cookie = jsonDataToUrlParams(html_set_cookie)
                        outtxt = open('cookie.txt', 'w')
                        outtxt.write(cookie)
                        outtxt.close()
                        win.destroy()
                        tkinter.messagebox.showinfo('提示','已将cookie写入同一目录下的cookie.txt！')
                except:
                        pass
        else:
            break
        time.sleep(3)

'''def changelink(files):
    txt.delete(0,END)
    txt.insert(END,files)
    print(files)'''

def clicked9():
    #print(output.get(1.0,END))
    TimeSt=time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
    rzpath='抽奖记录'+TimeSt+'.txt'
    RZtxt = open(rzpath,'a')
    RZtxt.write(output.get(1.0,END))
    RZtxt.close()
    tkinter.messagebox.showinfo("提示",'抽奖记录已保存为：'+rzpath)

def clicked10(btn):
    global DisplayLogInfo
    DisplayLogInfo=bool(1-DisplayLogInfo)
    DPLI2=repBool2(DisplayLogInfo)
    #tkinter.messagebox.showinfo("提示",'已切换为：'+DPLI2)
    btn.configure(text='     '+repBool2(bool(1-DisplayLogInfo))+'登录细节     ')
    login1window.update()

window = Tk()#初始化一个窗口
window.title('B站动态抽奖工具 Python GUI版 '+version+' '+updatetime+' By: 芍芋')#标题
window.configure(bg='white')#背景颜色
#window.geometry("820x300")

#窗口居中实现
width = 690 #720 Linux
heigh = 450 #530 Linux
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()-50
window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
window.resizable(0,0)#设置禁止调整窗口大小
#定义图标
try:
    window.iconbitmap('icon.ico')
except:
    try:
        setIcon(window)
    except:
        pass

style= ttk.Style()
style.configure("TCheckbutton", background="white")
style.configure("cj.TButton", background="white",height=8,width=40)

#定义文本
lbl1 = Label(window, text="在下方输入动态链接或者动态ID (使用Ctrl+V粘贴)")
lbl1.place(x=10, y=10)
lbl1.configure(bg='white')
txt = ttk.Entry(window, width=40)
txt.place(x=10, y=35)
#txt.focus()
lbl2 = Label(window, text="选择一下抽奖条件吧")
lbl2.place(x=10, y=70)
lbl2.configure(bg='white')
#定义复选框
chk1_state = BooleanVar()
chk1_state.set(True) # Set check state
chk1 = ttk.Checkbutton(window, text="转发", var=chk1_state)#, onvalue=1, offvalue=0)
chk1.place(x=10, y=92)
chk2_state = BooleanVar()
chk2_state.set(False) # Set check state
chk2 = ttk.Checkbutton(window, text="评论", var=chk2_state)
chk2.place(x=90, y=92)
chk3_state = BooleanVar()
chk3_state.set(False) # Set check state
chk3 = ttk.Checkbutton(window, text="点赞", var=chk3_state)
chk3.place(x=170, y=92)
chk4_state = BooleanVar()
chk4_state.set(False) # Set check state
chk4 = ttk.Checkbutton(window, text="关注", var=chk4_state)
chk4.place(x=250, y=92)
spin = Spinbox(window, from_=1, to=999, width=5)
spin.place(x=70, y=152)
spin.configure(bg='white')
#spin.set(1)
var = StringVar(window)
spin2 = ttk.Combobox(window, width=4, textvariable=var)
spin2['values']=(-1,0,1,2,3,4,5,6,7,8,9,10)
spin2.place(x=245, y=152)
var2 = StringVar(window)
spin3 = ttk.Combobox(window, width=4, textvariable=var2)
spin3['values']=(0,1,2,3,4,5,6)
spin3.place(x=70, y=194)
spin2.current(0)
spin3.current(0)
chk7_state = BooleanVar()
chk7_state.set(True) # Set check state
chk7 = ttk.Checkbutton(window, text="自动复制@信息", var=chk7_state)
chk7.place(x=10, y=240)
chk5_state = BooleanVar()
chk5_state.set(False) # Set check state
chk5 = ttk.Checkbutton(window, text="保存抽奖记录", var=chk5_state)
chk5.place(x=10, y=265)
'''chk6_state = BooleanVar()
chk6_state.set(True) # Set check state
chk6 = ttk.Checkbutton(window, text="自动清空记录", var=chk6_state)
chk6.place(x=10, y=240)'''
btn2 = ttk.Button(window, text="关于本程序", command=clicked2)
btn2.place(x=213, y=253)
#btn2.configure(style="TButton")
btn4 = ttk.Button(window, text=" 保存当前记录 ", command=clicked9)
btn4.place(x=10, y=295)
btn3 = ttk.Button(window, text="登录/Cookie操作", command=clicked3)
btn3.place(x=196, y=295)
#btn3.configure(style="TButton")
btn = Button(window, text="开始抽奖!", command=clicked)
btn.place(x=10, y=340)
btn.configure(bg='deepskyblue',height=2,width=40)
lbl3 = Label(window, text="获奖人数")
lbl3.place(x=10, y=150)
lbl3.configure(bg='white')
lbl4 = Label(window, text="过滤抽奖号(0-10)")
lbl4.place(x=140, y=150)
lbl4.configure(bg='white')
lbl5 = Label(window, text="注: 评论获取不包括楼中楼")#\n抽取时如果数据过多可能会出现无响应，耐心等待即可~")
lbl5.place(x=10, y=116)
lbl5.configure(bg='white')
lbl6 = Label(window, text="最低等级")#\n(0-6)")
lbl6.place(x=10, y=193)
lbl6.configure(bg='white')
lbl7 = Label(window, text="值越小越严格,-1=无")
lbl7.place(x=186, y=175)
lbl7.configure(bg='white')
output = scrolledtext.ScrolledText(window, width=48, height=31, relief="solid")
output.place(x=315, y=17)
output['state']='disabled'
bar = Progressbar(window, length=250)#290)
bar.place(x=10, y=402)
bar['value']=0
barp = Label(window, text="0%")
barp.place(x=268, y=401)
barp.configure(bg='white')
btn4.state(['disabled'])
#chk6.state(['disabled'])
#显示窗口

DisplayLogInfo=True
chkupdwindow = Toplevel(window)
chkupdwindow.title('检查更新')
chkupdwindow.configure(bg='white')
width = 300
heigh = 100
screenwidth = chkupdwindow.winfo_screenwidth()
screenheight = chkupdwindow.winfo_screenheight()-50
chkupdwindow.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
chkupdwindow.resizable(0,0)
try:
    chkupdwindow.iconbitmap('icon.ico')
except:
    try:
        setIcon(chkupdwindow)
    except:
        pass
chklbl1 = Label(chkupdwindow, text="正在获取版本信息…", justify="center")
chklbl1.configure(bg='white')
chklbl1.place(relx = 0.5, rely = 0.4, anchor = "center")
chkupdthread=threading.Thread(target=chkupd,args=())
chkupdthread.start()
#windnd.hook_droptext(window, func=changelink)
#chkupdwindowIsOpen=True
#chkupdwindowIsOpen=False

window.mainloop()
