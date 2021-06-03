import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.filedialog import (askopenfilename,askopenfilenames,asksaveasfilename)#askdirectory,
import requests #外置库 需要使用pip install requests安装
import json
import linecache
import sys,os
import time
import math
import re
import random
import qrcode #外置库 需要使用pip install qrcode,pip install Pillow和pip install Image安装，py3.4版本及以下不支持
import tkinter.messagebox
from datetime import datetime,timedelta
import secrets
#import _thread
import threading
import pyperclip #外置库 需要使用pip install pyperclip安装，py3.4版本及以下不支持
#上方代码导入所有需要的库

import base64
try:
    from iconwin import img
    import rc4
except:
    pass
#打包成exe所需的库

version='1.3.3.024'
updatetime='2021-06-03'

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
    output.see(tk.END)
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

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

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
        r=requests.get('http://api.github.com/repos/shoyu3/DynamicRaffle-Python/releases/latest',headers=header)
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
                if pform=='win':
                    os.system('start '+gitreturn['html_url'])
                else:
                    tkinter.messagebox.showinfo("提示",'非windows平台请手动在浏览器打开项目地址下载更新！\n'+gitreturn['html_url'])
            updinfo='有新版本可用！('+gitversion+' > '+version+')'
        else:
            try:
                chklbl1.configure(text='当前版本已是最新！(~￣▽￣)~')
            except:
                pass
            time.sleep(0.8)
            updinfo='当前版本已是最新！('+version+')'
        if not cjthread.is_alive():
            printp(updinfo)
    except:
        try:
            chklbl1.configure(text='检测更新时出现了问题…o(TヘTo)')#!呜呜呜
        except:
            pass
        time.sleep(0.8)
        updinfo='检测更新时出现了问题……'
        printp(updinfo)
        #print('当前版本已是最新！')
    chkupdwindow.destroy()

httpsession = requests.session()

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
            html = httpsession.get(url, headers=header, timeout=5)
            html.encoding = "utf-8"
            return html.text
        except requests.exceptions.RequestException:
            printp('警告：超时'+str(i+1)+'次')
            i += 1

#=============================================================#
#部分代码思路参考项目：https://github.com/LeoChen98/BiliRaffle#
#=============================================================#

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

def getZF(dyn_id,*_Chong_Fu_):
    global RZOFF
    global ZFidDict,ZFcontDict
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
    data = httpsession.get(dynamic_api, headers=header, params=param, timeout=10)
    data.encoding='utf-8'
    data_json = json.loads(data.text)
    if data_json['code']==-412:
        notime=True
        outrb()
        printp('获取转发失败，调取间隔过短，请过一段时间再试吧~')
        notime=False
        return False
    total_num = data_json['data']['total']
    info['total'] = total_num
    # 获取全部数据
    uidall={}
    now_num = 0
    count = 0
    ZFidDict={}
    ZFcontDict={}
    #users = []
    while now_num < total_num:  # 循环获取页面
        param = {'dynamic_id': dyn_id, 'offset': offset}
        data = httpsession.get(dynamic_api, headers=header, params=param)
        data.encoding='utf-8'
        data_json = json.loads(data.text)
        #print(len(str(data_json)))
        #print(data_json['data']['items'][0]['desc']['user_profile']['info']['uname'])
        for i in range(0, 20):  # 获取单页的所有用户（最多20条）
            if count < total_num:
                count += 1
                try:
                    uid = data_json['data']['items'][i]['desc']['uid']
                    zfdyid=data_json['data']['items'][i]['desc']['dynamic_id']
                    uname = data_json['data']['items'][i]['desc']['user_profile']['info']['uname']
                    uidall[uid]=uname
                    #print(NeedIncludeKeyword[0],NeedIncludeKeyword)
                    if NeedIncludeKeyword[0] and not _Chong_Fu_:
                        #print(1)
                        dyn_card=json.loads(data_json['data']['items'][i]['card'])
                        #print(data_json['data']['items'][0])
                        ZFcontDict[uid]=dyn_card['item']['content']
                        '''for j in range(len(NeedIncludeKeyword[2])):
                            if not NeedIncludeKeyword[2][j] in dyn_card['item']['content']:
                                printp('[UID:'+str(uid)+' 未包含关键字中的第'+str(j+1)+'个，无效]')'''
                    if EnaSuoYin and not _Chong_Fu_:
                        ZFidDict[uid]=zfdyid
                    if _Chong_Fu_:
                        if not uid in ZFidDict.keys():
                            ZF_dyid_list=[]
                            ZF_dyid_list.append(zfdyid)
                        else:
                            ZF_dyid_list=ZFidDict[uid]
                            ZF_dyid_list.append(zfdyid)
                        ZFidDict[uid]=ZF_dyid_list
                    outrb()
                    curusr=len(uidall)
                    percent='%.2f' % float(curusr/total_num*100)
                    BarProgress(40+15*float(curusr/total_num))
                    printp(str(percent)+'% ('+str(curusr)+'/'+str(total_num)+')')
                except Exception as e:
                    print(repr(e))
                    pass
            else:  # 最后一页数量少于20时
                break
        offset = _get_offset(data_json)
        if offset is None:
            break
        now_num += 20
        #time.sleep(0.5)
    #uidall=list(set(uidall))
    #uidall.sort()
    if not _Chong_Fu_:
        try:
            del uidall[myuid]
        except:
            pass
    outrb()
    '''curusr=len(uidall)
    printp('100.00% ('+str(curusr)+'/'+str(curusr)+')')'''
    RZOFF=False
    #uidall=list(set(uidall))
    printp('完成，共收集到 '+str(len(uidall))+' 位用户')
    return uidall

def getPL(Dynamic_id,*_Chong_Fu_):
    global notime
    global RZOFF
    printp('正在获取完整评论列表……')
    current_page = 1
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/86.0.4324.182 Safari/537.36",
    }
    rid = dyinfo['card']['desc']['rid']
    old_rid=rid
    if dyn_type=='shipin':
        typnum=1
    elif dyn_type=='zhuanlan':
        typnum=12
    elif dyn_type=='xiangbu':
        typnum=11
    elif dyn_type=='yinpin':
        typnum=14
    elif dyn_type=='normal':
        typnum=17
        rid=Dynamic_id
    else:
        notime=True
        printp('动态类型有误！')
        notime=False
        return False
    link1 = 'http://api.bilibili.com/x/v2/reply?&jsonp=json&pn='
    link2 = '&type='+str(typnum)+'&oid='
    link3 = '&sort=2'#&_=1570498003332'
    global PLidDict,PLcontDict
    #comment_list = []
    userlist_1={}
    PLidDict={}
    PLcontDict={}
    #pool = {}
    r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
    json_data = json.loads(r)
    #print(json_data)
    '''if json_data['code']==-404:
        outrb()
        printp('正在获取完整评论列表……(模式二)')
        rid=Dynamic_id
        #print(rid)
        link2 = '&type=17&oid='
        r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
        json_data = json.loads(r)
        #print(json_data)
        if json_data['code']==-404:
            outrb()
            printp('正在获取完整评论列表……(模式三)')
            rid=old_rid
            #print(rid)
            link2 = '&type=1&oid='
            r = gethtml(link1 + str(current_page) + link2 + str(rid) + link3, header)
            json_data = json.loads(r)
            #print(json_data)
            '''
    if json_data['code']==-404:
        notime=True
        printp('获取评论失败，可能因为此动态没有除UP主自己的评论以外的评论呢')
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
        #print(len(str(json_data1)))
        if json_data1['data']['replies']:
            if EnaSuoYin and not _Chong_Fu_:
                for reply in json_data1['data']['replies']:
                    userlist_1[int(reply['member']['mid'])]=reply['member']['uname']
                    PLidDict[int(reply['member']['mid'])]=reply['rpid']
                    if NeedIncludeKeyword[1]:
                        print(reply['content']['message'])
                        PLcontDict[int(reply['member']['mid'])]=reply['content']['message']
                    outrb()
                    curusr=len(userlist_1)
                    percent='%.2f' % float(curusr/comments_num*100)
                    BarProgress(55+15*float(curusr/comments_num))
                    printp(str(percent)+'% ('+str(curusr)+'/'+str(comments_num)+')')
            elif _Chong_Fu_:
                for reply in json_data1['data']['replies']:
                    userlist_1[int(reply['member']['mid'])]=reply['member']['uname']
                    uid=int(reply['member']['mid'])
                    plrpid=reply['rpid']
                    if not uid in PLidDict.keys():
                        PL_rpid_list=[]
                        PL_rpid_list.append(plrpid)
                    else:
                        PL_rpid_list=PLidDict[uid]
                        PL_rpid_list.append(plrpid)
                    PLidDict[uid]=PL_rpid_list
                    #PLidDict[int(reply['member']['mid'])]=reply['rpid']
                    outrb()
                    curusr=len(userlist_1)
                    percent='%.2f' % float(curusr/comments_num*100)
                    BarProgress(55+15*float(curusr/comments_num))
                    printp(str(percent)+'% ('+str(curusr)+'/'+str(comments_num)+')')
            else:
                for reply in json_data1['data']['replies']:
                    userlist_1[int(reply['member']['mid'])]=reply['member']['uname']
                    outrb()
                    curusr=len(userlist_1)
                    percent='%.2f' % float(curusr/comments_num*100)
                    BarProgress(55+15*float(curusr/comments_num))
                    printp(str(percent)+'% ('+str(curusr)+'/'+str(comments_num)+')')
        current_page += 1
        if current_page > pages_num:
            break
    #userlist_1=list(set(userlist_1))
    #userlist_1.sort()
    if not _Chong_Fu_:
        try:
            del userlist_1[myuid]
        except:
            pass
    outrb()
    '''curusr=len(userlist_1)
    printp('100.00% ('+str(curusr)+'/'+str(curusr)+')')'''
    RZOFF=False
    if len(userlist_1)==0:
        notime=True
        printp('获取评论为空,可能因为此动态没有除UP主自己的评论以外的评论呢')
        notime=False
        return False
    #userlist_1=list(set(userlist_1))
    printp('完成，共收集到 '+str(len(userlist_1))+' 位用户')
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
    if userlist_dict['code']==-412:
        notime=True
        outrb()
        printp('获取点赞失败，调取间隔过短，请过一段时间再试吧~')
        notime=False
        return False
    jdata=userlist_dict['data']
    jlist=jdata['item_likes']
    totalfans=jdata.get('total_count')
    math2=math.ceil(jdata.get('total_count')/20)*20-totalfans
    pages=math.ceil(totalfans/20)
    times=1
    errortime=1
    userlist_1={}
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
                userlist_1[jlist[times2]['uid']]=jlist[times2]['uname']
                times2=times2+1
                outrb()
                curusr=len(userlist_1)
                percent='%.2f' % float(curusr/likes*100)
                printp(str(percent)+'% ('+str(curusr)+'/'+str(likes)+')')
        else:
            while times2<20-math2:
                userlist_1[jlist[times2]['uid']]=jlist[times2]['uname']
                times2=times2+1
                outrb()
                curusr=len(userlist_1)
                percent='%.2f' % float(curusr/likes*100)
                printp(str(percent)+'% ('+str(curusr)+'/'+str(likes)+')')
        BarProgress(70+15*float(curusr/likes))
        times=times+1
        time.sleep(0.1)
    #userlist_1=list(set(userlist_1))
    #userlist_1.sort()
    try:
        del userlist_1[myuid]
    except:
        pass
    notime=False
    outrb()
    RZOFF=False
    #userlist_1=list(set(userlist_1))
    printp('完成，共收集到 '+str(len(userlist_1))+' 位用户')
    return userlist_1

'''def getname_old(users):
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
        times=times+1'''

