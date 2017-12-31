# -*- coding:utf-8 -*-
# Eng_SnS_Manga_Crawler
import os
import re
import sys
import traceback
import urllib
import urllib2
import time
import cPickle as pickle


def build_folder(p):
    if not os.path.exists(p):
        os.mkdir(p)

# 截取话数
def no_get(u):
    return int(re.match(reg1,u).group().strip(' -'))

def get_dl(z, y, x, w):
    print 'Yes, <{}> chapter(s) need to be downloaded!'.format(y)
    cd(z)
    build_folder(path + x)
    count = 0
    r_new = urllib2.urlopen(urllib2.Request(url= w, headers=send_headers))
    html_c = r_new.read()
    li_list = re.findall(reg2, html_c) # 含尾页数
    img_src0 = re.findall(reg3, html_c) # 第一张;每页所含图
    last_pno = li_list[-1]

    img_src_list.extend(img_src0) # 加入第一张图
    [url_c_list.append(w[0:-1] + str(n)) for n in xrange(2, int(last_pno) + 1)]
    [img_src_list.extend(re.findall(reg3, urllib2.urlopen(urllib2.Request(url=i, headers=send_headers)).read())) for i in url_c_list]
    print 'Valid Image Url Numbers: <{}>\nLast Page Number: <{}>\n'.format(len(img_src_list), last_pno)
    for p in img_src_list: # start download
        img_name = re.findall(reg4, p)[0] # 原名
        result = re.findall(reg5, img_name)
        if len(result) != 0:
            if int(img_name[:2]) < 10:
                img_rename = img_name[:2] + result[0][1]
            else:
                img_rename = img_name[:2] + result[0][3]
            urllib.urlretrieve('https:' + p, path + x + '/' + img_rename)
            print '{} --> {}  √'.format(img_name, img_rename)
        else:
            urllib.urlretrieve('https:' + p, path + x + '/' + img_name)
            print img_name, ' √'
        count += 1
    print 'Download Counts: <{}>'.format(count)
    if count == int(last_pno):
        print '\n<%s>/%s pages of <%s> downloaded' % (count, last_pno, x)
    else:
        print u'エラーが発生しました'
    update_log(x)

def update_log(c):
    with open(path+u'本地更至.txt','wb') as f:
        ts = time.strftime('%Y/%m/%d %H:%M:%S')
        pickle.dump(c+'@'+ts, f)

def cd(t):
    while t > 0:
        sys.stdout.write('\rTime break: {}s'.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)

def do():
    with open(path+u'本地更至.txt','rb') as f1:
        local_cnt = pickle.loads(f1.read())
    if chpt_no_latest - no_get(local_cnt) == 0:
        print "Latest Chapter already Updated"
    elif chpt_no_latest - no_get(local_cnt) == 1:
        get_dl(5, 1, chpt[0][1], chpt_lk_list[0])
    elif chpt_no_latest - no_get(local_cnt) == 2:
        get_dl(5, 2, chpt[1][1], chpt_lk_list[1])
        get_dl(5, 1, chpt[0][1], chpt_lk_list[0])
    elif chpt_no_latest - no_get(local_cnt) >= 3:
        get_dl(5, 3, chpt[2][1], chpt_lk_list[2])
        get_dl(5, 2, chpt[1][1], chpt_lk_list[1])
        get_dl(5, 1, chpt[0][1], chpt_lk_list[0])
    else:
        print "Make a check!\nlatest ONLINE No.: {}\n latest LOCAL No.: {}".format(*[chpt_no_latest, no_get(local_cnt)])
    time.sleep(5)
    sys.exit()

if __name__ == "__main__":
    try:
        path = unicode("D:/迅雷下载/Shokugeki Manga Eng/", "utf-8")
        # 进入更新母页获取子页链接
        url_m = "https://readms.net/manga/shokugeki_no_souma"
        send_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://readms.net/manga/shokugeki_no_souma', # Anti-Anti-Hotlinking
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
        }

        req = urllib2.Request(url=url_m, headers=send_headers)
        r = urllib2.urlopen(req)
        html_m = r.read() # 返回的网页内容
        # receive_header = r.info() # 返回的报头信息
        # html_m = html_m.decode('utf-8','replace').encode(sys.getfilesystemencoding()) # 转码:避免输出出现乱码
        # print html_m

        reg = re.compile(r'<a href="(/r/shokugeki_no_souma/.+)">(.+)</a>') # group
        reg1 = re.compile(r'\d+ -') # title No., deliberately
        reg2 = re.compile(r'<li><a href="/r/shokugeki_no_souma/\d+/\d+/(\d+)">.+</a></li>')
        reg3 = re.compile(r'<img id="manga-page" src="(.+)"')
        reg4 = re.compile(r'//.+/\d+/\d+/(.+\.(?:jpg|png))') # non-capturing group, avoiding possible later .group(n)
        reg5 = re.compile(r'(0\d(?:1|2))(\D{4,5})|(1\d(?:1|2))(\D{4,5})') # for instances like 012.png/031.jpeg/161.png

        chpt = re.findall(reg, html_m) # 返回一个list,只含四物
        chpt_lk_list = ['https://readms.net' + chpt[0][0], 'https://readms.net' + chpt[1][0], 'https://readms.net' + chpt[2][0], 'https://readms.net' + chpt[3][0]]
        chpt_no_latest = no_get(chpt[0][1])

        url_c_list = [] # 第一页chpt_lk_list[0]就不放进去了,因为能同时获得第一张图
        img_src_list = []

        # 更新记录在,则读取更新话数
        if os.path.exists(path+u'本地更至.txt'):
            do()
        else: # 若更新记录不存在,获取本地文件夹的序号
            files= os.listdir(path)
            f_no = [f for f in files if os.path.isdir(path+f)]
            f_no.sort(reverse = True)
            update_log(f_no[0])
            do()
    except Exception,e:
        traceback.print_exc(file=open(path+'errlog.txt','wb')) # log error