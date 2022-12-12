import sys
import traceback  # bug捕获
import os
import re  # 正则表达式
import time  # 时间
from base64 import b64decode  # 二维码编码

import requests

# 初始化
local_time = time.strftime("%y/%m/%d", time.localtime())
brower = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

base_url = "http://127.0.0.1:64000"  # 默认端口
local_dir = os.getcwd()  # 默认下载地址
appdata = os.getenv('APPDATA')  # 获取系统变量
os.makedirs(local_dir+'/temp', exist_ok=True)  # 创建临时文件夹

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


# 浏览器请求函数
def get(url: str) -> dict:
    """
    请求数据
    """
    try:
        # cj = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
        response: dict = brower.get(url=url, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
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

# 浏览器发送函数


def post(url: str, json: str) -> dict:
    """
    发送json格式信息
    """
    response = brower.post(url=url, json=json, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "origin": "https://space.bilibili.com"
    }).json()
    return response

# User层
# 获取登录状态


def get_user_info() -> dict:
    """
    获取用户登陆状态
    mid = int 用户mid
    is_login = bool 登陆状态
    uname = str 用户名
    face = str 用户头像url
    vip_status = bool 大会员登陆状态
    vip_label_text = str 大会员状态
    """
    data: dict = get(base_url+'/bili/user/get_user_info')
    if data['message'] == "no login":
        return {'code': False}  # 返回状态
    user_data = data['data']
    mid: int = user_data['mid']  # 用户mid
    is_login: bool = user_data['is_login']  # 登录状态
    uname: str = user_data['uname']  # 用户名
    face: str = user_data['face']  # 用户头像
    vip_status: bool = user_data['vip_status']  # 大会员登录状态
    vip_label_text: str = user_data['vip_label_text']  # 大会员状态（年度大会员等）
    return {'code': True, 'mid': mid, 'is_login': is_login, 'uname': uname, 'face': face, 'vip_status': vip_status, 'vip_label_text': vip_label_text}

# 获取登录二维码


def get_login_status() -> dict:
    """
    获取登录二维码
    code = 0为已登录
    二维码保存至/temp/1.png
    """
    data = get(base_url+'/bili/user/tv/get_login_status')
    login_data = data['data']
    login_successful: bool = login_data['login_successful']  # 是否已登录
    login_image = login_data['image']  # 登录用二维码
    if login_successful != True:
        login_image = b64decode(login_image)  # 转换为图片
        os.makedirs(os.getcwd()+'/temp', exist_ok=True)
        with open(os.getcwd()+'/temp/1.png', 'wb+') as f:  # 写入图片
            f.write(login_image)
        return {'code': 1}
    return {'code': 0}

# Jiji层

# 获取下载目录


def get_down_dir() -> str:
    """
    返回下载目录
    """
    data = get(base_url+"/jijidown/settings/get_download_dir")
    data = data['data']
    return data['dir']

# 更改下载目录


def change_down_dir(down_dir: str):
    """
    修改下载目录
    """
    json = {'dir': down_dir}
    post(base_url+'/jijidown/settings/set_download_dir', json)


def ad() -> dict:
    """
    获取ad
    title = str 标题
    url = str 链接
    img = str 图片内容，转成bit进行显示
    """
    data = get(base_url+"/jijidown/ad")
    return data['data']


################################################################### video info层
#获取视频信息
def info(type: int, id: str) -> dict:
    """
    获取不同类型的视频信息
    1为AV类型 2 为BV类型 3为EP类型 4为SS类型 5为MEDIA类型 6为UP类型 7为FAV类型 8为UP主合集 9为UP主列表
    返回信息示例
    {
        "code": 0,
        "message": "",
        "data": {
                "id": 247906246,
                "link_type": 1,
                "video_cover": "http://i1.hdslb.com/bfs/archive/34f668b39d9ce216a644c79df8ddc70ad1b61c8c.jpg",
                "video_title": "完全疯了！清凉水手妹「So Crazy」甜蜜夏日！",
                "video_filename": "完全疯了！清凉水手妹「So Crazy」甜蜜夏日！",
                "video_desc": "歌曲&舞蹈：T-ara -so crazy\n摄影：亚特兰\n后期：面面桑，M子\n后勤：凌柒",
                "sub_sort": "明星舞蹈",
                "sort": "舞蹈",
                "up_name": "早上好七七",
                "up_mid": 1851105,
                "up_face": "https://i0.hdslb.com/bfs/face/111ea36c816eb52385d566e5d38221c960c255a0.jpg",
                "bili_pubdate_str": "2021-05-03 19:20:12",
                "is_stein_gate": false,
                "list": [
                        {
                                "page_av": 247906246,
                                "page_bv": "BV1sv411j7F8",
                                "page_cid": 332978921,
                                "duration": 106,
                                "page": 1,
                                "page_name": "1.完全疯了！清凉水手妹「So Crazy」甜蜜夏日！",
                                "page_title": "so crazy",
                                "video_title": "完全疯了！清凉水手妹「So Crazy」甜蜜夏日！",
                                "video_filename": "完全疯了！清凉水手妹「So Crazy」甜蜜夏日！ - 1.so crazy",
                                "is_bangumi": false
                        }
                ]
        }
}
    """
    data = get(base_url+'/bili/'+str(type)+'/'+str(id)+'/get_video_info')
    return data
################################################################## video quality层

# 获取分辨率


def quality(av: int, cid: int) -> dict:
    """
    获取视频清晰度
    av 为视频AV号 cid 为分P的id
    """
    # 获取指定分P清晰度
    one_video_info = get(base_url+'/bili/1/'+str(av) +
                         '/'+str(cid)+'/get_video_quality')
    one_video_info = one_video_info['data']['list']

    new_video_info = {}  # 新建分辨率排序
    new_video_info['WEB'] = {}
    new_video_info['WEB']['audio'] = []
    new_video_info['WEB']['video'] = []
    new_video_info['TV'] = {}
    new_video_info['TV']['audio'] = []
    new_video_info['TV']['video'] = []
    new_video_info['APP'] = {}
    new_video_info['APP']['audio'] = []
    new_video_info['APP']['video'] = []

    for quality in one_video_info:  # 分类
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

    # 排序
    new_video_info['WEB']['audio'] = dic(new_video_info['WEB']['audio'])
    new_video_info['WEB']['video'] = dic(new_video_info['WEB']['video'])
    new_video_info['TV']['audio'] = dic(new_video_info['TV']['audio'])
    new_video_info['TV']['video'] = dic(new_video_info['TV']['video'])
    new_video_info['APP']['audio'] = dic(new_video_info['APP']['audio'])
    new_video_info['APP']['video'] = dic(new_video_info['APP']['video'])

    return new_video_info

