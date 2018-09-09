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

def dl(m, o , x, v):
    for p in m:
        img_name = re.findall(reg4, p)[0] # 原名
        nose = img_name.split('.')[0]
        tail = '.' + img_name.split('.')[1]  # extension
        conj = re.findall(reg5, nose)
        if len(conj) != 0:  # filter 55/54/53/52/45/44/43/42/35/34/33/32/22/23/24/25 type like '00181-0019.jpg', '0012-00193.png', '00071-00082.jpeg', '0009-0010.png', '08-00091.jpg', '0011-122.jpg', '0022_23.jpg', '10-11.png', '02-03.jpg' etc.
            re_name = conj[0][0] + conj[0][1] + conj[0][2] + tail
            urllib.urlretrieve('https:' + p, path + x + '/' + re_name)
            print '{} --> {}   OK --- br. 1'.format(img_name, re_name)
        else:  # - or _ exclusive
            if len(nose) == 2:  # 2-digit type I
                urllib.urlretrieve('https:' + p, path + x + '/' + img_name)
                print img_name, '  OK --- orig.'
            elif len(nose) == 3 and re.search(r'[a-z]', nose) == None:  # 2-digit type II
                re_name = nose[:2] + tail
                urllib.urlretrieve('https:' + p, path + x + '/' + re_name)
                print '{} --> {}   OK --- br. 2'.format(img_name, re_name)
            elif len(nose) >= 4 and re.search(r'[a-z]', nose) == None:  # 00(00).png 00(07).jpg 00(21).png; exclude 0(05)1.png whose type's nonexistent by far
                re_name = nose[2:4] + tail
                urllib.urlretrieve('https:' + p, path + x + '/' + re_name)
                print '{} --> {}   OK --- br. 3'.format(img_name, re_name)
            else: # including 01a.jpg, 0001a.jpg
                print img_name, '  OK --- Skip'
                o += 1
                continue
        o += 1
    print '\nDownload Counts: <{}>'.format(o)
    if o == int(v):
        print '[%s]/%s pages of [%s] -- Process End！\n\n' % (o, v, x)
    else:
        print u'エラーが発生しました'

def get_dl(z, y, x, w):
    print '[{}] chapter(s) left!'.format(y)
    cd(z)
    print '\n[{}] -- Process Start...'.format(x)
    build_folder(path + x)

    url_c_list = [] # 第一页chpt_lk_list[0]就不放进去了,因为能同时获得第一张图
    img_src_list = []  ##上一行与这行移到函数中, 不然一次下几话的情况时会导致重复添加##

    count = 0
    r_new = urllib2.urlopen(urllib2.Request(url= w, headers=send_headers))
    html_c = r_new.read()
    li_list = re.findall(reg2, html_c) # 含尾页数
    img_src0 = re.findall(reg3, html_c) # 第一张;每页所含图
    last_pno = li_list[-1]

    img_src_list.extend(img_src0) # 加入第一张图
    [url_c_list.append(w[0:-1] + str(n)) for n in xrange(2, int(last_pno) + 1)]
    [img_src_list.extend(re.findall(reg3, urllib2.urlopen(urllib2.Request(url=i, headers=send_headers)).read())) for i in url_c_list]
    print 'Valid Image Url Counts: <{}>\nLast Page Number: <{}>\n'.format(len(img_src_list), last_pno)
    # print 'img_src_list: '+str(img_src_list)
    dl(img_src_list, count, x, last_pno)
    update_log(x)

def update_log(c):
    with open(path+u'本地更至.txt','wb') as f:
        ts = time.strftime('%Y/%m/%d %H:%M:%S')
        pickle.dump(c+'@'+ts, f)

def cd(t):
    while t >= 0: # 加了“=”
        sys.stdout.write('\rTime lapse: {}s'.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)

def do():
    with open(path+u'本地更至.txt','rb') as f1:
        local_cnt = pickle.loads(f1.read())
    chpt_no_local = no_get(local_cnt)
    diff = chpt_no_latest - chpt_no_local
    if diff == 0:
        print "Latest Chapter Already!"
    elif diff <= 4: ##目前站点上仅保留4话##
        for d in xrange(diff):
            if re.search(r'[:*?"<>|]', chpt[diff-1][1]) != None:
                rpl = (':', '：'), ('*', '×'), ('?', '？'), ('"', '\''), ('<', '《'), ('>', '》'), ('|', '-')
                tp = chpt[diff-1][1]
                tp = reduce(lambda a, b: a.replace(*b), rpl, tp) # directly manipulating tuple items are illegal, so a third party is needed;replace some half-width special characters with corresponding full-width chars
                get_dl(5, diff, tp, chpt_lk_list[diff-1])
            else:
                get_dl(5, diff, chpt[diff-1][1], chpt_lk_list[diff-1])
            diff -= 1
    else:
        print "Make a check!\nlatest ONLINE No.: {}\n latest LOCAL No.: {}".format(*[chpt_no_latest, chpt_no_local])
    time.sleep(5)
    sys.exit()

if __name__ == "__main__":
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8') # Added for tp.replace, thus prior unicode decoding methods go redundant and I just let this go.
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

        reg = re.compile(r'<td><a href="(/r/shokugeki_no_souma/.+)">(.+)</a></td>') # group
        reg1 = re.compile(r'\d+ -') # title No., deliberately
        reg2 = re.compile(r'<li><a href="/r/shokugeki_no_souma/\d+/\d+/(\d+)">.+</a></li>')
        reg3 = re.compile(r'<img id="manga-page"\s{1,2}?src="(.+)"') # on 180218 site's html unexpectedly gives me 2 spaces
        reg4 = re.compile(r'//.+/\d+/\d+/(.+\.(?:jpg|png))') # non-capturing group, avoiding possible later .group(n)
        reg5 = re.compile(r'(?:00)?(\d{2})\d?(-|_)(?:00)?(\d{2})\d?')

        chpt = re.findall(reg, html_m) # 返回一个list,只含四物
        chpt_lk_list = ['https://readms.net' + chpt[0][0], 'https://readms.net' + chpt[1][0], 'https://readms.net' + chpt[2][0], 'https://readms.net' + chpt[3][0]]
        chpt_no_latest = no_get(chpt[0][1])

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
        traceback.print_exc()
        traceback.print_exc(file=open(path+'errlog.txt','wb')) # log error