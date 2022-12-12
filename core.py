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

#获取登录状态
def get_user_info() -> dict:
    """
    获取用户登陆状态
    """
    data = get(base_url+'/bili/user/get_user_info')
    if data['message'] == "no login":
        return {'code':False}#返回状态
    user_data = data['data']
    mid:int = user_data['mid']#用户mid
    is_login:bool = user_data['is_login']#登录状态
    uname:str = user_data['uname']#用户名
    face:str = user_data['face']#用户头像
    vip_status:bool = user_data['vip_status']#大会员登录状态
    vip_label_text:str = user_data['vip_label_text']#大会员状态（年度大会员等）
    return {'code':True,'mid':mid,'is_login':is_login,'uname':uname,'face':face,'vip_status':vip_status,'vip_label_text'}
