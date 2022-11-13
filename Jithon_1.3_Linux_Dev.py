import sys
import traceback #bug捕获
import os
import re #正则表达式
import time #时间
from base64 import b64decode#二维码编码

import requests


#初始化
local_time = time.strftime("%y/%m/%d", time.localtime())
brower = requests.Session()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

base_url = "http://127.0.0.1:64000"#默认端口
local_dir =os.getcwd()#默认下载地址
appdata = os.getenv('APPDATA')#获取系统变量
os.makedirs(local_dir+'/temp',exist_ok=True)#创建临时文件夹

#清洗保存文件名
def clean_name(strs):
    strs = re.sub(r'/:<>?/\^|', "",strs)
    # 去除不可见字符
    return strs

#列表排序
def dic(info):
    new_list = []#创建临时列表
    for a in info:
        new_list.append(a["quality"])
    new_list.sort(reverse = True)#列表排序从大到小
    new_info = []
    for b in new_list:
        for c in info:
            if c["quality"] == b:
                new_info.append(c)
    return new_info



#浏览器请求函数
def get(url):
    try:
        #cj = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
        response = brower.get(url=url,headers={
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "origin": "https://space.bilibili.com"
            }).json()
        return response
    except:
        print('核心未启动,尝试重新访问核心')
        time.sleep(1)
        get(url)

#浏览器发送函数
def post(url,json):
    response = brower.post(url=url,json=json,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "origin": "https://space.bilibili.com"
        }).json()
    return response

#添加编码信息
def code(keys):
    if keys['codec'] == 0:
        keys['codec'] = 'NONE'
    if keys['codec'] == 1:
        keys['codec'] = 'H264'
    if keys['codec'] == 2:
        keys['codec'] = 'H265'
    if keys['codec'] == 3:
        keys['codec'] = 'AV1'
    if keys['codec'] == 4:
        keys['codec'] = 'M4A'
    if keys['codec'] == 5:
        keys['codec'] = 'DOLBY'
    return keys

#获取登录状态
def get_user_info():
    data = get(base_url+'/bili/user/get_user_info')
    if data['message'] == "no login":
        print('用户未登录')
        return
    user_data = data['data']
    is_login = user_data['is_login']
    uname = user_data['uname']
    vip_status = user_data['vip_status']
    vip_label_text = user_data['vip_label_text']
    if is_login == True :
        if vip_status == True:
            print('当前登录用户: '+uname+' ['+vip_label_text+']')
        if vip_status != True:
            print('当前登录用户: '+uname+' [普通用户]')
        #全局声明当前用户ID
        global mid
        mid = user_data['mid']

#获取下载目录
def get_down_dir():
    data = get(base_url+"/jijidown/settings/get_download_dir")
    data = data['data']
    return data

#更改下载目录
def change_down_dir(down_dir):
    json = {'dir': down_dir}
    post(base_url+'/jijidown/settings/set_download_dir',json)

#登录
def login():
    data = get(base_url+'/bili/user/tv/get_login_status')
    login_data =data['data']
    login_successful = login_data['login_successful']
    login_image = login_data['image']
    if login_successful != True:
        print('从核心获取登录二维码,扫码完成后按回车继续')
        input()
        login_image = b64decode(login_image)
        os.makedirs(os.getcwd()+'/temp',exist_ok=True)
        with open(os.getcwd()+'/temp/1.png','wb+') as f:
            f.write(login_image)
    if login_successful == True:
        print('用户已登录')
    get_user_info()



#获取分辨率
def quality(video_info):

    #获取指定分P清晰度
        one_video_info = get(base_url+'/bili/1/'+str(video_info['page_av'])+'/'+str(video_info['page_cid'])+'/get_video_quality')
        one_video_info = one_video_info['data']['list']

        new_video_info = {}#新建分辨率排序
        new_video_info['WEB'] = {}
        new_video_info['WEB']['audio'] = []
        new_video_info['WEB']['video'] = []
        new_video_info['TV'] = {}
        new_video_info['TV']['audio'] = []
        new_video_info['TV']['video'] = []
        new_video_info['APP'] = {}
        new_video_info['APP']['audio'] = []
        new_video_info['APP']['video'] = []

        for quality in one_video_info:#分类
            quality = code(quality)
            if quality["api_type"] == 0:
                if quality["is_audio"] == True:
                    new_video_info['WEB']['audio'].append(quality)
                    continue
                if quality["is_video"] == True:
                    new_video_info['WEB']['video'].append(quality)
                    continue

            if quality["api_type"] == 1:
                if quality["is_audio"] == True:
                    new_video_info['TV']['audio'].append(quality)
                    continue
                if quality["is_video"] == True:
                    new_video_info['TV']['video'].append(quality)
                    continue

            if quality["api_type"] == 2:
                if quality["is_audio"] == True:
                    new_video_info['APP']['audio'].append(quality)
                    continue
                if quality["is_video"] == True:
                    new_video_info['APP']['video'].append(quality)
                    continue


        #排序
        new_video_info['WEB']['audio'] = dic(new_video_info['WEB']['audio'])
        new_video_info['WEB']['video'] = dic(new_video_info['WEB']['video'])
        new_video_info['TV']['audio'] = dic(new_video_info['TV']['audio'])
        new_video_info['TV']['video'] = dic(new_video_info['TV']['video'])
        new_video_info['APP']['audio'] = dic(new_video_info['APP']['audio'])
        new_video_info['APP']['video'] = dic(new_video_info['APP']['video'])

        return new_video_info

