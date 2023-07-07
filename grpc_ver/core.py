import os
import json
import time
from base64 import b64decode  # 二维码编码
from pathlib import Path #路径库
import hashlib#sha256加密库

import wget
import requests

import grpc

from grpc_core import user_pb2
from grpc_core import user_pb2_grpc
from grpc_core import task_pb2
from grpc_core import task_pb2_grpc
from grpc_core import status_pb2
from grpc_core import status_pb2_grpc
from grpc_core import bvideo_pb2
from grpc_core import bvideo_pb2_grpc


# 初始化
local_core = str(Path('resources/JiJiDownCore-win64.exe').resolve())
local_time = time.strftime("%y/%m/%d", time.localtime())
brower = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

base_url = "http://127.0.0.1:64000"  # 默认端口
local_dir = str(Path.cwd())  # 默认下载地址
appdata = os.getenv('APPDATA')  # 获取系统变量
channel = grpc.insecure_channel(base_url)#启动grpc
metadata = [('client_sdk','JiJiDownPython/1.0.0')]#设置sdk
Path(local_dir+'/resources').mkdir(parents=True,exist_ok=True)  # 创建核心文件夹
Path(local_dir+'/temp').mkdir(parents=True,exist_ok=True)# 创建临时文件夹
Path(appdata+'/JiJiDown').mkdir(parents=True,exist_ok=True)# 创建jijidown配置文件夹


#检查核心是否启动
def check() -> str:
    """
    检查核心是否启动
    """
    try:
        # cj = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
        response: dict = requests.get(url=base_url+"/jijidown/settings/get_download_dir", headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "origin": "https://space.bilibili.com"
        },timeout=5)
        if response.status_code == 200:
            return 'ok'
        return 'error'
    except:
        return 'error'

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

# 浏览器发送函数
def patch(url: str) -> dict:
    """
    发送patch信息
    """
    response = brower.patch(url=url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "origin": "https://space.bilibili.com"
    }).json()
    return response

def delete(url: str) -> dict:
    """
    发送patch信息
    """
    response = brower.delete(url=url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "origin": "https://space.bilibili.com"
    }).json()
    return response
############################################################ User层

# 获取登录状态
def get_user_info() -> dict:
    """
    获取用户登陆状态
    如果未登录 code = bool False
    mid = int 用户mid
    is_login = bool 登陆状态
    uname = str 用户名
    face = str 用户头像url
    vip_status = bool 大会员登陆状态
    vip_label_text = str 大会员状态
    """
    #data: dict = get(base_url+'/bili/user/get_user_info')
    with user_pb2_grpc.UserStub(channel) as stub:
        try:
            response = stub.Info(user_pb2.UserInfoReply(),metadata=metadata)
        except:
            return {'code': False}# 返回状态
    mid: int = response.mid  # 用户mid
    is_login: bool = response.is_login  # 登录状态
    uname: str = response.uname  # 用户名
    face: bytes = response.face  # 保存用户头像(二进制png的图片)
    vip_status: bool = response.vip_status  # 大会员登录状态
    vip_label_text: str = response.vip_label_text  # 大会员状态（年度大会员等）
    return {'code': True, 'mid': mid, 'is_login': is_login, 'uname': uname, 'face': face, 'vip_status': vip_status, 'vip_label_text': vip_label_text}

# 获取登录二维码
def get_login_status(api:int) -> dict:
    """
    api为登录接口
    0为WEB
    1为TV
    获取登录二维码
    code = 0为已登录
    返回{'code','image','id'}
    """

    #data = get(base_url+'/bili/user/tv/get_login_status')
    with user_pb2_grpc.UserStub(channel) as stub:
        try:
            response = stub.Info(user_pb2.UserLoginQRCodeReq(api=0),metadata=metadata)
        except:#已登录
            return {'code': 0}
    login_image:bytes = response.qr_code  # 登录用二维码(二进制png)
    return {'code': 1,'image':login_image,'id':response.id}

# 获取二维码扫码状态
def get_qr_status(id:str):
    """
    id为get_login_status返回的id
    login_successful:bool 登录是否成功
    // 未知
    LoginStatus_UNKNOWN = 0;
    // 登录成功
    LoginStatus_SUCCEEDED = 1;
    // 二维码已失效
    LoginStatus_EXPIRED = 2;
    // 未扫码
    LoginStatus_UNSCANNED = 3;
    // 二维码已扫码未确认
    LoginStatus_UNCONFIRMED = 4;
    """
    with user_pb2_grpc.UserStub(channel) as stub:
        response = stub.LoginStatus(user_pb2.UserLoginStatusReq(id=id),metadata=metadata)
        