def getname(users,userdict):
    global ATuser
    if NEEDAT:
        ATuser=[]
    '''userdict2={}
    print(userdict)
    for j in range(len(userdict)):
        print(userdict2,j)
        userdict2[str(list(userdict.keys())[j])]=list(userdict.values())[j]'''
    times=1
    for i in users:
        uname=userdict[i]
        printp(str(times)+' '+uname+' (UID:'+str(i)+')')
        tiao_jian=bool(chk2_state.get()) or bool(chk1_state.get())
        if EnaSuoYin and tiao_jian:
            try:
                printp('>>对应动态链接：https://t.bilibili.com/'+str(ZFidDict[i]))
            except:
                pass
            try:
                printp('>>对应评论链接：https://t.bilibili.com/'+str(dyid)+'#reply'+str(PLidDict[i]))
            except:
                pass
            if times!=len(users):
                printp('-------------------------------------------')
        if NEEDAT:
            ATuser.append('@'+uname)
        times+=1

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
        try:
            be_relation=rinfo['be_relation']['attribute']
        except:
            #print(res.text)
            printp('获取UID:'+str(mid)+'的关注状态出错，请自行查看!')
            return True
        if not be_relation==2 and not be_relation==6:
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
            printp('[UID:'+str(mid)+' 未关注自己('+str(be_relation)+')，无效]')
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
                try:
                    dycont2=json.loads(json.loads(dycont)['origin'])['item']['description']
                except:
                    try:
                        dycont2=json.loads(json.loads(dycont)['origin'])['item']['content']
                    except:
                        dycont2='(Empty)'
                if bool(CHKCJDT(dycont2)):
                    raffle_count=raffle_count+1
                #print(str(times)+'\n'+dycont2+'\n'+str(bool(CHKCJDT(dycont2)))+'\n---')
                times=times+1
        if raffle_count > condition:
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
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
        res.encoding='utf-8'
        resback=json.loads(res.text)
        usrinfo=resback.get('data')
        try:
            usrlvl=usrinfo.get('level')
        except:
            #print(res.text)
            printp('获取UID:'+str(mid)+'的等级信息出错，请自行查看!')
            return True
        if usrlvl<HJlvl:
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
            printp('[UID:'+str(mid)+' 等级过低('+str(usrlvl)+'/'+str(HJlvl)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def get_same_follow(vmid):
    same_follow_list=[]
    header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
    "Cookie":cookie,
    }
    r=requests.get('http://api.bilibili.com/x/relation/same/followings?pn=1&vmid='+str(vmid),headers=header)
    r.encoding='utf-8'
    try:
        jdata=json.loads(r.text)['data']
        total_num=jdata['total']
        pages=math.ceil(total_num/50)
        times=1
        while times<=pages:
            r=requests.get('http://api.bilibili.com/x/relation/same/followings?pn='+str(times)+'&vmid='+str(vmid),headers=header)
            r.encoding='utf-8'
            try:
                jlist=json.loads(r.text)['data']['list']
                for i in range(len(jlist)):
                    same_follow_list.append(jlist[i]['mid'])
            except:
                pass
            times+=1
    except:
        pass
    same_follow_list.sort()
    #print(same_follow_list)
    return same_follow_list

def checkSameFollow(mid):
    if NeedFollowOther:
        sflist=get_same_follow(mid)
        nfol=[ int(x) for x in NeedFollowOtherList ]
        '''print(nfol)
        print(sflist)
        print(set(nfol).issubset(sflist))'''
        if not set(nfol).issubset(sflist):
            not_follow_list=list(set(nfol)-set(sflist))
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
            printp('[UID:'+str(mid)+' 未关注指定用户中的'+','.join(not_follow_list)+'，无效]')
            return False
        else:
            return True
    else:
        return True
        
def checkZBJ(mid):
    if NeedHaveLiveRoom:
        url='http://api.bilibili.com/x/space/acc/info?mid='+str(mid)
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.4324.182 Safari/537.36",
        }
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        usrinfo=resback.get('data')
        try:
            usrlroom=usrinfo['live_room']['roomStatus']
            usrlroom2=usrinfo['live_room']['roomid']
        except:
            #print(res.text)
            printp('获取UID:'+str(mid)+'的直播间信息出错，请自行查看!')
            return True
        if usrlroom==0:
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
            printp('[UID:'+str(mid)+' 未开通直播间('+str(usrlroom)+','+str(usrlroom2)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def checkZhuangBan(mid):
    if NeedHaveGarb:
        url='https://app.biliapi.net/x/v2/space/garb/list?pn=1&ps=200&vmid='+str(mid)
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/75.0.4324.182 Safari/537.36",
        }
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        usrinfo=resback.get('data')
        try:
            usrfanscount=usrinfo['count']
        except:
            print(res.text)
            printp('获取UID:'+str(mid)+'的装扮信息出错，请自行查看!')
            return True
        if usrfanscount==0:
            if noDisplayUser1:
                asterisknum=len(str(mid))-3
                asterisks=''
                for i in range(asterisknum):
                    asterisks=asterisks+'*'
                mid=str(mid)[-10:][:1]+asterisks+str(mid)[-10:][-2:]
            printp('[UID:'+str(mid)+' 未拥有任何粉丝套装('+str(usrfanscount)+')，无效]')
            return False
        else:
            return True
    else:
        return True

def checkKW_1(mid):
    if not NeedIncludeKeyword[0]:
        return True
    if len(NeedIncludeKeyword[2])==0:
        return True
    for j in range(len(NeedIncludeKeyword[2])):
        if not NeedIncludeKeyword[2][j] in ZFcontDict[mid]:
            printp('[UID:'+str(mid)+' 转发未包含关键字中的第'+str(j+1)+'个，无效]')
            return False
    return True

def checkKW_2(mid):
    if not NeedIncludeKeyword[1]:
        return True
    if len(NeedIncludeKeyword[2])==0:
        return True
    for j in range(len(NeedIncludeKeyword[2])):
        if not NeedIncludeKeyword[2][j] in PLcontDict[mid]:
            printp('[UID:'+str(mid)+' 评论未包含关键字中的第'+str(j+1)+'个，无效]')
            return False
    return True

def linktodyid(dyid):
    #转换t.bilibili.com格式链接为动态id 备用正则/[0-9]{18}/
    if "t.bilibili.com/" in dyid and '#' in dyid:
        dyid, sep, tail = dyid.partition('#')
        dyid, sep, tail = dyid.partition('?')
        dyid=dyid[dyid.rfind('/'):]
        head, sep, dyid = dyid.partition('/')
    elif "t.bilibili.com/" in dyid:
        dyid, sep, tail = dyid.partition('?')
        dyid=dyid[dyid.rfind('/'):]
        head, sep, dyid = dyid.partition('/')
    else:
        return dyid
    return dyid

def clicked():
    btn['state']=tk.DISABLED
    btn7['state']=tk.DISABLED
    global cjthread
    btn.configure(text="进行中…",bg='ivory')
    btn7.configure(text="(等待当前任务)")
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
    btn['state']=tk.NORMAL
    btn7['state']=tk.NORMAL
    btn.configure(text="开始抽奖!",bg='deepskyblue')
    btn7.configure(text="转发/评论查重")

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
        time.sleep(0.001)
        barval=bar['value']
        #if bar['value']==100:
        #    bar.stop()
        #    break
        #print(bar['value'])
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
    if '关' in dycont or '关注' in dycont or '粉丝' in dycont:
        if not '关于' in dycont:
            GZ='关'
        elif '关注' in dycont:
            GZ='关'
    TJ='['+ZF+PL+DZ+GZ+']'
    if CHKCJDT(dycont):
        if not TJ=='[]':
            return TJ+'(可能)'
        else:
            return '[未知]'
    else:
        return '(可能不是抽奖动态)'

