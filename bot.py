# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
#=================================================================#
### LOGIN SETTING ###
boteater = LINE()##LOGIN LEWAT TOKEN
boteater.log("Auth Token : " + str(boteater.authToken))
#=================================================================#
### SETTINGS INFO ###
boteaterMID = boteater.profile.mid
boteaterProfile = boteater.getProfile()
lineSettings = boteater.getSettings()
oepoll = OEPoll(boteater)
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)
botStart = time.time()
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
myProfile["displayName"] = boteaterProfile.displayName
myProfile["statusMessage"] = boteaterProfile.statusMessage
myProfile["pictureStatus"] = boteaterProfile.pictureStatus
#=================================================================#
#=================================================================#
#=================================================================#
### DESCRIBE DEF ##
#=================================================================#
def restartBot():
    print (">>>機器重啟<<<")
    backupData()
    time.sleep(1)
    python = sys.executable
    os.execl(python, python, *sys.argv)

def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    boteater.log("發生錯誤 : " + str(text))
    time_ = datetime.now()
    with open("error.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        boteater.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
#=================================================================#
#=================================================================#
def lineBot(op):
    try:
#=================================================================#
        if op.type == 0:
            print ("DONE")
            return
#=================================================================#
        if op.type == 5:
            print ("通知 : 加入好友")
            if settings["autoAdd"] == True:
                boteater.sendMessage(op.param1, "=== 尹莫測試 V1.0 === \n嘿嘿! {} 恭喜您成為白老鼠".format(str(boteater.getContact(op.param1).displayName)))
#=================================================================#
        if op.type == 13:
            print ("通知 : 加入群組")
            group = boteater.getGroup(op.param1)
            if settings["autoJoin"] == True:
                boteater.acceptGroupInvitation(op.param1)
#=================================================================#
        if op.type == 24:
            print ("通知 : 離開副本")
            if settings["autoLeave"] == True:
                boteater.leaveRoom(op.param1)
#=================================================================#
        if op.type == 25:
            print ("通知 : 傳送訊息")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != boteater.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
#=================================================================#
#=================================================================#
                if text is None:
                    return
#=================================================================#
#=================================================================#
                if text.lower() == 'help':
                    boteater.sendMessage(to, "=== SELFBOT V.1 === \nbotmenu \nsetting \nselfmenu \ngrupmenu \nmedia \ntokenlist \nanimenew \nanimelist")
                if text.lower() == 'tokenlist':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ntoken mac \ntoken ios \ntoken chrome \ntoken win10 \ntoken desktop \ntoken done")
                elif text.lower() == 'botmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nrestart \nspeed \nstatus \nabout \nruntime \nerrorlog")
                elif text.lower() == 'setting':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nautoadd(on/off) \nautoread(on/off) \nautojoin(on/off) \nautoleave(on/off) \nautochecksticker(on/off) \ndetectmention(on/off)")
                elif text.lower() == 'selfmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \nme \nmymid \nmypicture \nmyvideo \nmycover \nstealcontact(mention) \nstealmid(mention) \nstealbio(mention) \nstealpicture(mention) \nstealvideoprofile(mention) \nstealcover(mention) \ncloneprofile(mention) \nrestoreprofile \nmention")
                elif text.lower() == 'grupmenu':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ngcreator \ngpicture \nglink \nqr(on/off) \nglist \ngmember \nginfo \ncrash")
                elif text.lower() == 'media':
                    boteater.sendMessage(to, "===  SELFBOT V.1 === \ninstagraminfo(username) \ninstagrampost(username) \nyoutubes(keyword) \nimage(keyword) \nssweb(link)")
#=================================================================#
### BOT MENU COMMAND ###
#=================================================================#
#=================================================================#
                elif text.lower() == 'speed':
                    start = time.time()
                    boteater.sendMessage(to, "█▒▒▒▒▒▒▒▒▒...")
                    elapsed_time = time.time() - start
                    boteater.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    boteater.sendMessage(to, "正在重啟...")
                    time.sleep(5)
                    boteater.sendMessage(to, "系統載入完畢")
                    restartBot()
                elif text.lower() == 'errorlog':
                    with open('error.txt', 'r') as er:
                        error = er.read()
                    boteater.sendMessage(to, str(error))          
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    boteater.sendMessage(to, "系統已運行 \n {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        saya = "MIDMU"
                        creator = boteater.getContact(saya)
                        ret_ = ">>> 關於本機 <<<"
                        ret_ += "\n PYTHON 3 測試版 V1.0"
                        ret_ += "\n此為公開型機器"
                        ret_ += "\n作者 : {}".format(creator.displayName)
                        boteater.sendMessage(to, str(ret_))
                    except Exception as e:
                        boteater.sendMessage(msg.to, str(e))
                elif text.lower() == 'status':
                    try:
                        ret_ = " >>> 本機狀態 <<<"
                        if settings["autoAdd"] == True: ret_ += "\n自動加入好友✔"
                        else: ret_ += "\n自動加入好友✘"
                        if settings["autoJoin"] == True: ret_ += "\n自動進群✔"
                        else: ret_ += "\n自動進群✘"
                        if settings["autoLeave"] == True: ret_ += "\n離開副本✔"
                        else: ret_ += "\n離開副本✘"
                        if settings["autoRead"] == True: ret_ += "\n自動已讀✔"
                        else: ret_ += "\n自動已讀✘"
                        if settings["autochecksticker"] == True: ret_ += "\n鑑定貼圖✔"
                        else: ret_ += "\n鑑定貼圖✘"
                        if settings["detectMention"] == True: ret_ += "\n標註回覆✔"
                        else: ret_ += "\n標註回覆✘"
                        ret_ += " "
                        boteater.sendMessage(to, str(ret_))
                    except Exception as e:
                        boteater.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    boteater.sendMessage(to, "自動加入好友✔")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    boteater.sendMessage(to, "自動加入好友✘")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    boteater.sendMessage(to, "自動進群✔")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    boteater.sendMessage(to, "自動進群✘")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    boteater.sendMessage(to, "離開副本✔")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    boteater.sendMessage(to, "離開副本✘")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    boteater.sendMessage(to, "自動已讀✔")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    boteater.sendMessage(to, "自動已讀✘")
                elif text.lower() == 'autochecksticker on':
                    settings["autochecksticker"] = True
                    boteater.sendMessage(to, "鑑定貼圖✔")
                elif text.lower() == 'autochecksticker off':
                    settings["autochecksticker"] = False
                    boteater.sendMessage(to, "鑑定貼圖✘")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    boteater.sendMessage(to, "標註回覆✔")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    boteater.sendMessage(to, "標註回覆✘")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    boteater.sendMessage(to, "請傳送友資以模仿")
#=================================================================#
### SELFBOT COMMAND ###
#=================================================================#
                elif text.lower() == 'me':
                    sendMessageWithMention(to, boteaterMID)
                    boteater.sendContact(to, boteaterMID)
                elif text.lower() == 'mymid':
                    boteater.sendMessage(msg.to,"MID : " +  msg.from_)
                elif text.lower() == 'mypicture':
                    me = boteater.getContact(boteaterMID)
                    boteater.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideo':
                    me = boteater.getContact(boteaterMID)
                    boteater.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = boteater.getContact(boteaterMID)
                    cover = boteater.getProfileCoverURL(boteaterMID)    
                    boteater.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("stealcontact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            mi_d = contact.mid
                            boteater.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("stealmid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "此人MID : "
                        for ls in lists:
                            ret_ += "\n{}" + ls
                        boteater.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("stealname "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            boteater.sendMessage(msg.to, "此人名字 : \n" + contact.displayName)
                elif msg.text.lower().startswith("stealbio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = boteater.getContact(ls)
                            boteater.sendMessage(msg.to, "此人各簽 : \n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("stealpicture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + boteater.getContact(ls).pictureStatus
                            boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealvideoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + boteater.getContact(ls).pictureStatus + "/vp"
                            boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealcover "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = boteater.getProfileCoverURL(ls)
                                boteater.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            boteater.cloneContactProfile(contact)
                            boteater.sendMessage(msg.to, "寶貝我愛你")
                        except:
                            boteater.sendMessage(msg.to, "不要!他好醜")
                            
                elif text.lower() == 'restoreprofile':
                    try:
                        boteaterProfile.displayName = str(myProfile["displayName"])
                        boteaterProfile.statusMessage = str(myProfile["statusMessage"])
                        boteaterProfile.pictureStatus = str(myProfile["pictureStatus"])
                        boteater.updateProfileAttribute(8, boteaterProfile.pictureStatus)
                        boteater.updateProfile(boteaterProfile)
                        boteater.sendMessage(msg.to, "寶貝我不愛妳了")
                    except:
                        boteater.sendMessage(msg.to, "拉機換不回去==")
#=================================================================#
#=======### GROUP COMMAND ###
#=================================================================#
                elif text.lower() == 'crash':
                    boteater.sendContact(to, "ub621484bd88d2486744123db00551d5e',")
                elif text.lower() == 'gcreator':
                    group = boteater.getGroup(to)
                    GS = group.creator.mid
                    boteater.sendContact(to, GS)
                elif text.lower() == 'gpicture':
                    group = boteater.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    boteater.sendImageWithURL(to, path)
                elif text.lower() == 'glink':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            link = boteater.reissueGroupTicket(to)
                            boteater.sendMessage(to, ">> 群組網址 <<<\nhttps://line.me/R/ti/g/{}".format(str(link)))
                        else:
                            boteater.sendMessage(to, "請先開啟群組網址")
                elif text.lower() == 'qr on':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            boteater.sendMessage(to, "群組網址已開啟")
                        else:
                            group.preventedJoinByTicket = False
                            boteater.updateGroup(group)
                            boteater.sendMessage(to, "群組網址已經是開啟的")
                elif text.lower() == 'qr off':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            boteater.sendMessage(to, "群組網址已關閉")
                        else:
                            group.preventedJoinByTicket = True
                            boteater.updateGroup(group)
                            boteater.sendMessage(to, "群組網址已經是關閉的")
                elif text.lower() == 'ginfo':
                    group = boteater.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明(已砍帳)"
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "不開放"
                    else:
                        gQr = "開放"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(boteater.reissueglink(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = ">>> 群組資訊 <<<"
                    ret_ += "\n群組名稱 : {}".format(str(group.name))
                    ret_ += "\n創群者 : {}".format(str(gCreator))
                    ret_ += "\n群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n網址狀態 : {}".format(gQr)
                    ret_ += "\n群組網址 : {}".format(gTicket)
                    boteater.sendMessage(to, str(ret_))
                    boteater.sendImageWithURL(to, path)
                elif text.lower() == 'gmember':
                    if msg.toType == 2:
                        group = boteater.getGroup(to)
                        ret_ = ">>> 都是智障 <<<"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n總共: \n{}".format(str(len(group.members)))
                        boteater.sendMessage(to, str(ret_))
                elif text.lower() == 'glist':
                        groups = boteater.groups
                        ret_ = ">>> 群組列表 <<<"
                        no = 0 + 1
                        for gid in groups:
                            group = boteater.getGroup(gid)
                            ret_ += "\n{}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n總共 : \n{}".format(str(len(groups)))
                        boteater.sendMessage(to, str(ret_))
                        
                elif text.lower() == 'mention':
                    group = boteater.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u' '
                        boteater.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        boteater.sendMessage(to, "總共標註 : \n{}".format(str(len(nama))))          
#=================================================================#
###ELIF COMMAND###
#=================================================================#
                elif text.lower() == 'kalender':
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    boteater.sendMessage(msg.to, readTime)                 
                elif "ssweb" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        boteater.sendImageWithURL(to, data["result"])
                elif "instagraminfo" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.instagram.com/{}/?__a=1".format(search))
                        try:
                            data = json.loads(r.text)
                            ret_ = (">>> IG 查詢結果 {} <<<".format(search))
                            ret_ += "\n名字 : {}".format(str(data["user"]["full_name"]))
                            ret_ += "\n使用者名稱 : {}".format(str(data["user"]["username"]))
                            ret_ += "\n狀態消息 : {}".format(str(data["user"]["biography"]))
                            ret_ += "\n追蹤者 : {}".format(format_number(data["user"]["followed_by"]["count"]))
                            ret_ += "\n追蹤中 : {}".format(format_number(data["user"]["follows"]["count"]))
                            if data["user"]["is_verified"] == True:
                                ret_ += "\n驗證 : 商業"
                            else:
                                ret_ += "\n驗證 : 一般"
                            if data["user"]["is_private"] == True:
                                ret_ += "\n帳號 : 私人"
                            else:
                                ret_ += "\n帳號 : 公開"
                            ret_ += "\n貼文數量 : {}".format(format_number(data["user"]["media"]["count"]))
                            ret_ += "\n追蹤連結 : https://www.instagram.com/{} ]".format(search)
                            path = data["user"]["profile_pic_url_hd"]
                            boteater.sendImageWithURL(to, str(path))
                            boteater.sendMessage(to, str(ret_))
                        except:
                            boteater.sendMessage(to, "查詢不到與此相關的使用者")
                elif "instagrampost" in msg.text.lower():
                    separate = msg.text.split(" ")
                    user = msg.text.replace(separate[0] + " ","")
                    profile = "https://www.instagram.com/" + user
                    with requests.session() as x:
                        x.headers['user-agent'] = 'Mozilla/5.0'
                        end_cursor = ''
                        for count in range(1, 999):
                            print('PAGE: ', count)
                            r = x.get(profile, params={'max_id': end_cursor})
                        
                            data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                            j    = json.loads(data)
                        
                            for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']: 
                                if node['is_video']:
                                    page = 'https://www.instagram.com/p/' + node['code']
                                    r = x.get(page)
                                    url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                                    print(url)
                                    boteater.sendVideoWithURL(msg.to,url)
                                else:
                                    print (node['display_src'])
                                    boteater.sendImageWithURL(msg.to,node['display_src'])
                            end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
                elif "image " in msg.text.lower():
                    separate = msg.text.split(" ")
                    search = msg.text.replace(separate[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(urllib.parse.quote(search)))
                        data = r.text
                        data = json.loads(data)
                        if data["result"] != []:
                            items = data["result"]
                            path = random.choice(items)
                            a = items.index(path)
                            b = len(items)
                            boteater.sendImageWithURL(to, str(path))
                elif "youtubes" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {"search_query": search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.youtube.com/results", params = params)
                        soup = BeautifulSoup(r.content, "html5lib")
                        ret_ = ">>> YOUTUBE 搜尋結果 <<<"
                        datas = []
                        for data in soup.select(".yt-lockup-title > a[title]"):
                            if "&lists" not in data["href"]:
                                datas.append(data)
                        for data in datas:
                            ret_ += "\n影片標題 : {} ".format(str(data["title"]))
                            ret_ += "\n觀賞連結 : https://www.youtube.com{}".format(str(data["href"]))
                        boteater.sendMessage(to, str(ret_))

#=================================================================#
#######################MEDIA#############################
#=================================================================#

                elif text.lower() == 'animelist':
                    data = {
                        'submit2': ''
                        }
                    r = requests.post(url = 'https://boteater.com/anime/', data = data)
                    qr= r.text
                    os.system('rm {}.txt'.format(msg._from))
                    urllib.request.urlretrieve('http://149.28.137.54/animelist.json', '{}.txt'.format(msg._from))
                    links = []
                    juduls = []
                    if r.status_code == 404:
                        boteater.sendMessage(msg.to, 'FAIL!!!')
                    else:
                        j = json.loads(qr)
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        h= ('>>ANIME LIST<<')
                        number= 1
                        try:
                            for numx in range(1000):
                                xx =juduls[numx]
                                h+= ('\n{}. {}'.format(numx, xx))
                                number += 1
                        except:
                            boteater.sendMessage(msg.to, h)
                            boteater.sendMessage(msg.to, 'PLEASE TYPE = EPPLIST [NUMBER]')
                    if text.lower() == 'animenew':
                        data = {
                            'submit1': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        qr= r.text
                        os.system('rm {}.txt'.format(msg._from))
                        urllib.request.urlretrieve('http://149.28.137.54/animebaru.json', '{}.txt'.format(msg._from))
                        links = []
                        juduls = []
                        if r.status_code == 404:
                            boteater.sendMessage(msg.to, 'FAIL!!!')
                        else:
                            j = json.loads(qr)
                            for p in j['result']:
                                juduls.append(p['judul'])
                                links.append(p['link'])
                            h= ('>>ANIME LIST<<')
                            number= 1
                            try:
                                for numx in range(1000):
                                    xx =juduls[numx]
                                    h+= ('\n{}. {}'.format(numx, xx))
                                    number += 1
                            except:
                                boteater.sendMessage(msg.to, h)
                                boteater.sendMessage(msg.to, 'PLEASE TYPE = STREAMEPPZ [NUMBER]')
                elif "epplist " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link2': '{}'.format(xx),
                            'submit4': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        qr= r.text
                        f = open('{}.txt'.format(msg._from),'w')
                        f.write(qr)
                        f.close()
                        links = []
                        juduls = []
                        if r.status_code == 404:
                            boteater.sendMessage(msg.to, 'FAIL!!! SELECT YOUR ANIME FIRST!!!')
                        else:
                            j = json.loads(qr)
                            for p in j['result']:
                                juduls.append(p['epp'])
                                links.append(p['link'])
                            h= ('>>EPISODE LIST LIST<< \n>>{}<<'.format(xxx))
                            number= 1
                            try:
                                for numx in range(1000):
                                     zzz =juduls[numx]
                                     h+= ('\n{}. {}'.format(numx, zzz))
                                     number += 1
                            except:
                                boteater.sendMessage(msg.to, h)
                                boteater.sendMessage(msg.to, 'PLEASE TYPE = STREAMEPP [NUMBER]')
                                if juduls in ["", "\n", " ",  None]:
                                    boteater.sendMessage(msg.to, 'LINK ANIME IS DIED!!')
                elif "streamepp " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['epp'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link1': '{}'.format(xx),
                            'submit3': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        link= r.text
                        boteater.sendMessage(msg.to, ">> STREAM ANIME<< \n>> {} << \n{}".format(xxx, link))
                elif "streameppz " in msg.text.lower():
                    separate = msg.text.split(" ")
                    numf = msg.text.replace(separate[0] + " ","")
                    numzz = int(numf)
                    numz = numzz
                    with open('{}.txt'.format(msg._from), 'r') as f:
                        qr = f.read()
                        j = json.loads(qr)
                        juduls = []
                        links = []
                        for p in j['result']:
                            juduls.append(p['judul'])
                            links.append(p['link'])
                        xx =links[numz]
                        xxx =juduls[numz]
                        data = {
                            'link1': '{}'.format(xx),
                            'submit3': ''
                            }
                        r = requests.post(url = 'https://boteater.com/anime/', data = data)
                        link= r.text
                        boteater.sendMessage(msg.to, ">> STREAM ANIME<< \n>> {} << \n{}".format(xxx, link))
#=================================================================#
#                                       LOGIN TOKEN.   
#=================================================================#
                elif text.lower() == 'token mac':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit4': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token win10':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit3': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token ios':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit2': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token chrome':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit1': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token desktop':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit7': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(msg.to, '{}'.format(qr))
                elif text.lower() == 'token done':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit5': ''
                    
                    }
                    post_response = requests.post(url = 'https://boteater.com/sniff/', data = data)
                    qr = post_response.text
                    boteater.sendMessage(to, "TOKEN已經由私聊傳送")
                    boteater.sendMessage(msg.to, '{}'.format(qr))
#=================================================================#
#=================================================================#
#=================================================================#
            elif msg.contentType == 7:
                if settings["autochecksticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = ">>> 貼圖資訊 <<<"
                    ret_ += "\n貼圖ID : {}".format(stk_id)
                    ret_ += "\n貼圖連結 : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n>>鑑定完畢<<"
                    boteater.sendMessage(to, str(ret_))
                    
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = boteater.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        boteater.sendText(msg.to, "沒有可複製對象")
                        pass
                    else:
                        for target in targets:
                            try:
                                boteater.cloneContactProfile(target)
                                boteater.sendMessage(msg.to, "成功複製目標")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
#=================================================================#
#=================================================================#
#=================================================================#
#=================================================================#
        if op.type == 26:
            print ("通知:收到訊息")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != boteater.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    boteater.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        boteater.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in boteaterMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if boteaterMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = boteater.getContact(sender)
                                    boteater.sendMessage(to, "sundala nu")
                                    sendMessageWithMention(to, contact.mid)
                                break
#=================================================================#
#=================================================================#
        if op.type == 55:
            print ("通知:已讀訊息")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#=================================================================#
#=================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