############################################################ Jiji层

# 获取服务器sha265
def get_sha265() -> dict:
    """
    获取最新的服务器上存储的sha265
    """
    cloud_hash = brower.get('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-hash.txt').text#获取云端最新核心信息
    cloud_hash = cloud_hash.split()
    fin = []
    for a in cloud_hash:
        a = a.split('|')
        fin.append(a)
    return fin

# 检查是否存在核心
def find_core():
    dir_path = Path('resources/').iterdir()
    fin = []
    for i in dir_path:
        fin.append(i.name)
    return fin

# 下载最新版本
def down_core(system_type:str,system_bit:str) -> str:
    """
    自动匹配平台下载核心
    返回下载的核心文件名
    """
    if system_type == 'Windows':#如果平台为windows
        if system_bit == 'AMD64':#如果系统位数为64
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-win64.exe',out=str(Path('resources/')))
            return core_name
        elif system_bit == 'x86':
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-win32.exe',out=str(Path('resources/')))
            return core_name
        elif system_bit == 'i386':
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-win32.exe',out=str(Path('resources/')))
            return core_name
    elif system_type == 'Linux':
        if system_bit == 'AMD64':#如果系统为x86平台
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-linux-amd64',out=str(Path('resources/')))
            return core_name
        elif system_bit == 'aarch64':
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-linux-arm64',out=str(Path('resources/')))
        #如果均不匹配下载amd64版本
        core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-linux-amd64',out=str(Path('resources/')))
        return core_name
    elif system_type == 'darwin':
        if system_bit == 'amd64':#如果系统位数为64
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-darwin-amd64',out=str(Path('resources/')))
            return core_name
        elif system_bit == 'arm64':
            core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-darwin-arm64',out=str(Path('resources/')))
        #如果均不匹配下载amd64版本
        core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/JiJiDownCore-darwin-amd64',out=str(Path('resources/')))
        return core_name
    return 'error'

# 更新核心
def update_core(system_type:str,system_bit:str) -> str:
    """
    核心更新函数
    """
    global local_core#使用全局变量

    local_core_list = find_core()#获取本地文件夹列表
    b = []
    for a in local_core_list:#查询本地核心是否存在
        if 'JiJiDownCore-' in a :
            b.append(a)
    if len(b) > 1:#如果存在多于一个的核心
        for a in b:#全部删除
            Path.unlink(Path('resources/'+a))
    elif len(b) == 1:#如果只有一个，设置本地核心路径为那一个
        local_core = Path('resources/'+b[0])
    if Path(local_core).exists():#如果只有一个
        with open(local_core,'rb') as f:#获取本地核心sha265
            sha265 = hashlib.sha256(f.read()).hexdigest()
        cloud_sha265 = get_sha265()#获取云端sha265
        for a in cloud_sha265:#对比sha265
            if a[0] == sha265:
                return '目前是最新版本'
        for a in cloud_sha265:#sha265不匹配就查找相同名称的最新核心进行替换
            if a[-1] == str(Path(local_core).name):
                Path.unlink(local_core)#删除旧核心
                core_name = wget.download('https://101.34.172.63/PC/ReWPF/core/'+str(Path(local_core).name),out=str(Path('resources/')))
                return core_name+'已更新完成'
    else:#如果没有核心
        return_data = down_core(system_type,system_bit)#按平台下载核心
        return return_data+'自动下载完成'