def CHKCJDT(dycont):
    '''cjkw1='抽' in dycont and '奖' in dycont
    cjkw2='抽' in dycont and '送' in dycont
    cjkw3='关' in dycont and '转' in dycont
    cjkw4='转' in dycont and '评' in dycont
    cjkw5='转' in dycont and '留言' in dycont
    cjkw6='转' in dycont and '抽' in dycont
    cjkw7='评' in dycont and '抽' in dycont
    cjkw8='赞' in dycont and '抽' in dycont
    cjkw9='转' in dycont and '送' in dycont
    cjkw10='评' in dycont and '送' in dycont
    cjkw11='赞' in dycont and '送' in dycont
    cjkwall=cjkw1 or cjkw2 or cjkw3 or cjkw4 or cjkw5 or cjkw6 or cjkw7 or cjkw8 or cjkw9 or cjkw10 or cjkw11'''
    dycont=dycont.replace('\n','')
    cjkwall=re.search(r'/(?=.*抽)(?=.*奖)^.*|(?=.*抽)(?=.*送)^.*|(?=.*关)(?=.*转)^.*|(?=.*转)(?=.*评)^.*|(?=.*转)(?=.*抽)^.*|(?=.*转)(?=.*留言)^.*|(?=.*转)(?=.*抽)^.*|(?=.*评)(?=.*抽)^.*|(?=.*赞)(?=.*抽)^.*|(?=.*转)(?=.*送)^.*|(?=.*评)(?=.*送)^.*|(?=.*赞)(?=.*送)^.*/g',dycont)
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
    global noDisplayUser1
    global RaffleBeginTime
    global EnaSuoYin
    global NeedFollowOther
    global ZFidDict
    global PLidDict
    global dyn_type
    RaffleBeginTime=time.localtime()
    bar['value']=0
    barval=0
    barp.configure(text='0%')
    btn4.state(['disabled'])
    #print()
    TZF=bool(chk1_state.get())
    TPL=bool(chk2_state.get())
    TDZ=bool(chk3_state.get())
    TGZ=NeedFollowSelf
    #TRZ=bool(chk5_state.get())
    global NEEDAT
    NEEDAT=bool(chk7_state.get())
    ZFidDict={}
    PLidDict={}
    EnaSuoYin=bool(chk9_state.get())
    if True:#chk6_state.get():
        output['state']='normal'
        output.delete(1.0, tk.END)
        output['state']='disabled'
    notime=True
    printp(updinfo)
    notime=False
    if txt.get()=='':
        tkinter.messagebox.showwarning("提示", '需要输入动态链接或动态ID！')
        return False
    try:
        dyid=linktodyid(txt.get())
        dyid=int(dyid)
    except:
        if 'www.bilibili.com/' in dyid:
            tkinter.messagebox.showwarning("提示", '如使用视频/专栏/音频抽奖请点击“转换稿件编号”进行转换！')
        else:
            tkinter.messagebox.showwarning("提示", '输入的动态链接或动态ID无法识别！')
        #printp('')
        return False
    dyinfoo=''
    if len(str(dyid))<13:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?type=2&rid='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfoo=resback['data']['card']['desc']
            #tkinter.messagebox.showinfo("提示", '已将相簿ID还原为动态ID，请再次开始抽奖！')
        except:
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))<=17 and len(str(dyid))>=13:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfo=resback['data']['card']
        except Exception as e:
            #print(e)
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))>18:
        tkinter.messagebox.showwarning("提示", '输入的动态ID过长 ('+str(len(str(dyid)))+'/'+'18) ！')
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
    noDisplayUser1=(chk8_state.get())
    if not TZF and not TPL and not TDZ:#not TGZ and
        tkinter.messagebox.showwarning("提示", '需要至少选中一个获奖条件！')
        #printp()
        return False
    '''if TGZ and not TZF and not TPL and not TDZ:
        tkinter.messagebox.showwarning("提示", '还需要选择除了关注以外的任一获奖条件！')
        #printp()
        return False'''
    try:
        HJNUM=int(spin.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的获奖者数量没有意义！')
        return False
    if HJNUM<1:
        tkinter.messagebox.showwarning("提示",'输入的获奖者数量小于1，这是不想让小伙伴们抽中？')
        return False
    try:
        HJlvl=int(spin3.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的最低等级没有意义！')
        return False
    if HJlvl<0 or HJlvl>6:
        tkinter.messagebox.showwarning("提示",'输入的最低等级小于0或大于6！请不要调戏我呢…')
        return False
    try:
        CJHnum=int(spin2.get())
    except:
        tkinter.messagebox.showwarning("提示",'输入的过滤抽奖号的值没有意义！')
        return False
    if CJHnum<-1 or CJHnum>10:
        tkinter.messagebox.showwarning("提示",'输入的过滤抽奖号的值小于-1或大于10！请不要调戏我呢…')
        return False
    if not TGZ and not NeedFollowOther:
        bar.start(2)
        barval=0
        BarProgress(10)
    if NeedFollowOther and len(NeedFollowOtherList)==0:
        NeedFollowOther=False
    TZF2=repBool(TZF)
    TPL2=repBool(TPL)
    TDZ2=repBool(TDZ)
    TGZ2=repBool(TGZ)
    TGZ3=repBool(NeedFollowOther)
    TZBJ=repBool(NeedHaveLiveRoom)
    printp('转发：'+str(TZF2)+' 评论：'+str(TPL2)+' 点赞：'+str(TDZ2)+' 关注自己：'+str(TGZ2)+' 关注其他：'+str(TGZ3)+'\n开通直播间：'+str(TZBJ)+' 最低等级：'+str(HJlvl)+' 抽奖号阈值：'+str(CJHnum))
    if CJHnum!=-1:
        GLCJH=True
    else:
        GLCJH=False
    if HJlvl!=0:
        GLlvl=True
    else:
        GLlvl=False
    notime=False
    if TGZ or NeedFollowOther:
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
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            "Cookie":cookie,
            }
            r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header)
            r.encoding='utf-8'
            userinfo_dict=json.loads(r.text)
            #print(r)
            jdata=userinfo_dict['data']
            myuid=jdata.get('mid')
            name=str(jdata.get('name'))
            level=jdata.get('level')
            coins=jdata.get('coins')
            needexp=str(jdata['level_exp']['next_exp']-jdata['level_exp']['current_exp'])
            outrb()
            if DisplayLogInfo:
                printp('模拟登录成功，UID:'+str(myuid)+'，详情如下\n'+name+'，Lv'+str(level)+'，粉丝数 '+str(jdata['follower'])+'，拥有 '+str(coins)+' 枚硬币')#用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
                #printp('模拟登录成功：'+name+'(UID:'+str(myuid)+')，详情如下\n'+'Lv'+str(level)+'(还需'+needexp+')，粉丝数 '+str(jdata['follower'])+'，拥有 '+str(coins)+' 枚硬币')#用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
            else:
                printp('模拟登录成功：'+name+'(UID:'+str(myuid)+')')#，用户名：')                
            isLogin=True
        except Exception as e:
            try:
                if userinfo_dict['code']==-412:
                    printp('模拟登录失败，请求间隔过短，请过一段时间后重试!')
                    return False
            except:
                pass
            printp('模拟登录失败，可能是cookie无效，已过期或未登录，请重新获取cookie!')
            print(str(repr(e)))
            return False
    #dyid=input('输入动态ID：')
    #bar['value']=30
    BarProgress(30)
    dyid=str(dyid)
    dyn_type='normal'
    if not dyinfoo=='':
        notime=True
        changelink(dyinfoo['dynamic_id'])
        printp('<将相簿ID('+str(dyid)+')转换为动态ID>')
        dyid=str(dyinfoo['dynamic_id'])
        dyn_type='xiangbu'
    notime=False
    printp('正在获取动态详情……')
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        }
        url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+dyid
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        dyinfo=resback.get('data')
        tmstmp=time.localtime(dyinfo['card']['desc']['timestamp'])
        dycard=json.loads(dyinfo['card']['card'])
        notime=True
        outrb()
        try:
            if dycard['aid']!=None:
                printp('<检测到视频稿件动态(av'+str(dycard['aid'])+')>')#，B站可能会对此类稿件限流!')
                dycard['item']['reply']=dycard['stat']['reply']
                dyn_type='shipin'
        except:
            pass
        try:
            if dycard['id']!=None and 'summary' in dycard.keys():
                printp('<检测到专栏稿件动态(cv'+str(dycard['id'])+')>')
                dycard['item']['reply']=dycard['stats']['reply']
                dyn_type='zhuanlan'
        except:
            pass
        try:
            if dycard['id']!=None and 'intro' in dycard.keys():
                printp('<检测到音频稿件动态(au'+str(dycard['id'])+')>')
                dycard['item']['reply']=dycard['replyCnt']
                dyn_type='yinpin'
        except:
            pass
        try:
            if dycard['item']['id']!=None and 'category' in dycard['item'].keys() and dyinfoo=='':
                printp('<检测到相簿动态('+str(dycard['item']['id'])+')>')
                dyn_type='xiangbu'
        except:
            pass
        printp('-------------------------------------------')
        printp('动态ID:'+dyid+' '+checkTJ(dyinfo['card']['card']))
        printp('动态发送者：'+str(dyinfo['card']['desc']['user_profile']['info']['uname'])+'\n浏览：'+str(dyinfo['card']['desc']['view'])+'，转发：'+str(dyinfo['card']['desc']['repost'])+'，评论：'+str(dycard['item']['reply'])+'，点赞：'+str(dyinfo['card']['desc']['like']))
        printp('发送时间：'+time.strftime("%Y-%m-%d %H:%M:%S", tmstmp))
        printp('-------------------------------------------')
        if TGZ and dyinfo['card']['desc']['user_profile']['info']['uid']!=myuid:
            notime=True
            printp('警告：动态发送者('+dyinfo['card']['desc']['user_profile']['info']['uname']+')和当前已登录用户不一致!')
            return False
        if NeedFollowOther and dyinfo['card']['desc']['user_profile']['info']['uid']!=myuid:
            notime=True
            printp('注意：动态发送者('+dyinfo['card']['desc']['user_profile']['info']['uname']+')和当前已登录用户不一致!')
            #return False
        try:
            lottdata=json.loads(dyinfo['card']['extension']['lott'])
            printp('此动态已经存在官方官方抽奖工具!抽奖ID:'+str(lottdata['lottery_id']))
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
        if str(repr(e))=="KeyError('card')":
            printp('动态详情为空，可能是动态链接/ID输入有误，请检查')
        else:
            printp('获取出错，可能是动态链接/ID输入有误，请检查\n详细报错如下：\n'+str(repr(e)))
        try:
            printp('获取到的信息：\n'+res.text)
        except:
            printp('(未接收到任何信息)')
        return False
    '''if not isLogin:
        myuid=dyinfo.get('card').get('desc').get('user_profile').get('info').get('uid')'''
    myuid=dyinfo['card']['desc']['user_profile']['info']['uid']
    printp('开始获取数据……\n(抽取时将自动过滤UP主自己和重复转发/评论的用户)')
    #bar['value']=40
    notime=True
    if TZF and dyinfo['card']['desc']['repost']>550:
        printp('警告：转发数量超过550的部分可能获取不完整!')
    if TPL and dycard['item']['reply']>8000:
        printp('警告：评论数量超过8000的部分如继续获取可能被限制!')
    if TDZ and dyinfo['card']['desc']['like']>20000:
        printp('警告：点赞数量超过25000的部分如继续获取可能被限制!')
    printp('')
    Error=False
    BarProgress(40)
    if TZF:
        if dyinfo['card']['desc']['repost']==0:
            printp('这条动态没有任何用户转发!')
            Error=True
        if dyinfo['card']['desc']['repost']>600:
            printp('转发限制在600次以内!(如超出建议改抽评论)')
            Error=True
        if HJNUM>dyinfo['card']['desc']['repost']:
            printp('设置的获奖者总数大于这条动态的转发数!')
            Error=True
    if TPL:
        if dycard['item']['reply']==0:
            printp('这条动态没有任何用户评论!')
            Error=True
        if dycard['item']['reply']>30000:
            printp('评论限制在30000条以内!')
            Error=True
        if HJNUM>dycard['item']['reply']:
            printp('设置的获奖者总数大于这条动态的评论数!')
            Error=True
    if TDZ:
        if dyinfo['card']['desc']['like']==0:
            printp('这条动态没有任何用户点赞!')
            Error=True
        if dyinfo['card']['desc']['like']>50000:
            printp('点赞限制在50000个以内!')
            Error=True
        if HJNUM>dyinfo['card']['desc']['like']:
            printp('设置的获奖者总数大于这条动态的点赞数!')
            Error=True
    if Error:
        return False
    LBALL=[]
    LBALL2={}
    notime=False
    #BarProgress(40)
    if TZF:
        LBZF2=getZF(dyid)
        try:
            if not LBZF2:
                return False
        except:
            pass
        LBZF=list(LBZF2.keys())
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBZF)
            LBALL2=Merge(LBALL2,LBZF2)
        else:
            LBALL=set(LBZF)
            LBALL2=(LBZF2)
    #bar['value']=50
    BarProgress(55)
    if TPL:
        LBPL2=getPL(dyid)
        try:
            if not LBPL2:
                return False
        except:
            pass
        LBPL=list(LBPL2.keys())
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBPL)
            LBALL2=Merge(LBALL2,LBPL2)
        elif not TZF:
            LBALL=set(LBPL)
            LBALL2=LBPL2
    #bar['value']=60
    BarProgress(70)
    if TDZ:
        LBDZ2=getDZ(dyid)
        try:
            if not LBDZ2:
                return False
        except:
            pass
        LBDZ=list(LBDZ2.keys())
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBDZ)
            LBALL2=Merge(LBALL2,LBDZ2)
        elif not TZF and not TPL:
            LBALL=set(LBDZ)
            LBALL2=LBDZ2
    #bar['value']=70
    BarProgress(85)
    notime=True
    printp('')
    notime=False
    printp('已获取到符合要求的参与者数量为：'+str(len(list(LBALL))))
    #print(GLCJH,NeedFollowOther)
    if GLCJH or NeedFollowOther:
        notime=True
        printp('注意：依据抽奖设定所需获取数据较多，请耐心等待')
    notime=True
    if HJNUM>len(list(LBALL)) or HJNUM<1:
        printp('输入的获奖者数量('+str(HJNUM)+')超出范围!')
        return False
    HJMD=[]
    times=1
    lba=len(LBALL)
    BarProgress(85)
    #恶作剧代码，应UID:291224482的要求 https://b23.tv/CUkmf3
    for i in BLACKLIST:
        LBALL.remove(i)
    #======================================================#
    while True:
        while True:
            if not len(LBALL) < HJNUM:
                HJuser=secrets.choice(list(LBALL))#这句是核心功能之一，随机从参与者数组里抽一位
                #print(HJuser)
                if not HJuser in HJMD:
                    if checkGZ(HJuser) and checklvl(HJuser,HJlvl) and checkCJH(HJuser,CJHnum) and checkZBJ(HJuser) and checkZhuangBan(HJuser) and checkSameFollow(HJuser) and checkKW_1(HJuser) and checkKW_2(HJuser):
                        HJMD.append(HJuser)
                        #LBALL.remove(HJuser)
                        #printp('[抽到UID:'+str(HJuser)+']')
                        times=times+1
                    else:
                        LBALL.remove(HJuser)
                    #print(len(LBALL))
                numz1=lba-len(LBALL)
                numz2=numz1/lba
                time.sleep(0.01)
                BarProgress(85+13*numz2)
                #print(bar['value'])
                break
            else:
                printp('')
                printp('警告：参与者列表人数已小于设定的获奖者数量!\n建议：修改或取消抽奖号过滤值，取消部分获奖条件')
                return False
        if times>HJNUM:
            break
        '''if len(HJMD)!=0:
            BarProgress(85+13*len(HJMD)/HJNUM)'''
    #bar['value']=90
    #input('waiting...')
    #BarProgress(98)
    HJMD.sort()
    random.shuffle(HJMD)
    notime=False
    printp('抽取完成！\n获奖名单：(以UID为准)')
    notime=True
    bar['value']=98
    barval=98
    barp.configure(text='98%')
    #BarProgress(90)
    printp('-------------------------------------------')
    getname(HJMD,LBALL2)
    printp('-------------------------------------------')
    #printp('程序即将退出……')
    #bar['value']=100
    btn4['state']=tk.NORMAL
    #if EnaSuoYin:
    #    print(ZFidDict,PLidDict)
    barval=100
    if NEEDAT:
        #print(ATuser)
        '''ATmsg0=str(ATuser).replace('[','')
        ATmsg1=ATmsg0.replace(']','')
        ATmsg2=ATmsg1.replace(',',' ')
        ATmsg3=ATmsg2.replace("'",'')'''
        #print(ATmsg3)
        ATmsg=' '.join(ATuser)
        pyperclip.copy(ATmsg)
        printp('已复制获奖者用户名，可直接粘贴到动态编辑框')
    if pform=='win':
        import platform
        if platform.release()=='10':
            printp('提示：可以按下 Win+Shift+S 保存窗口截图')
        else:
            printp('提示：可以按下 Alt+PrtSc 并粘贴到画图保存窗口截图')
    elif pform=='linux':
        printp('提示：可以按下 Alt+PrtSc 保存窗口截图\n（可能需要粘贴到合适的位置保存）')
    elif pform=='darwin':
        printp('提示：可以按下 Command+Shift+4 保存局部截图')
    notime=False
    return True