#选择分辨率
def choice_quality(info):
        download_list = info
        while 1 == 1:
            #选择接口
            while 1 == 1:
                if len(download_list['TV']['video']) == 0:
                    answer = input('选择下载接口 WEB/APP(1/2) (本视频不支持TV通道)（输入0返回上一层）:')
                if not len(download_list['TV']['video']) == 0:
                    answer = input('选择下载接口 WEB/APP/TV(1/2/3)(输入0返回上一层） :')

                #输入0返回上一层
                if answer == '0':
                    return 'null'
                if answer == '1':
                    choice = 1
                    sb = 0
                    print('视频列表')
                    for info in download_list['WEB']['video']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    sb = 0
                    print('音频列表')
                    for info in download_list['WEB']['audio']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    break

                if answer == '3' and not len(download_list['TV']['video']) == 0:
                    choice = 2
                    sb = 0
                    print('视频列表')
                    for info in download_list['TV']['video']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    sb = 0
                    print('音频列表')
                    for info in download_list['TV']['audio']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    break

                if answer == '2':
                    choice = 3
                    sb = 0
                    print('视频列表')
                    for info in download_list['APP']['video']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    sb = 0
                    print('音频列表')
                    for info in download_list['APP']['audio']:
                        sb+=1
                        print(str(sb)+'. '+info['quality_str']+'  '+info['codec']+'  '+info['bit_rate']+'   '+info['stream_size'])
                    break
                print('输入不正确，请重试')

            #选择分辨率
            while 1 == 1:
                try:
                    answer = input('选择分辨率(视频编号;音频编号)(输入0返回）')
                    if choice == 1:
                        api = 'WEB'
                    if choice == 2:
                        api = 'TV'
                    if choice == 3:
                        api = 'APP'

                    #返回上一层
                    if answer == '0':
                        break

                    need_down = answer.split(';')#拆分数字序号
                    down_quality = []#定义需下载分辨率列表
                    if len(download_list[api]['video'])>= int(need_down[0]) and int(need_down[0]) > 0:#校验序号合理性
                        down_quality.append(download_list[api]['video'][int(need_down[0])-1])
                    if len(download_list[api]['audio'])>= int(need_down[1]) and int(need_down[1]) > 0:#校验序号合理性
                        down_quality.append(download_list[api]['audio'][int(need_down[1])-1])
                        if choice == 1:
                            down_quality.append(0)
                        if choice == 2:
                            down_quality.append(1)
                        if choice == 3:
                            down_quality.append(2)

                        return down_quality
                    print('输入不正确，请重试')
                except:
                    print('输入不正确，请重试')