# 生成配置文件
def make_yaml():
    if not Path(appdata+'/JiJiDown/config.yaml').exists():
        with open(str(Path(appdata+'/JiJiDown/config.yaml')),'w') as f:#写入设置文件
            f.write("""portable: false
log-level: debug
external-controller: 127.0.0.1:64000
external-ui: ""
secret: ""
user-info:
    raw-access-token: ""
    raw-cookies: ""
    hide-nickname: false
download-task:
    temp-dir: ""
    download-dir: """+local_dir+"""
    ffmpeg-path: ""
    max-task: 2
    download-speed-limit: 1
    disable-mcdn: false
jdm:
    max-retry: 0
    retry-wait: 0
    jdm-task-workers: 0
    session-workers: 0
    min-split-size: 0
    proxy-addr: ""
    check-best-mirror: false
    cache-in-ram: false
    cache-in-ram-limit: 0
    insecure-skip-verify: false
    certs-file-path: ""
""")

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
def quality(av:int, cid:int) -> dict:
    """
    获取视频清晰度
    av 为视频AV号 cid 为分P的id
    """
    # 获取指定分P清晰度
    one_video_info = get(base_url+'/bili/1/'+str(av) +'/'+str(cid)+'/get_video_quality')
    one_video_info = one_video_info['data']['list']

    new_video_info = {}  # 新建分辨率排序
    new_video_info['audio'] = {}
    new_video_info['video'] = {}
    new_video_info['audio']['WEB'] = []
    new_video_info['audio']['TV'] = []
    new_video_info['audio']['APP'] = []
    new_video_info['video']['WEB'] = []
    new_video_info['video']['TV'] = []
    new_video_info['video']['APP'] = []

    for quality in one_video_info:  # 分类
        quality = code(quality)
        if quality["api_type"] == 0:
            if quality["is_audio"] == True:
                new_video_info['audio']['WEB'].append(quality)
                continue
            if quality["is_video"] == True:
                new_video_info['video']['WEB'].append(quality)
                continue

        if quality["api_type"] == 1:
            if quality["is_audio"] == True:
                new_video_info['audio']['TV'].append(quality)
                continue
            if quality["is_video"] == True:
                new_video_info['video']['TV'].append(quality)
                continue

        if quality["api_type"] == 2:
            if quality["is_audio"] == True:
                new_video_info['audio']['APP'].append(quality)
                continue
            if quality["is_video"] == True:
                new_video_info['video']['APP'].append(quality)
                continue

    # 排序
    new_video_info['audio']['WEB'] = dic(new_video_info['audio']['WEB'])
    new_video_info['video']['WEB'] = dic(new_video_info['video']['WEB'])
    new_video_info['audio']['TV'] = dic(new_video_info['audio']['TV'])
    new_video_info['video']['TV'] = dic(new_video_info['video']['TV'])
    new_video_info['audio']['APP'] = dic(new_video_info['audio']['APP'])
    new_video_info['video']['APP'] = dic(new_video_info['video']['APP'])

    return new_video_info

################################################################## 任务管理层

#创建下载任务
def post_new_task(avid:int,cid:int,video_quality_data:dict,audio_quality_data:dict,video_filename:str) -> dict:
    """
    video_quality为1000时使用默认最高分辨率下载
    以下参数仅在video_quality不等于1000时生效
    api_type 指示使用的下载接口,在1000时默认走WEB接口

    UseAV = true  使用B站AV号处理
    UseAV = false 不使用B站AV号处理

    """
    video_quality = video_quality_data['quality']
    audio_quality = audio_quality_data['quality']
    if video_quality != 1000:
        api_type = video_quality_data['api_type']
        video_codecs = video_quality_data['codec']
        json={
                "avid": avid,
                "cid": cid,
                "video_quality": video_quality,
                "audio_quality": audio_quality,
                "api_type": api_type,
                "useav": True,
                "useflv": False,
                "video_codecs": video_codecs,
                "video_filename": video_filename
            }
    else:
        json={
            "avid": avid,
            "cid": cid,
            "video_quality": 1000,
            "useav": True,
            "useflv": False,
            "video_codecs": 1,#TODO 这里以后增加选择项，默认使用什么编码
            "video_filename": video_filename
            }
    data = post(base_url+'/task/post_new_task',json)
    download_danmaku(avid,cid,video_filename)#下载弹幕
    return data

#下载弹幕
def download_danmaku(avid:int,cid:int,video_filename:str):
    return_data = get(base_url+'/danmaku/'+avid+'/'+cid+'/download_danmaku?file='+video_filename)

#获取下载任务进度
def get_task_status(control_name:str):
    return_data = get(base_url+'/task/'+control_name+'/get_task_status')
    return return_data['data']

#暂停任务
def patch_pause_task(control_name:str):
    return_data = patch(base_url+'/task/'+control_name+'/patch_pause_task')

#继续任务
def patch_resume_task(control_name:str):
    return_data = patch(base_url+'/task/'+control_name+'/patch_resume_task')

#删除任务和文件
def delete_task(control_name:str):
    return_data = patch(base_url+'/task/'+control_name+'/delete_task_and_file')

#读取json中的下载列表
def load_json() -> dict:
    """
    读取配置参数
    """
    if os.path.exists('set.json'):
        with open('set.json','r') as f:
            return_data = json.loads(f.read())
    else:
        data = {}
        data['need_down_list'] = []
        data['fin_down_list'] = []
        with open('set.json','w') as f:
            f.write(json.dumps(data))
        return_data = data
    return return_data

#写入下载列表
def save_json(data:dict) -> None:
    """
    读取配置参数
    """
    with open('set.json','w') as f:
        f.write(json.dumps(data))
    return