def clicked18():
    btn['state']=tk.DISABLED
    btn7['state']=tk.DISABLED
    global cjthread2
    btn.configure(text="(等待当前任务)",bg='ivory')
    btn7.configure(text="进行中…")
    cjthread2=threading.Thread(target=clicked18_2,args=())
    cjthread2.start()
    thread2=threading.Thread(target=checkthread2,args=(cjthread2,))
    thread2.start()

def checkthread2(thread):
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
    btn['state']=tk.NORMAL
    btn7['state']=tk.NORMAL
    btn.configure(text="开始抽奖!",bg='deepskyblue')
    btn7.configure(text="转发/评论查重")

def clicked18_2():
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
    global noDisplayUser1
    global RaffleBeginTime
    global EnaSuoYin
    global NeedFollowOther
    global ZFidDict
    global PLidDict
    global dyn_type
    global LoginUID
    RaffleBeginTime=time.localtime()
    bar['value']=0
    barval=0
    barp.configure(text='0%')
    btn4.state(['disabled'])
    #print()
    TZF=bool(chk1_state.get())
    TPL=bool(chk2_state.get())
    TGZ=NeedFollowSelf
    ZFidDict={}
    PLidDict={}
    EnaSuoYin=bool(chk9_state.get())
    output['state']='normal'
    output.delete(1.0, tk.END)
    output['state']='disabled'
    notime=True
    printp(updinfo)
    notime=False
    if txt.get()=='':
        tkinter.messagebox.showwarning("提示", '需要输入动态链接或动态ID！')
        return False
    try:
        dyid=linktodyid(txt.get())
        dyid=int(dyid)
    except:
        if 'www.bilibili.com/' in dyid:
            tkinter.messagebox.showwarning("提示", '如使用视频/专栏/音频抽奖请点击“转换稿件编号”进行转换！')
        else:
            tkinter.messagebox.showwarning("提示", '输入的动态链接或动态ID无法识别！')
        #printp('')
        return False
    dyinfoo=''
    if len(str(dyid))<13:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?type=2&rid='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfoo=resback['data']['card']['desc']
            #tkinter.messagebox.showinfo("提示", '已将相簿ID还原为动态ID，请再次开始抽奖！')
        except:
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))<=17 and len(str(dyid))>=13:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfo=resback['data']['card']
        except Exception as e:
            #print(repr(e))
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))>18:
        tkinter.messagebox.showwarning("提示", '输入的动态ID过长 ('+str(len(str(dyid)))+'/'+'18) ！')
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
    LoginUID=''
    noDisplayUser1=(chk8_state.get())
    if not TZF and not TPL:#not TGZ and
        tkinter.messagebox.showwarning("提示", '至少需要选择转发或评论的其中一个！')
        return False
    TZF2=repBool(TZF)
    TPL2=repBool(TPL)
    TGZ2=repBool(TGZ)
    printp('转发：'+str(TZF2)+' 评论：'+str(TPL2)+' 检测自己：'+str(TGZ2))
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
                printp('检测自己需要登录，请点击“登录/Cookie操作”按钮进行登录！')
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
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            "Cookie":cookie,
            }
            r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header)
            r.encoding='utf-8'
            userinfo_dict=json.loads(r.text)
            #print(r)
            jdata=userinfo_dict['data']
            myuid=jdata.get('mid')
            LoginUID=jdata['mid']
            name=str(jdata.get('name'))
            level=jdata.get('level')
            coins=jdata.get('coins')
            needexp=str(jdata['level_exp']['next_exp']-jdata['level_exp']['current_exp'])
            outrb()
            if DisplayLogInfo:
                printp('模拟登录成功，UID:'+str(myuid)+'，详情如下\n'+name+'，Lv'+str(level)+'，粉丝数 '+str(jdata['follower'])+'，拥有 '+str(coins)+' 枚硬币')#用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
                #printp('模拟登录成功：'+name+'(UID:'+str(myuid)+')，详情如下\n'+'Lv'+str(level)+'(还需'+needexp+')，粉丝数 '+str(jdata['follower'])+'，拥有 '+str(coins)+' 枚硬币')#用户名：'+name+'，等级 '+str(level)+'，拥有 '+str(coins)+' 枚硬币')
            else:
                printp('模拟登录成功：'+name+'(UID:'+str(myuid)+')')#，用户名：')                
            isLogin=True
        except Exception as e:
            try:
                if userinfo_dict['code']==-412:
                    printp('模拟登录失败，请求间隔过短，请过一段时间后重试!')
                    return False
            except:
                pass
            printp('模拟登录失败，可能是cookie无效，已过期或未登录，请重新获取cookie!')
            print(str(repr(e)))
            return False
    BarProgress(30)
    dyid=str(dyid)
    dyn_type='normal'
    if not dyinfoo=='':
        notime=True
        changelink(dyinfoo['dynamic_id'])
        printp('<将相簿ID('+str(dyid)+')转换为动态ID>')
        dyid=str(dyinfoo['dynamic_id'])
        dyn_type='xiangbu'
    notime=False
    printp('正在获取动态详情……')
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        }
        url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+dyid
        res = requests.get(url=url,headers=header)
        res.encoding='utf-8'
        resback=json.loads(res.text)
        dyinfo=resback.get('data')
        tmstmp=time.localtime(dyinfo['card']['desc']['timestamp'])
        dycard=json.loads(dyinfo['card']['card'])
        notime=True
        outrb()
        try:
            if dycard['aid']!=None:
                printp('<检测到视频稿件动态(av'+str(dycard['aid'])+')>')#，B站可能会对此类稿件限流!')
                dycard['item']['reply']=dycard['stat']['reply']
                dyn_type='shipin'
        except:
            pass
        try:
            if dycard['id']!=None and 'summary' in dycard.keys():
                printp('<检测到专栏稿件动态(cv'+str(dycard['id'])+')>')
                dycard['item']['reply']=dycard['stats']['reply']
                dyn_type='zhuanlan'
        except:
            pass
        try:
            if dycard['id']!=None and 'intro' in dycard.keys():
                printp('<检测到音频稿件动态(au'+str(dycard['id'])+')>')
                dycard['item']['reply']=dycard['replyCnt']
                dyn_type='yinpin'
        except:
            pass
        try:
            if dycard['item']['id']!=None and 'category' in dycard['item'].keys() and dyinfoo=='':
                printp('<检测到相簿动态('+str(dycard['item']['id'])+')>')
                dyn_type='xiangbu'
        except:
            pass
        printp('-------------------------------------------')
        printp('动态ID:'+dyid+' '+checkTJ(dyinfo['card']['card']))
        printp('动态发送者：'+str(dyinfo['card']['desc']['user_profile']['info']['uname'])+'\n浏览：'+str(dyinfo['card']['desc']['view'])+'，转发：'+str(dyinfo['card']['desc']['repost'])+'，评论：'+str(dycard['item']['reply'])+'，点赞：'+str(dyinfo['card']['desc']['like']))
        printp('发送时间：'+time.strftime("%Y-%m-%d %H:%M:%S", tmstmp))
        printp('-------------------------------------------')
        try:
            lottdata=json.loads(dyinfo['card']['extension']['lott'])
            printp('此动态已经存在官方官方抽奖工具!抽奖ID:'+str(lottdata['lottery_id']))
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
        if str(repr(e))=="KeyError('card')":
            printp('动态详情为空，可能是动态链接/ID输入有误，请检查')
        else:
            printp('获取出错，可能是动态链接/ID输入有误，请检查\n详细报错如下：\n'+str(repr(e)))
        try:
            printp('获取到的信息：\n'+res.text)
        except:
            printp('(未接收到任何信息)')
        return False
    myuid=dyinfo['card']['desc']['user_profile']['info']['uid']
    printp('开始获取数据……')#\n(抽取时将自动过滤UP主自己和重复转发/评论的用户)')
    #bar['value']=40
    notime=True
    if TZF and dyinfo['card']['desc']['repost']>550:
        printp('警告：转发数量超过550的部分可能获取不完整!')
    if TPL and dycard['item']['reply']>8000:
        printp('警告：评论数量超过8000的部分如继续获取可能被限制!')
    printp('')
    Error=False
    BarProgress(40)
    if TZF:
        if dyinfo['card']['desc']['repost']==0:
            printp('这条动态没有任何用户转发!')
            Error=True
        '''if dyinfo['card']['desc']['repost']>600:
            printp('转发限制在600次以内!')
            Error=True'''
    if TPL:
        if dycard['item']['reply']==0:
            printp('这条动态没有任何用户评论!')
            Error=True
        if dycard['item']['reply']>30000:
            printp('评论限制在30000条以内!')
            Error=True
    if Error:
        return False
    LBALL=[]
    LBALL2={}
    LBZF=[]
    LBPL=[]
    notime=False
    #BarProgress(40)
    if TZF:
        LBZF2=getZF(dyid,True)
        #print(ZFidDict)
        try:
            if not LBZF2:
                return False
        except:
            pass
        LBZF=list(LBZF2.keys())
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBZF)
            LBALL2=Merge(LBALL2,LBZF2)
        else:
            LBALL=set(LBZF)
            LBALL2=(LBZF2)
    #bar['value']=50
    BarProgress(55)
    if TPL:
        LBPL2=getPL(dyid,True)
        #print(PLidDict)
        try:
            if not LBPL2:
                return False
        except:
            pass
        LBPL=list(LBPL2.keys())
        if len(LBALL)!=0:
            LBALL=set(LBALL)&set(LBPL)
            LBALL2=Merge(LBALL2,LBPL2)
        elif not TZF:
            LBALL=set(LBPL)
            LBALL2=LBPL2
    #bar['value']=60
    BarProgress(70)
    #bar['value']=70
    BarProgress(85)
    notime=True
    printp('')
    notime=False
    printp('数据收集完成，即将开始检测……')
    #printp('已获取到参与者数量为：'+str(len(list(LBALL))))
    #print(GLCJH,NeedFollowOther)
    notime=True
    bar['value']=95
    barval=95
    barp.configure(text='95%')
    getname_chongfu(LBALL2,zf=ZFidDict,pl=PLidDict)
    barval=100
    return True