#获取视频信息
def get_video_info(url):
    #判断输入url类型
    if "BV" in url:
        video_info = re.findall('BV(..........)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/2/BV"+video_info+"/get_video_info")
    elif "av" in url:
        video_info = re.findall('av(\d*)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/1/"+video_info+"/get_video_info")
    elif "b23.tv" in url:
        url = re.findall('(https://b23.tv/.......)',url)[0]
        video_info = requests.get(url,allow_redirects=False).text
        get_video_info(video_info)

    elif "ep" in url:
        video_info = re.findall('ep(\d*)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/3/"+video_info+"/get_video_info")
    elif "ss" in url:
        video_info = re.findall('ss(\d*)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/4/"+video_info+"/get_video_info")
    elif "av" in url:
        video_info = re.findall('av(\d*)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/1/"+video_info+"/get_video_info")
    elif "av" in url:
        video_info = re.findall('av(\d*)',url)[0]
        #向核心发起通讯获取视频信息
        video_info = get(base_url+"/bili/1/"+video_info+"/get_video_info")

    else:
        print('视频链接不正确')
        return '0'
    return video_info

#下载弹幕数据
def danmu(avid,cid,name):
    answer = get(base_url+'/danmaku/'+str(avid)+'/'+str(cid)+'/download_danmaku?file='+name)
    if answer['code'] == 0:
        print('弹幕数据下载成功')
        return
    print('弹幕数据下载出错')
    time.sleep(1)
    danmu(info)

#新建任务函数
def new_task(info,down_quality,mode):
    if mode == 0:
            video_quality = down_quality[0]['quality']#视频
            audio_quality = down_quality[1]['quality']#音频
            api_type = down_quality[2]#接口类型

    filename = info['video_filename']
    if mode == 0:
        json={
            "avid": info['page_av'],
            "cid": info['page_cid'],
            "video_quality": video_quality,
            "audio_quality": audio_quality,
            "api_type": api_type,
            "useav": True,
            "useflv": False,
            "video_codecs": 1,
            "video_filename": filename
        }
    elif mode == 1:
        json={
            "avid": info['page_av'],
            "cid": info['page_cid'],
            "video_quality": 1000,
            "useav": True,
            "useflv": False,
            "videocodecs": 1,
            "video_filename": filename
        }
    post(base_url+'/task/post_new_task',json)
    danmu(info['page_av'],info['page_cid'],filename)

#下载函数
def download(url):
    video_info = get_video_info(url)#获取视频信息
    if video_info == '0':
        return

    #解析视频信息
    video_title = video_info["data"]["video_title"]#视频标题
    video_desc = video_info["data"]["video_desc"]#描述
    up_name = video_info["data"]["up_name"]#up用户名
    bili_pubdate_str = video_info['data']['bili_pubdate_str']#上传时间
    video_cover = video_info["data"]["video_cover"]#封面
    video_list = video_info["data"]["list"]#视频列表
    sort = video_info["data"]["sort"]#链接类型

    #显示视频信息
    print('标题：'+video_title)
    print('类型：'+sort)
    print('UP主：'+up_name)
    print('\n'+'简介：'+video_desc+'\n')
    print('上传时间：'+bili_pubdate_str)
    print('\n共有'+str(len(video_list))+'个分P'+'\n')
    for video_list_every in video_list:#遍历视频列表
        print(str(video_list_every['page'])+'.'+video_list_every['page_title'])

    while 1 == 1:
        #若分P列表中仅有一个视频直接进入分辨率选择
        if len(video_list) == 1:
            download_list = video_list
            #选择默认下载分辨率
            answer = input('是否使用默认最高分辨率下载（否请输入N/n)(取消下载输入0）')
            moreng = 1
            #取消下载
            if answer == '0':
                print('下载已取消')
                return
            if answer == 'N' or answer == 'n':
                print('正在获取可使用的分辨率。。。。')
                moreng = 0
                down_quality = choice_quality(quality(video_list[0]))#选择分辨率
                #返回上一层
                if down_quality == 'null':
                    continue
                if down_quality != 'null':
                    break


        if len(video_list) > 1:
            while 1==1:
                try:
                    #获取需下载分P列表
                    answer = input('请输入所需下载视频数字序号，中间用；分隔，若全部下载请直接回车 ：')
                    if len(answer) == 0:#若全部下载
                        download_list = video_list
                        break
                    if len(answer) > 0:#获取需要下载目录
                        need_down = answer.split(';')#拆分数字序号
                        new_list = []
                        for need_number in need_down:#追加需要下载分P
                            new_list.append(video_list[int(need_number)-1])
                        download_list = new_list
                        break
                except:
                    print('输入不正确，请重新输入')
        #选择默认下载分辨率
        answer = input('是否使用默认最高分辨率下载（否请输入N/n)(取消下载输入0）')
        moreng = 1
        #取消下载
        if answer == '0':
            print('下载已取消')
        if answer == 'N' or answer == 'n':
            print('正在获取可使用的分辨率。。。。')
            moreng = 0
            down_quality = choice_quality(quality(video_list[0]))#选择分辨率
            #输入0返回上一层
            if down_quality == 'null':
                continue
            if down_quality != 'null':
                break

    #建立下载任务
    for down in download_list:
        if moreng == 1:
            new_task(down,1000,1)
            continue
        new_task(down,down_quality,0)

    print(str(len(download_list))+'个任务已发送至核心')




#主函数
print('Jithon 鸡枞v1.4 Linux Dev')
print('Power by python')
print('Made in Mr.G')
print('程序初始化。。。。')

#获取登录状态
try:
    get_user_info()
except:
    print('用户未登录')

while 1==1:
        answer = input('请粘贴视频地址(输入set调整设置,输入login进行登录,输入user查看,输入exit退出)：')
        if answer == 'set':
            while 1==1:
                down_dir = get_down_dir()
                print('1.当前下载目录：'+down_dir['dir'])
                answer = input('输入1修改设置(输入0退出)：')
                if answer == '0':
                    break
                if answer == '1':
                    answer = input('输入新指定的下载目录（若留空指定为'+local_dir+'/Download）：')
                    if answer == '':
                        os.makedirs(local_dir+'/Download',exist_ok=True)
                        change_down_dir(local_dir+'/Download')
                        print('已修改下载目录')
                        continue
                    if answer != '':
                        os.makedirs(answer,exist_ok=True)
                        if os.path.exists(answer):
                            print('下载目录存在')
                            change_down_dir(answer)
                            print('已修改下载目录')
                            continue
                print('输入不正确')
            continue
        if answer == 'login':
            login()
            continue
        if answer == 'user':
            get_user_info()
            continue
        if answer == 'exit':
            sys.exit()
        download(answer)