def getname_chongfu(usrdict,*,zf,pl):
    #print(zf)
    #print(pl)
    printp('-------------------------------------------')
    times=1
    cfzfuid=[]
    cfpluid=[]
    if len(zf)!=0:
        times=1
        for i in zf:
            if len(zf[i])>1:
                cfzfuid.append(i)
                printp('重复转发：'+usrdict[i]+'(UID:'+str(i)+') NO.'+str(times))
                for j in range(len(zf[i])):
                    #printp(str(j+1)+' 动态ID：'+str(zf[i][j]))
                    printp(str(j+1)+' 链接：https://t.bilibili.com/'+str(zf[i][j]))
                times+=1
        if times==1:
            printp('<未发现重复转发>')
    if len(pl)!=0:
        if times!=1:
            printp('-------------------------------------------')
        times=1
        for i in pl:
            if len(pl[i])>1:
                cfpluid.append(i)
                printp('重复评论：'+usrdict[i]+'(UID:'+str(i)+') NO.'+str(times))
                for j in range(len(pl[i])):
                    #printp(str(j+1)+' 评论ID：'+str(pl[i][j]))
                    printp(str(j+1)+' 链接：https://t.bilibili.com/'+str(dyid)+'#reply'+str(pl[i][j]))
                times+=1
        if times==1:
            printp('<未发现重复评论>')
    printp('-------------------------------------------')
    if LoginUID!='':
        #print(LoginUID,cfzfuid,cfpluid)
        if LoginUID in cfzfuid:
            printp('注意：检测到当前已登录用户的重复转发！位于NO.'+str(cfzfuid.index(LoginUID)+1))
        if LoginUID in cfpluid:
            printp('注意：检测到当前已登录用户的重复评论！位于NO.'+str(cfpluid.index(LoginUID)+1))

def clicked2():
    #关于窗口
    tkinter.messagebox.showinfo("关于", '''B站动态抽奖工具 Python GUI版 '''+version+'''
更新日期: '''+updatetime+'''
作者: 派蒙月饼（芍芋）
Bili.fan首页: https://bili.fan
Blog: https://bili.fan/blog/
哔哩哔哩: https://space.bilibili.com/229778960
爱发电: https://afdian.net/@shoyu
本项目Github：https://github.com/shoyu3/DynamicRaffle-Python
Copyright © 2021 Bili.fan 本项目以 GPL v3 开源''')
#https://shoyu.top

def clicked3():
    global login1window
    global login2window
    global login3window
    login1window = tk.Toplevel(window)
    login1window.title('登录/Cookie操作')
    login1window.configure(bg='white')
    login1window.transient(window) 
    width = 266
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
    logbtn3 = ttk.Button(login1window, text="   加密Cookie    ", command=clicked6)
    logbtn3.place(x=10, y=52)
    logbtn4 = ttk.Button(login1window, text="     "+repBool2(bool(1-DisplayLogInfo))+"登录细节      ", command=lambda:clicked10(logbtn4))#clicked10(loginlbl1))
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
    login2window = tk.Toplevel(window)
    login2window.title('使用B站客户端扫码登录')
    width = 294
    heigh = 286
    screenwidth = login2window.winfo_screenwidth()
    screenheight = login2window.winfo_screenheight()-50
    login2window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login2window.resizable(0,0)
    login2window.configure(bg='white')
    login2window.transient(window) 
    try:
        login2window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(login2window)
        except:
            pass
    photo = tk.PhotoImage(file='qrcode.png')
    w = tk.Label(login2window, image=photo)
    w.place(x=-2, y=-10)
    #w.pack()
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
        #notime=True
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
    try:
        csrftoken=cookies_dict['bili_jct']
    except:
        tkinter.messagebox.showwarning("提示",'指定的cookie无效！')
        return False
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
    login3window = tk.Toplevel(window)
    login3window.title('输入加密用密码')
    width = 280
    heigh = 90
    screenwidth = login3window.winfo_screenwidth()
    screenheight = login3window.winfo_screenheight()-50
    login3window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    login3window.resizable(0,0)
    login3window.configure(bg='white')
    login3window.transient(window) 
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
    login4window = tk.Toplevel(window)
    login4window.title('输入解密用密码')
    login4window.configure(bg='white')
    login4window.transient(window) 
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
    tkinter.messagebox.showinfo('提示','已将该cookie解密！')
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
                tkinter.messagebox.showwarning('提示','二维码已过期，请重试！')
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

def changelink(t):
    txt.delete(0,tk.END)
    txt.insert(tk.END,t)
    #print(t)

def clicked9():
    #print(output.get(1.0,END))
    TimeSt=time.strftime("%Y-%m-%d-%H-%M-%S",RaffleBeginTime)
    rzpath='抽奖记录'+TimeSt+'.txt'
    RZtxt = open(rzpath,'w',encoding='utf-8')
    RZtxt.write(output.get(1.0,tk.END))
    RZtxt.close()
    tkinter.messagebox.showinfo("提示",'抽奖记录已保存为：'+rzpath)

def clicked10(btn):
    global DisplayLogInfo
    DisplayLogInfo=bool(1-DisplayLogInfo)
    DPLI2=repBool2(DisplayLogInfo)
    #tkinter.messagebox.showinfo("提示",'已切换为：'+DPLI2)
    btn.configure(text='     '+repBool2(bool(1-DisplayLogInfo))+'登录细节      ')
    login1window.update()

def mo_switch_onoff(name,*ele):
    global NeedFollowSelf
    global NeedFollowOther
    global NeedHaveLiveRoom
    global NeedHaveGarb
    global NeedIncludeKeyword
    if name=='mochk1':
        NeedFollowSelf=not NeedFollowSelf
    elif name=='mochk2':
        NeedFollowOther=not NeedFollowOther
        #str(NeedFollowOther)
        switch_disnorm(ele)
    elif name=='mochk3':
        NeedHaveLiveRoom=not NeedHaveLiveRoom
    elif name=='mochk4':
        NeedHaveGarb=not NeedHaveGarb
    elif name=='mochk5':
        NeedIncludeKeyword[0]=not NeedIncludeKeyword[0]
    elif name=='mochk6':
        NeedIncludeKeyword[1]=not NeedIncludeKeyword[1]
    more1window.update()

def switch_disnorm(ele):
    #print(str(ele[0]['state']))
    if str(ele[0]['state'])=='normal':
        ele[0]['state']='disabled'
    else:
        ele[0]['state']='normal'
    more1window.update()

def clicked12():
    gzlist=motxt1.get()
    #print(gzlist)
    if gzlist=='':
        tkinter.messagebox.showwarning("提示", '您未输入任何内容！')
        return False
    gzlist=gzlist.split(',')
    wgzlist=[]
    if not all(v for v in gzlist):
        tkinter.messagebox.showwarning("提示", '存在多余或无意义逗号分隔！')
        return False
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
            tkinter.messagebox.showinfo("提示", '本功能需要登录，请点击“登录/Cookie操作”按钮进行登录！')
            return False
    cook=open(cookiepath,'r')
    cookie=cook.read()
    cook.close()
    if 'ENCRYPTED\n' in cookie:
        tkinter.messagebox.showwarning("提示", '请将cookie文件解密后重试!')
        decrycook(cookiepath)
        return False
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        "Cookie":cookie,
        }
        r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header).text
        userinfo_dict=json.loads(r)
        #print(r)
        jdata=userinfo_dict['data']
        myuid=jdata.get('mid')
        name=str(jdata.get('name'))
        level=jdata.get('level')
        coins=jdata.get('coins')
        needexp=str(jdata['level_exp']['next_exp']-jdata['level_exp']['current_exp'])
        isLogin=True
    except:
        try:
            if userinfo_dict['code']==-412:
                tkinter.messagebox.showinfo("提示", '模拟登录失败，请求间隔过短，请过一段时间后重试!')
                return False
        except:
            pass
        tkinter.messagebox.showinfo("提示", '模拟登录失败，可能是cookie无效，已过期或未登录，请重新获取cookie!')
        return False
    for i in range(len(gzlist)):
        if not gzlist[i]=='':
            url='http://api.bilibili.com/x/space/acc/relation?mid='+str(gzlist[i])
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            "Cookie":cookie,
            }
            res = requests.get(url=url,headers=header)
            resback=json.loads(res.text)
            rinfo=resback.get('data')
            try:
                relation=rinfo['relation']['attribute']
            except:
                relation=0
            #print(res.text)
            if not relation==2 and not relation==6:
                wgzlist.append(gzlist[i])
    if not len(wgzlist)==0:
        tkinter.messagebox.showwarning("提示", '保存失败，还有以下用户您并未关注：\n'+','.join(wgzlist))
    else:
        tkinter.messagebox.showinfo("提示", '保存成功，您已关注所有指定用户！')
        while '' in gzlist:
            gzlist.remove('')
        global NeedFollowOtherList
        NeedFollowOtherList=list(set(gzlist))

NeedFollowSelf=False
NeedFollowOther=False
NeedHaveLiveRoom=False
NeedHaveGarb=False
NeedFollowOtherList=[]
NeedIncludeKeyword=[True,False,[]]
def clicked11():
    if cjthread.is_alive():
        tkinter.messagebox.showwarning("提示", '请等待抽奖结束后再进行调整！')
        return False
    global more1window
    global motxt1,motxt2
    global mochk1_state
    more1window = tk.Toplevel(window)
    more1window.title('更多选项')
    more1window.configure(bg='white')
    more1window.transient(window) 
    width = 308
    heigh = 240
    screenwidth = more1window.winfo_screenwidth()
    screenheight = more1window.winfo_screenheight()-50
    more1window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    more1window.resizable(0,0)
    try:
        more1window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(more1window)
        except:
            pass
    mochk1_state = tk.BooleanVar()
    mochk1_state.set(NeedFollowSelf)
    mochk1 = ttk.Checkbutton(more1window, text="需要关注自己", var=mochk1_state ,command=lambda:mo_switch_onoff('mochk1'))
    mochk1.place(x=10, y=10)
    mochk3_state = tk.BooleanVar()
    mochk3_state.set(NeedHaveLiveRoom)
    mochk3 = ttk.Checkbutton(more1window, text="需要拥有直播间", var=mochk3_state ,command=lambda:mo_switch_onoff('mochk3'))
    mochk3.place(x=176, y=10)
    mochk2_state = tk.BooleanVar()
    mochk2_state.set(NeedFollowOther)
    mochk2 = ttk.Checkbutton(more1window, text="需要关注其他用户", var=mochk2_state,command=lambda:mo_switch_onoff('mochk2',motxt1))
    mochk2.place(x=10, y=40)
    mochk4_state = tk.BooleanVar()
    mochk4_state.set(NeedHaveGarb)
    mochk4 = ttk.Checkbutton(more1window, text="需要拥有粉丝套装", var=mochk4_state ,command=lambda:mo_switch_onoff('mochk4'))
    mochk4.place(x=176, y=40)
    molbl1 = tk.Label(more1window, text="需一并关注的UID (使用半角逗号,隔开 需要自己也关注)")
    molbl1.place(x=4, y=65)
    molbl1.configure(bg='white')
    motxt1 = ttk.Entry(more1window, width=40)
    motxt1.place(x=11, y=86)
    nfol=NeedFollowOtherList
    while '' in nfol:
        nfol.remove('')
    motxt1.insert(tk.END,','.join(nfol))
    if not NeedFollowOther:
        motxt1['state']='disabled'
    #print(NeedFollowOtherList)
    if NeedFollowOther and NeedFollowOtherList==[]:
        mochk2_state.set(False)
        motxt1['state']='disabled'
    mobtn2 = ttk.Button(more1window, text="搜索关注列表", command=clicked13)
    mobtn2.place(x=10, y=112)
    mobtn3 = ttk.Button(more1window, text="读取动态at", command=clicked14)
    mobtn3.place(x=100, y=112)
    mobtn1 = ttk.Button(more1window, text="保存并检测", command=clicked12)
    mobtn1.place(x=211, y=112)
    molbl2 = tk.Label(more1window, text="需包含的文字 (使用半角逗号,隔开 无需启用索引功能)")
    molbl2.place(x=8, y=143)
    molbl2.configure(bg='white')
    motxt2 = ttk.Entry(more1window, width=40)
    motxt2.place(x=11, y=166)
    nikw=NeedIncludeKeyword[2]
    while '' in nikw:
        nikw.remove('')
    motxt2.insert(tk.END,','.join(nikw))
    mobtn4 = ttk.Button(more1window, text="搜索可用tag", command=clicked_002)
    mobtn4.place(x=10, y=192)
    mobtn4['state']=tk.DISABLED
    mochk5_state = tk.BooleanVar()
    mochk5_state.set(NeedIncludeKeyword[0])
    mochk5 = ttk.Checkbutton(more1window, text="转发", var=mochk5_state ,command=lambda:mo_switch_onoff('mochk5'))
    mochk5.place(x=103, y=194)
    mochk6_state = tk.BooleanVar()
    mochk6_state.set(NeedIncludeKeyword[1])
    mochk6 = ttk.Checkbutton(more1window, text="评论", var=mochk6_state ,command=lambda:mo_switch_onoff('mochk6'))
    mochk6.place(x=159, y=194)
    #mobtn3 = ttk.Button(more1window, text="读取动态at", command=clicked14)
    #mobtn3.place(x=100, y=112)
    mobtn5 = ttk.Button(more1window, text="保存", command=clicked_001)
    mobtn5.place(x=211, y=192)
    more1window.lift()
    more1window.grab_set()
    more1window.mainloop()

def clicked_002():
    tkinter.messagebox.showinfo('提示','无意义功能，暂未完成！')
    return False
    global more4window
    global mo4txt1
    global mo4lbox
    global mo4lbl2
    more4window = tk.Toplevel(window)
    more4window.title('搜索可用tag')
    more4window.configure(bg='white')
    more4window.transient(window) 
    width = 292
    heigh = 230
    screenwidth = more4window.winfo_screenwidth()
    screenheight = more4window.winfo_screenheight()-50
    more4window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    more4window.resizable(0,0)
    try:
        more4window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(more4window)
        except:
            pass
    mo4lbl1 = tk.Label(more4window, text="输入关键字")
    mo4lbl1.place(x=10, y=0)
    mo4lbl1.configure(bg='white')
    mo4lbl2 = tk.Label(more4window, text="")
    mo4lbl2.place(x=10, y=196)
    mo4lbl2.configure(bg='white')
    mo4txt1 = ttk.Entry(more4window, width=25)
    mo4txt1.place(x=10, y=20)
    mo4btn1 = ttk.Button(more4window, text="搜索", command=clicked_003)
    mo4btn1.place(x=193, y=18)
    mo4lbox = tk.Listbox(more4window,relief='solid',width=38,height=8)
    mo4lbox.place(x=10, y=45)
    mo4btn2 = ttk.Button(more4window, text="插入", command=clicked_003_2)
    mo4btn2.place(x=193, y=194)
    more4window.lift()
    more4window.grab_set()
    more4window.mainloop()

def clicked_001():
    global NeedIncludeKeyword
    kwlist=motxt2.get()
    #print(gzlist)
    if kwlist=='':
        tkinter.messagebox.showinfo("提示", '保存成功！关键字数量：0')
        NeedIncludeKeyword[2]=[]
        #tkinter.messagebox.showwarning("提示", '您未输入任何内容！')
        return False
    kwlist=kwlist.split(',')
    #wkwlist=[]
    if not all(v for v in kwlist):
        tkinter.messagebox.showwarning("提示", '存在多余或无意义逗号分隔！')
        return False
    tkinter.messagebox.showinfo("提示", '保存成功！关键字数量：'+str(len(kwlist)))
    while '' in kwlist:
        kwlist.remove('')
    #print(kwlist)
    NeedIncludeKeyword[2]=list(set(kwlist))

def clicked_003():
    pass

def clicked_003_2():
    pass

def clicked13():
    global more2window
    global mo2txt1
    global mo2lbox
    global mo2lbl2
    more2window = tk.Toplevel(window)
    more2window.title('搜索关注列表')
    more2window.configure(bg='white')
    more2window.transient(window) 
    width = 292
    heigh = 230
    screenwidth = more2window.winfo_screenwidth()
    screenheight = more2window.winfo_screenheight()-50
    more2window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    more2window.resizable(0,0)
    try:
        more2window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(more2window)
        except:
            pass
    mo2lbl1 = tk.Label(more2window, text="输入用户名关键字")
    mo2lbl1.place(x=10, y=0)
    mo2lbl1.configure(bg='white')
    mo2lbl2 = tk.Label(more2window, text="")
    mo2lbl2.place(x=10, y=196)
    mo2lbl2.configure(bg='white')
    mo2txt1 = ttk.Entry(more2window, width=25)
    mo2txt1.place(x=10, y=20)
    mo2btn1 = ttk.Button(more2window, text="搜索", command=clicked15)
    mo2btn1.place(x=193, y=18)
    mo2lbox = tk.Listbox(more2window,relief='solid',width=38,height=8)
    mo2lbox.place(x=10, y=45)
    mo2btn2 = ttk.Button(more2window, text="插入", command=clicked15_2)
    mo2btn2.place(x=193, y=194)
    more2window.lift()
    more2window.grab_set()
    more2window.mainloop()

def clicked15():
    searchkw=mo2txt1.get()
    if searchkw=='':
        tkinter.messagebox.showwarning("提示", '您未输入任何内容！')
        return False
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
            tkinter.messagebox.showinfo("提示", '本功能需要登录，请点击“登录/Cookie操作”按钮进行登录！')
            return False
    cook=open(cookiepath,'r')
    cookie=cook.read()
    cook.close()
    if 'ENCRYPTED\n' in cookie:
        tkinter.messagebox.showwarning("提示", '请将cookie文件解密后重试!')
        decrycook(cookiepath)
        return False
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        "Cookie":cookie,
        }
        r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header)
        r.encoding='utf-8'
        userinfo_dict=json.loads(r.text)
        #print(r)
        jdata=userinfo_dict['data']
        myuid=jdata.get('mid')
        name=str(jdata.get('name'))
        level=jdata.get('level')
        coins=jdata.get('coins')
        needexp=str(jdata['level_exp']['next_exp']-jdata['level_exp']['current_exp'])
        isLogin=True
    except Exception as e:
        print(repr(e))
        try:
            if userinfo_dict['code']==-412:
                tkinter.messagebox.showinfo("提示", '模拟登录失败，请求间隔过短，请过一段时间后重试!')
                return False
        except:
            pass
        tkinter.messagebox.showinfo("提示", '模拟登录失败，可能是cookie无效，已过期或未登录，请重新获取cookie!')
        return False
    r=requests.get('http://api.bilibili.com/x/relation/followings/search?vmid=229778960&pn=1&ps=50&order=desc&order_type=attention&name='+str(mo2txt1.get()),headers=header)
    r.encoding='utf-8'
    jdata=json.loads(r.text)['data']
    total_num=jdata['total']
    mo2lbox.delete(0,tk.END)
    times=1
    pages=math.ceil(total_num/50)
    global AttList
    AttList=[]
    while times<=pages:
        r=requests.get('http://api.bilibili.com/x/relation/followings/search?vmid=229778960&pn='+str(times)+'&ps=50&order=desc&order_type=attention&name='+str(mo2txt1.get()),headers=header)
        r.encoding='utf-8'
        jdata=json.loads(r.text)['data']
        alist=jdata['list']
        for i in range(len(alist)):
            m=alist[i]['uname']+' (UID:'+str(alist[i]['mid'])+')'
            AttList.append(alist[i]['mid'])
            mo2lbox.insert(tk.END,m)
        times+=1
    mo2lbl2.configure(text='共有：'+str(len(AttList))+'位')

def clicked15_2():
    if mo2lbox.curselection()==():
        tkinter.messagebox.showwarning("提示", '请选中需插入的用户！')
        return False
    Dis=False
    if str(motxt1['state'])=='disabled':
        Dis=True
        motxt1['state']='normal'
    curusr=int(mo2lbox.curselection()[0])
    needadd=''
    txtcont=motxt1.get()
    if txtcont!='' and txtcont[-1]!=',':
        needadd=','
    motxt1.insert(tk.END,needadd+str(AttList[curusr]))#+',')
    if Dis:
        motxt1['state']='disabled'
    more2window.destroy()

def clicked14():
    global more3window
    global mo3txt1
    global mo3lbox
    global mo3lbl2
    more3window = tk.Toplevel(window)
    more3window.title('读取动态at')
    more3window.configure(bg='white')
    more3window.transient(window) 
    width = 292
    heigh = 230
    screenwidth = more3window.winfo_screenwidth()
    screenheight = more3window.winfo_screenheight()-50
    more3window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    more3window.resizable(0,0)
    try:
        more3window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(more3window)
        except:
            pass
    mo3lbl1 = tk.Label(more3window, text="输入动态链接或动态ID")
    mo3lbl1.place(x=10, y=0)
    mo3lbl1.configure(bg='white')
    mo3lbl2 = tk.Label(more3window, text="")
    mo3lbl2.place(x=10, y=196)
    mo3lbl2.configure(bg='white')
    mo3txt1 = ttk.Entry(more3window, width=25)
    mo3txt1.place(x=10, y=20)
    mo3btn1 = ttk.Button(more3window, text="读取", command=clicked16)
    mo3btn1.place(x=193, y=18)
    mo3lbox = tk.Listbox(more3window,relief='solid',width=38,height=8)
    mo3lbox.place(x=10, y=45)
    mo3btn2 = ttk.Button(more3window, text="插入", command=clicked16_2)
    mo3btn2.place(x=193, y=194)
    more3window.lift()
    more3window.grab_set()
    more3window.mainloop()

def clicked16():
    if mo3txt1.get()=='':
        tkinter.messagebox.showwarning("提示", '需要输入动态链接或动态ID！')
        return False
    try:
        dyid=linktodyid(mo3txt1.get())
        dyid=int(dyid)
    except:
        tkinter.messagebox.showwarning("提示", '输入的动态链接或动态ID无法识别！')
        return False
    dyinfoo=''
    if len(str(dyid))<16:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?type=2&rid='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfoo=resback['data']['card']['desc']
        except:
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))==17 or len(str(dyid))==16:
        try:
            header={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
            }
            url='http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+str(dyid)
            res = requests.get(url=url,headers=header)
            res.encoding='utf-8'
            resback=json.loads(res.text)
            dyinfo=resback['data']['card']
        except Exception as e:
            print(str(repr(e)))
            tkinter.messagebox.showwarning("提示", '输入的动态ID长度不够 ('+str(len(str(dyid)))+'/'+'18) ！')
            return False
    elif len(str(dyid))>18:
        tkinter.messagebox.showwarning("提示", '输入的动态ID过长 ('+str(len(str(dyid)))+'/'+'18) ！')
        return False
    if not dyinfoo=='':
        mo3txt1.delete(0,tk.END)
        mo3txt1.insert(tk.END,dyinfoo['dynamic_id'])
        dyid=str(dyinfoo['dynamic_id'])
    r=requests.get('http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+str(dyid)).text
    jdata=json.loads(r)['data']
    dycard1=json.loads(jdata['card']['card'])
    dycard2=json.loads(jdata['card']['extend_json'])
    try:
        #print(dycard1)
        atlist=dycard1['item']['at_uids']
    except:
        try:
            atctrl=json.loads(dycard1['item']['at_control'])
            atlist=[]
            for j in range(len(atctrl)):
                atlist.append(atctrl[j]['data'])
        except:
            tkinter.messagebox.showwarning("提示", '指定动态没有任何at！')
            return False
    mo3lbox.delete(0,tk.END)
    global AtUserList
    AtUserList=[]
    for i in range(len(atlist)):
        r=requests.get('http://api.bilibili.com/x/space/acc/info?mid='+str(atlist[i]))
        r.encoding='utf-8'
        atusrname=json.loads(r.text)['data']['name']
        m=atusrname+' (UID:'+str(atlist[i])+')'
        AtUserList.append(atlist[i])
        mo3lbox.insert(tk.END,m)
    mo3lbl2.configure(text='共有：'+str(len(AtUserList))+'位')

def clicked16_2():
    if mo3lbox.curselection()==():
        tkinter.messagebox.showwarning("提示", '请选中需插入的用户！')
        return False
    Dis=False
    if str(motxt1['state'])=='disabled':
        Dis=True
        motxt1['state']='normal'
    curusr=int(mo3lbox.curselection()[0])
    needadd=''
    txtcont=motxt1.get()
    if txtcont!='' and txtcont[-1]!=',':
        needadd=','
    motxt1.insert(tk.END,needadd+str(AtUserList[curusr]))#+',')
    if Dis:
        motxt1['state']='disabled'
    more3window.destroy()

def clicked17():
    global aid1window
    global aidtxt
    global aidoutput
    global aidbtn2
    global aidlbl2
    aid1window = tk.Toplevel(window)
    aid1window.title('转换稿件编号')
    aid1window.configure(bg='white')
    aid1window.transient(window) 
    width = 376
    heigh = 290
    screenwidth = aid1window.winfo_screenwidth()
    screenheight = aid1window.winfo_screenheight()-50
    aid1window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    aid1window.resizable(0,0)
    aidlbl1= tk.Label(aid1window, text="输入稿件编号或稿件链接（av/BV/cv/au）",bg='white')
    aidlbl1.place(x=10, y=10)
    #login4window.configure(bg='white')
    try:
        login4window.iconbitmap('icon.ico')
    except:
        try:
            setIcon(aid1window)
        except:
            pass
    aidtxt = ttk.Entry(aid1window, width=50)
    aidtxt.place(x=10, y=30)
    aidbtn1 = ttk.Button(aid1window, text="转换", command=clicked17_2)
    aidbtn1.place(x=146, y=60)
    aidoutput = scrolledtext.ScrolledText(aid1window, width=48, height=9, relief="solid")
    aidoutput.place(x=10, y=94)
    aidoutput['state']='disabled'
    aidbtn2 = ttk.Button(aid1window, text="插入", command=clicked17_3)
    aidbtn2.place(x=146, y=255)
    aidbtn2.state(['disabled'])
    aidlbl2= tk.Label(aid1window, text="动态ID：无",bg='white',justify='center')
    aidlbl2.place(relx = 0.5, rely = 0.81, anchor = "center")
    aid1window.lift()
    aid1window.grab_set()

class bvconv:
    def dec(x):
        try:
            table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
            tr={}
            for i in range(58):
                    tr[table[i]]=i
            s=[11,10,3,8,4,6]
            xor=177451812
            add=8728348608
            r=0
            for i in range(6):
                    r+=tr[x[s[i]]]*58**i
            return (r-add)^xor
        except:
            tkinter.messagebox.showwarning('提示','BV号转换出错！')
            return 'Failed'

def cookie_to_json(cookies_str):
    cookies_dict={}
    for cookie in cookies_str.replace(' ','').split(';'):
        cookies_dict[cookie.split('=')[0]]=cookie.split('=')[-1]
    return cookies_dict

def linktoaid(dyid):
    if dyid[-1]=='/':
        dyid=dyid[:-1]
    if "www.bilibili.com/" in dyid and '#' in dyid:
        dyid, sep, tail = dyid.partition('#')
        dyid, sep, tail = dyid.partition('?')
        dyid=dyid[dyid.rfind('/'):]
        head, sep, dyid = dyid.partition('/')
    elif "www.bilibili.com/" in dyid:
        dyid, sep, tail = dyid.partition('?')
        dyid=dyid[dyid.rfind('/'):]
        head, sep, dyid = dyid.partition('/')
    else:
        return dyid
    return dyid

def clicked17_2():
    aidoutput['state']='normal'
    aidoutput.delete(1.0, tk.END)
    aidoutput['state']='disabled'
    aidlbl2.configure(text='动态ID：无')
    aidbtn2['state']=tk.DISABLED
    aid_in=aidtxt.get()
    if aid_in=='':
        tkinter.messagebox.showwarning("提示", '您未输入任何内容！')
        return False
    if 'www.bilibili.com' in aid_in:
        anum=linktoaid(aid_in)
    else:        
        anum=aid_in
    atype=anum[:2]
    aid=anum[2:]
    if aid=='':
        tkinter.messagebox.showwarning("提示", '输入的值有误！')
        return False
    if atype=='av':
        sharetype='8'
    elif atype=='BV':
        sharetype='8'
        aid=bvconv.dec(anum)
        if aid=='Failed':
            return False
        anum='av'+str(aid)
    elif atype=='cv':
        sharetype='64'
    elif atype=='au':
        sharetype='256'
    else:
        tkinter.messagebox.showwarning("提示", '稿件类型不正确！')
        return False
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
            tkinter.messagebox.showinfo("提示", '本功能需要登录，请点击“登录/Cookie操作”按钮进行登录！')
            return False
    cook=open(cookiepath,'r')
    cookie=cook.read()
    cook.close()
    if 'ENCRYPTED\n' in cookie:
        tkinter.messagebox.showwarning("提示", '请将cookie文件解密后重试!')
        decrycook(cookiepath)
        return False
    try:
        header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182 Safari/537.36",
        "Cookie":cookie,
        }
        r=requests.get('http://api.bilibili.com/x/space/myinfo',headers=header).text
        userinfo_dict=json.loads(r)
        #print(r)
        jdata=userinfo_dict['data']
        myuid=jdata.get('mid')
        name=str(jdata.get('name'))
        level=jdata.get('level')
        coins=jdata.get('coins')
        needexp=str(jdata['level_exp']['next_exp']-jdata['level_exp']['current_exp'])
        isLogin=True
    except:
        try:
            if userinfo_dict['code']==-412:
                tkinter.messagebox.showinfo("提示", '模拟登录失败，请求间隔过短，请过一段时间后重试!')
                return False
        except:
            pass
        tkinter.messagebox.showinfo("提示", '模拟登录失败，可能是cookie无效，已过期或未登录，请重新获取cookie!')
        return False
    aidprint('即将开始获取稿件动态ID……')
    aidprint('>>尝试分享'+anum+'……')
    cookie_dict=cookie_to_json(cookie)
    csrf_token=cookie_dict.get('bili_jct')
    data={
    'csrf':csrf_token,
    "csrf_token":csrf_token,
    "platform":'pc',
    'uid':'2',
    'type':sharetype,
    'share_uid':myuid,
    'content':'',
    'repost_code':'20000',
    'rid':aid,
    }
    res = requests.post(url='http://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share',data=data,headers=header)
    #aidprint(res.text)
    message=json.loads(res.text)
    if (message['code'] == 0):
        share_dynid=message['data']['dynamic_id_str']
        aidprint('>>动态分享成功，动态ID：'+share_dynid)
    else:
        aidprint('>>动态分享失败，返回信息为：'+message['message'])
        return False
    aidprint('>>获取动态详情('+str(share_dynid)+')……')
    r=requests.get('http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id='+str(share_dynid)).text
    message=json.loads(r)
    if (message['code'] == 0):
        global adynid
        adynid=message['data']['card']['desc']['orig_dy_id_str']
        if str(adynid)!='0' and str(adynid)!='':
            aidprint('>>稿件('+str(anum)+')对应动态获取成功\n>>>动态ID：'+str(adynid))
            aidlbl2.configure(text='动态ID：'+str(adynid))
            aidbtn2['state']=tk.NORMAL
        else:
            aidprint('注意：稿件('+str(anum)+')对应动态ID为空值('+str(adynid)+')!')
    else:
        aidprint('>>获取失败，返回信息为：'+message['message'])
    aidprint('>>尝试删除刚才的动态('+str(share_dynid)+')……')
    data={
    'dynamic_id':share_dynid,
    "csrf":csrf_token,
    'csrf_token':csrf_token,
    }
    res = requests.post('http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic?csrf='+csrf_token,data=data,headers=header)
    message=json.loads(res.text)
    if (message['code'] == 0):
        aidprint('>>动态删除成功')
    else:
        aidprint('>>删除动态失败，返回信息为：'+message['message'])
    return False

def clicked17_3():
    if txt.get()!='':
        usr_choice=tkinter.messagebox.askyesno('提示','动态ID输入框已有内容，是否覆盖？')
        if not usr_choice:
            return False
    changelink(adynid)
    aid1window.destroy()

def aidprint(text):
    aidoutput['state']='normal'
    aidoutput.insert('end',str(text)+'\n')
    aidoutput['state']='disabled'
    aidoutput.see(tk.END)
    aid1window.update()

window = tk.Tk()#初始化一个窗口
window.title('B站动态抽奖工具 Python GUI版 '+version+' 演示视频av247587107 如遇问题请联系作者')#按下F1可查看按键操作说明')#标题 By: 芍芋 '+updatetime+' 
window.configure(bg='white')#背景颜色
#window.geometry("820x300")

#窗口居中实现
width = 723 #720 Linux
heigh = 445 #530 Linux
if 'win' in sys.platform:
    pform='win'
    window.resizable(0,0)#设置禁止调整窗口大小
else:
    width = 770 #720 Linux
    heigh = 560 #530 Linux
    pform=sys.platform
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()-50
window.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
#定义图标
try:
    window.iconbitmap('icon.ico')
except:
    try:
        setIcon(window)
    except:
        pass

style=ttk.Style()
style.configure("TCheckbutton", background="white")
style.configure("cj.TButton", background="white",height=8,width=40)
style.configure("TScale", background="white")#,width=10)

def focto(obj):
    obj.focus()
    changelink(pyperclip.paste())

def switch_to(status):
    if status.get():
        status.set(False)
    else:
        status.set(True)

def pressbutton(command):
    command()

def pressbutton2(btnn,command):
    #print(str(btnn.state())=="('disabled',)")
    if not str(btnn.state())=="('disabled',)":
        command()

def clickedkeyhelp():
    #按键操作帮助
    tkinter.messagebox.showinfo("按键操作说明", 'F1 显示本说明\nF2 粘贴剪贴板内容到输入框\nF3 开始抽奖\nF5 切换转发开关\nF6 切换评论开关\nF7 切换点赞开关\nF8 更多选项\nF9 切换隐藏无效用户开关\nF10 切换自动复制用户名开关\nF11 保存当前记录\nF12 登录\Cookie操作')

def show_value(ele,nlbl):
    nlbl.configure(text=str(ele.get()).rjust(2, ' '))
    #print(ele.get())

class Limiter(ttk.Scale):
    """ ttk.Scale sublass that limits the precision of values. """

    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')  # Remove non-std kwarg.
        self.chain = kwargs.pop('command', lambda *a: None)  # Save if present.
        super(Limiter, self).__init__(*args, command=self._value_changed, **kwargs)

    def _value_changed(self, newvalue):
        newvalue = round(float(newvalue), self.precision)
        self.winfo_toplevel().globalsetvar(self.cget('variable'), (newvalue))
        self.chain(newvalue) 

#定义文本
lbl1 = tk.Label(window, text="在下方输入动态链接或者动态ID")# (使用Ctrl+V粘贴)")
lbl1.place(x=10, y=10)
lbl1.configure(bg='white')
txt = ttk.Entry(window, width=43)
txt.bind_all('<F2>', lambda a:focto(txt))
txt.place(x=10, y=35)
#txt.focus()
lbl2 = tk.Label(window, text="选择抽奖条件")#"选择一下抽奖条件吧")
lbl2.place(x=10, y=70)
lbl2.configure(bg='white')
#定义复选框
chk1_state = tk.BooleanVar()
chk1_state.set(True) # Set check state
chk1 = ttk.Checkbutton(window, text="转发", var=chk1_state)#, onvalue=1, offvalue=0)
chk1.bind_all('<F5>', lambda a:switch_to(chk1_state))
chk1.place(x=10, y=92)
chk2_state = tk.BooleanVar()
chk2_state.set(False) # Set check state
chk2 = ttk.Checkbutton(window, text="评论", var=chk2_state)
chk2.bind_all('<F6>', lambda a:switch_to(chk2_state))
chk2.place(x=90, y=92)
chk3_state = tk.BooleanVar()
chk3_state.set(False) # Set check state
chk3 = ttk.Checkbutton(window, text="点赞", var=chk3_state)
chk3.bind_all('<F7>', lambda a:switch_to(chk3_state))
chk3.place(x=170, y=92)
'''chk4_state = tk.BooleanVar()
chk4_state.set(False) # Set check state
chk4 = ttk.Checkbutton(window, text="关注", var=chk4_state)
chk4.bind_all('<F8>', lambda a:switch_to(chk4_state))
chk4.place(x=270, y=92)'''
btn6 = ttk.Button(window, text="更多选项", command=clicked11)
btn6.bind_all('<F8>', lambda a:pressbutton(clicked11))
btn6.place(x=230, y=90)
spin = ttk.Spinbox(window, from_=1, to=999, width=5)
spin.place(x=69, y=145)
spin.set(1)
#spin.configure(bg='white')
#lbl7 = tk.Label(window, text="值越小越严格,-1=无☞")
#lbl7.place(x=125, y=189)
#lbl7.configure(bg='white')
#var2 = tk.StringVar(window)
lbln1= tk.Label(window, text="0")
lbln1.place(x=300, y=144)
lbln1.configure(bg='white')
lbln2= tk.Label(window, text="-1")
lbln2.place(x=300, y=182)
lbln2.configure(bg='white')
nvar2 = tk.IntVar(window)
spin3=Limiter(window,from_=0,to=6,length=53,command=lambda x:show_value(nvar2,lbln1),precision=4,variable=nvar2)
'''spin3 = ttk.Combobox(window, width=4, textvariable=var2)
spin3['values']=(0,1,2,3,4,5,6)'''
spin3.configure(style="TScale")
#spin3.configure(bg='white',orient="horizontal")
spin3.place(x=242, y=143)
nvar = tk.IntVar(window)
spin2=Limiter(window,from_=-1,to=10,length=83,command=lambda x:show_value(nvar,lbln2),precision=4,variable=nvar)
'''spin2 = ttk.Combobox(window, width=4, textvariable=var)
spin2['values']=(-1,0,1,2,3,4,5,6,7,8,9,10)'''
spin2.configure(style="TScale")
#spin2.configure(bg='white',orient="horizontal")
spin2.place(x=212, y=182)
spin2.set(-1)
spin3.set(0)
chk8_state = tk.BooleanVar()
chk8_state.set(False) # Set check state
chk8 = ttk.Checkbutton(window, text="隐藏无效用户", var=chk8_state)
chk8.bind_all('<F9>', lambda a:switch_to(chk8_state))
chk8.place(x=10, y=220)
chk7_state = tk.BooleanVar()
chk7_state.set(False) # Set check state
chk7 = ttk.Checkbutton(window, text="自动复制用户名", var=chk7_state)
chk7.bind_all('<F10>', lambda a:switch_to(chk7_state))
chk7.place(x=10, y=245)
chk9_state = tk.BooleanVar()
chk9_state.set(True) # Set check state
chk9 = ttk.Checkbutton(window, text="索引转发/评论", var=chk9_state)
#chk9.bind_all('<F10>', lambda a:switch_to(chk7_state))
chk9.place(x=10, y=270)
'''chk5_state = BooleanVar()
chk5_state.set(False) # Set check state
chk5 = ttk.Checkbutton(window, text="保存抽奖记录", var=chk5_state)
chk5.place(x=10, y=265)
chk6_state = BooleanVar()
chk6_state.set(True) # Set check state
chk6 = ttk.Checkbutton(window, text="自动清空记录", var=chk6_state)
chk6.place(x=10, y=240)'''
btn4 = ttk.Button(window, text=" 保存当前记录 ", command=clicked9)
btn4.bind_all('<F11>', lambda a:pressbutton2(btn4,clicked9))
btn4.place(x=10, y=295)
btn7 = ttk.Button(window, text="转发/评论查重", command=clicked18)
btn7.place(x=112, y=295)
btn2 = ttk.Button(window, text="关于本程序", command=clicked2)
btn2.bind_all('<F1>', lambda a:pressbutton(clickedkeyhelp))
btn2.place(x=228, y=221)
btn5 = ttk.Button(window, text="转换稿件编号", command=clicked17)
btn5.place(x=228, y=258)
#btn2.configure(style="TButton")
btn3 = ttk.Button(window, text="登录/Cookie操作", command=clicked3)
btn3.bind_all('<F12>', lambda a:pressbutton(clicked3))
btn3.place(x=211, y=295)
#btn3.configure(style="TButton")
btn = tk.Button(window, text="开始抽奖!", command=clicked)
btn.bind_all('<F3>', lambda a:pressbutton(clicked))
btn.place(x=10, y=340)
btn.configure(bg='deepskyblue',height=2,width=42)
lbl3 = tk.Label(window, text="获奖人数")
lbl3.place(x=10, y=144)
lbl3.configure(bg='white')
lbl4 = tk.Label(window, text="过滤抽奖号 [值越小越严格,-1=禁用]")
lbl4.place(x=10, y=182)
lbl4.configure(bg='white')
lbl5 = tk.Label(window, text="※评论获取不包括楼中楼")
lbl5.place(x=10, y=115)
lbl5.configure(bg='white')
lbl6 = tk.Label(window, text="获奖者最低等级")
lbl6.place(x=147, y=144)
lbl6.configure(bg='white')
output = scrolledtext.ScrolledText(window, width=51, height=31, relief="solid")
output.place(x=333, y=17)
output['state']='disabled'
bar = ttk.Progressbar(window, length=265)#290)
bar.place(x=10, y=402)
bar['value']=0
barp = tk.Label(window, text="0%")
barp.place(x=283, y=401)
barp.configure(bg='white')
btn4.state(['disabled'])
#chk5.state(['disabled'])
#显示窗口
if not pform=='win':
    tkinter.messagebox.showinfo("提示", '非Windows平台需手动调整窗口大小使内容显示完整！')

show = tk.StringVar()
class section:
    def onPaste(self):
        try:
            sel_index=a,b=txt.index('sel.first'),txt.index('sel.last')
            #print(sel_index)
            txt_str=txt.get()
            new_str=''
            for i in range(0, len(txt_str)):
                if i not in range(sel_index[0],sel_index[1]):
                    new_str = new_str + txt_str[i]
            txt.delete(0,tk.END)
            txt.insert(0,new_str)
        except:
            sel_index=(txt.index('insert'),tk.END)
        t=pyperclip.paste()
        txt.insert(txt.index(sel_index[0]),t)
        txt.icursor(sel_index[0]+len(t))
            #show.set(str(self.text))
 
    def onCopy(self):
        sel_index=a,b=txt.index('sel.first'),txt.index('sel.last')
        self.text = txt.get()[sel_index[0]:sel_index[1]]
        pyperclip.copy(self.text)
 
    def onCut(self):
        self.onCopy()
        try:
            txt.delete('sel.first', 'sel.last')
        except:
            pass

    def onSelectAll(self):
        txt.select_range('0',tk.END)

BLACKLIST=[]
def clicked_surprise():
    global BLACKLIST
    BLACKLIST.append(291224482)
    menu.delete('点我有惊喜！')

section = section()
menu = tk.Menu(window, tearoff=0)
menu.add_command(label="粘贴", command=section.onPaste)
menu.add_command(label="剪切", command=section.onCut)
menu.add_command(label="复制", command=section.onCopy)
menu.add_separator()
menu.add_command(label="全选", command=section.onSelectAll)
menu.add_command(label="点我有惊喜！", command=clicked_surprise)

def popupmenu(event):
    if pyperclip.paste()=='':
        menu.entryconfig('粘贴',state=tk.DISABLED)
    else:
        menu.entryconfig('粘贴',state=tk.NORMAL)
    if txt.select_present()==0:
        menu.entryconfig('剪切',state=tk.DISABLED)
        menu.entryconfig('复制',state=tk.DISABLED)
    else:
        menu.entryconfig('剪切',state=tk.NORMAL)
        menu.entryconfig('复制',state=tk.NORMAL)
    menu.post(event.x_root, event.y_root)

txt.bind("<Button-3>", popupmenu)
show2 = tk.StringVar()
class section2:
    '''def onPaste(self):
        try:
            sel_index=a,b=output.index('sel.first'),output.index('sel.last')
            #print(sel_index)
            output_str=output.get()
            new_str=''
            for i in range(0, len(output_str)):
                if i not in range(sel_index[0],sel_index[1]):
                    new_str = new_str + output_str[i]
            output.delete(0,tk.END)
            output.insert(0,new_str)
        except:
            sel_index=(output.index('insert'),tk.END)
        t=pyperclip.paste()
        output.insert(output.index(sel_index[0]),t)
        output.icursor(sel_index[0]+len(t))
            #show.set(str(self.text))'''
 
    def onCopy(self):
        sel_index=a,b=output.index('sel.first'),output.index('sel.last')
        self.text = output.get(sel_index[0],sel_index[1])#[]
        pyperclip.copy(self.text)
 
    '''def onCut(self):
        self.onCopy()
        try:
            output.delete('sel.first', 'sel.last')
        except:
            pass'''

    def onSelectAll(self):
        output.selection_range('0',tk.END)

section2 = section2()
menu2 = tk.Menu(window, tearoff=0)
menu2.add_command(label="复制", command=section2.onCopy)
#menu2.add_separator()
#menu2.add_command(label="全选", command=section2.onSelectAll)

def popupmenu2(event):
    try:
        output.selection_get()
        #print(output.selection_get())
        menu2.entryconfig('复制',state=tk.NORMAL)
    except:
        menu2.entryconfig('复制',state=tk.DISABLED)
    menu2.post(event.x_root, event.y_root)

output.bind("<Button-3>", popupmenu2)
DisplayLogInfo=True
chkupdwindow = tk.Toplevel(window)
chkupdwindow.title('检查更新')
chkupdwindow.configure(bg='white')
chkupdwindow.transient(window) 
width = 300
heigh = 100
screenwidth = chkupdwindow.winfo_screenwidth()+300
screenheight = chkupdwindow.winfo_screenheight()-50#+200
chkupdwindow.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
chkupdwindow.resizable(0,0)
try:
    chkupdwindow.iconbitmap('icon.ico')
except:
    try:
        setIcon(chkupdwindow)
    except:
        pass
chklbl1 = tk.Label(chkupdwindow, text="正在检查是否有新版本… (/ω＼*)\n（可忽略本窗口）", justify="center")
chklbl1.configure(bg='white')
chklbl1.place(relx = 0.5, rely = 0.4, anchor = "center")
chkupdthread=threading.Thread(target=chkupd,args=())
chkupdthread.start()

window.mainloop()
