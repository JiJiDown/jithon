import os
import time
import subprocess
from pathlib import Path #路径库
import hashlib#sha256加密库

from loguru import logger#日志库

import requests
from tqdm import tqdm
import pywebio as io
out = io.output
ioin = io.input
pin = io.pin


import grpc

from grpc_core import user_pb2
from grpc_core import user_pb2_grpc
from grpc_core import task_pb2
from grpc_core import task_pb2_grpc
from grpc_core import status_pb2
from grpc_core import status_pb2_grpc
from grpc_core import bvideo_pb2
from grpc_core import bvideo_pb2_grpc

import google.protobuf.empty_pb2 as empty_pb2
# 初始化
local_core = str(Path('resources/JiJiDownCore-win64.exe').resolve())
local_time = time.strftime("%y/%m/%d", time.localtime())
brower = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

base_url = "localhost:64000"  # 默认端口
local_dir = str(Path.cwd())  # 默认下载地址
appdata = os.getenv('APPDATA')  # 获取系统变量
channel = grpc.insecure_channel(base_url)#启动grpc
logger.info('启动grpc,地址为{}',base_url)# log
metadata = [('client_sdk','JiJiDownPython/1.0.0')]#设置sdk
logger.info('设置SDK')# log
Path(local_dir+'/resources').mkdir(parents=True,exist_ok=True)  # 创建核心文件夹
Path(local_dir+'/temp').mkdir(parents=True,exist_ok=True)# 创建临时文件夹
Path(appdata+'/JiJiDown').mkdir(parents=True,exist_ok=True)# 创建jijidown配置文件夹
logger.info('设置路径')

#检查ffmpeg可用性
def check_ffmpeg():
    return_ff_list = find_core()
    for a in return_ff_list:
        if 'ffmpeg' in a:
            logger.info('ffmpeg存在') # log
            return
    logger.warning('未找到ffmpeg,下载的视频可能无法合成') # log
    logger.info('尝试下载ffmpeg')
    down_url = lanzou_api('https://wwwv.lanzouw.com/iluwh12vtnli','9zp2')['download']
    download(down_url,str(Path('resources/ffmpeg.exe')))
    check_ffmpeg()
    return

#下载文件
def download(url:str,out:str):
    """
    下载文件
    """
    #try:
    Path(local_dir+'/resources').mkdir(parents=True,exist_ok=True)  # 创建核心文件夹
    r = brower.get(url=url,stream=True,headers=headers)
    # 用流stream的方式获取url的数据
    # 拿到文件的长度，并把total初始化为0
    total = int(r.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(str(Path(out).resolve()), 'wb') as file, tqdm(
        desc='下载中',
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

#检查核心是否启动
def check() -> str:
    """
    检查服务是否正常
    """
    #try:
    stub = bvideo_pb2_grpc.BvideoStub(channel)
    response = stub.CheckContent(bvideo_pb2.BvideoContentReq(content='https://www.bilibili.com/video/av170001'),metadata=metadata)
    if response.is_valid:
        logger.debug('服务一切正常')
        return 'ok'
    else:
        return 'error'

#编码信息转索引
def code(keys):
    if keys['codec'] == 0:
        keys['codec_text'] = 'NONE'
    elif keys['codec'] == 1:
        keys['codec_text'] = 'H264'
    elif keys['codec'] == 2:
        keys['codec_text'] = 'H265'
    elif keys['codec'] == 3:
        keys['codec_text'] = 'AV1'
    elif keys['codec'] == 4:
        keys['codec_text'] = 'M4A'
    elif keys['codec'] == 5:
        keys['codec_text'] = 'DOLBY'
    return keys


#列表排序
def dic(info):
    new_list = []#创建临时列表
    for a in info:
        new_list.append(a["quality_id"])
    new_list.sort(reverse = True)#列表排序从大到小
    new_info = []
    for b in new_list:
        for c in info:
            if c["quality_id"] == b:
                new_info.append(c)
    return new_info

#强制关闭端口占用程序
def find_kill(ano:int):
    """
    查找并关闭占用端口的程序
    """
    return_data = subprocess.check_output('netstat -aon|findstr "'+str(ano)+'"',shell=True).decode('gbk').split()#获取信息,编码,分割成列表
    pid = return_data[-1]
    if pid.isnumeric():
        return_data = os.popen('taskkill /F /PID '+str(pid)+' /t')#获取进程PID并停止进程
        if '成功:' in return_data:
            logger.info('成功关闭占用 '+str(ano)+'端口的 PID'+str(pid)+'程序')
            return
        logger.warning('未成功关闭占用 '+str(ano)+'端口的 PID'+str(pid)+'程序')
    return

#蓝奏api
def lanzou_api(url:str,password:str):
    """
    蓝奏链接转直链
    """
    return_data = requests.get('https://www.yuanxiapi.cn/api/lanzou/?url='+url+'&pwd='+password,headers=headers).json()
    return return_data
############################################################ User层

# 获取登录状态
def get_user_info() -> dict:
    """
    获取用户登陆状态
    如果未登录 code = bool False
    mid = int 用户mid
    is_login = bool 登陆状态
    uname = str 用户名
    face = bytes 用户头像
    vip_status = bool 大会员登陆状态
    vip_label_text = str 大会员状态
    badge = str 头衔
    """
    #data: dict = get(base_url+'/bili/user/get_user_info')
    stub = user_pb2_grpc.UserStub(channel)
    logger.debug('尝试获取用户登录状态')# log
    try:
        response = stub.Info(user_pb2.UserInfoReply(),metadata=metadata)
    except grpc._channel._InactiveRpcError as e:#通讯失败
        if e.code().value[0] == 14:
            logger.warning('核心未启动')
            out.toast('无法连接核心,重试中',duration=3,position='center',color='warn')
            return {'code':-1}
        logger.debug('用户未登录')# log
        return {'code': 1}# 返回状态
    mid: int = response.mid  # 用户mid
    is_login: bool = response.is_login  # 登录状态
    uname: str = response.uname  # 用户名
    face: bytes = response.face  # 保存用户头像(二进制png的图片)
    vip_status: bool = response.vip_status  # 大会员登录状态
    vip_label_text: str = response.vip_label_text  # 大会员状态（年度大会员等）
    badge:str = response.badge  # 头衔
    return {'code': 0, 'mid': mid, 'is_login': is_login, 'uname': uname, 'face': face, 'vip_status': vip_status, 'vip_label_text': vip_label_text,'badge':badge}

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
    stub = user_pb2_grpc.UserStub(channel)
    try:
            response = stub.LoginQRCode(user_pb2.UserLoginQRCodeReq(api=api),metadata=metadata)
    except Exception as e:#已登录
            if e.code().value[0] == 14:#连接失败
                logger.warning('核心无响应')
            logger.debug('用户已登录')
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
    stub = user_pb2_grpc.UserStub(channel)
    logger.debug('获取扫码状态')
    response = stub.LoginStatus(user_pb2.UserLoginStatusReq(id=id),metadata=metadata)
    for one in response:#迭代器
            status = one.status#登录状态
            #TODO
            login_successful = one.login_successful#登录是否成功
            if login_successful or status == 1:#登陆成功
                return 1
            elif status == 2:#二维码失效
                return 2
            elif status == 0:#未知
                return 0

############################################################ Jiji层

# 获取服务器sha265
def get_sha265() -> dict:
    """
    获取最新的服务器上存储的sha265
    """
    logger.info('获取云端核心数据,检查更新')
    cloud_hash = brower.get('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-hash.txt').text#获取云端最新核心信息
    cloud_hash = cloud_hash.split()
    fin = []
    for a in cloud_hash:
        a = a.split('|')
        fin.append(a)
    return fin

# 检查是否存在核心
def find_core():
    dir_path = Path('resources/').resolve().iterdir()
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
    logger.info('未找到核心,尝试下载') # log
    if system_type == 'Windows':#如果平台为windows
        if system_bit == 'AMD64':#如果系统位数为64
            core_name = download('http://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-win64.exe',out=str(Path('resources/JiJiDownCore-win64.exe')))
            return core_name
        elif system_bit == 'x86':
            core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-win32.exe',out=str(Path('resources/JiJiDownCore-win32.exe')))
            return core_name
        elif system_bit == 'i386':
            core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-win32.exe',out=str(Path('resources/JiJiDownCore-win32.exe')))
            return core_name
    elif system_type == 'Linux':
        if system_bit == 'AMD64':#如果系统为x86平台
            core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-linux-amd64',out=str(Path('resources/JiJiDownCore-linux-amd64')))
            return core_name
        elif system_bit == 'aarch64':
            core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-linux-arm64',out=str(Path('resources/JiJiDownCore-linux-arm64')))
        #如果均不匹配下载amd64版本
        core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-linux-amd64',out=str(Path('resources/JiJiDownCore-linux-amd64')))
        return core_name
    elif system_type == 'darwin':
        if system_bit == 'amd64':#如果系统位数为64
            core_name =download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-darwin-amd64',out=str(Path('resources/JiJiDownCore-darwin-amd64')))
            return core_name
        elif system_bit == 'arm64':
            core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-darwin-arm64',out=str(Path('resources/JiJiDownCore-darwin-arm64')))
        #如果均不匹配下载amd64版本
        core_name = download('https://jj.xn--5nx14y.top/PC/ReWPF/core/JiJiDownCore-darwin-amd64',out=str(Path('resources/JiJiDownCore-darwin-amd64')))
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
                logger.info('核心目前是最新版本') # log
                return '目前是最新版本'
        for a in cloud_sha265:#sha265不匹配就查找相同名称的最新核心进行替换
            if a[-1] == str(Path(local_core).name):
                Path.unlink(local_core)#删除旧核心
                core_name = download('https://101.34.172.63/PC/ReWPF/core/'+str(Path(local_core).name),out=str(Path('resources/'+str(Path(local_core).name))))
                logger.info('核心更新完成')
                return core_name+'已更新完成'
    else:#如果没有核心
        return_data = down_core(system_type,system_bit)#按平台下载核心
        return '自动下载完成'

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
    #data = get(base_url+"/jijidown/settings/get_download_dir")
    data = data['data']
    return data['dir']

# 更改下载目录
def change_down_dir(down_dir: str):
    """
    修改下载目录
    """
    json = {'dir': down_dir}
    #post(base_url+'/jijidown/settings/set_download_dir', json)

def ad() -> dict:
    """
    获取ad
    title = str 标题
    url = str 链接
    img = str 图片内容，转成bit进行显示
    """
    #data = get(base_url+"/jijidown/ad")
    #return data['data']

################################################################### video info层

#获取视频信息
def info(url: str) -> dict:
    """
    获取视频信息
    bool error 是否出现错误
    msg 错误信息
    error_value 错误状态码
    error_name 错误类型

    // B站 URL 检测结果
    BLinkResult blink_result = 1;
    // 视频封面
    bytes video_cover = 2;
    // 视频标题
    string video_title = 3;
    // 视频文件名
    string video_filename = 4;
    // 描述
    string video_desc = 5;
    // 视频子类型
    string sub_sort = 6;
    // 视频类型
    string sort = 7;
    // UP主昵称
    string up_name = 9;
    // UP主 ID
    int64 up_mid = 10;
    // UP主头像
    bytes up_face = 11;
    // B站发布时间 番剧的字符串时间
    string bili_pubdate_str = 12;
    // 是否为互动视频
    bool is_stein_gate = 13;
    // 视频列表块
    repeated BvideoBlock block = 14;
    """
    #data = get(base_url+'/bili/'+str(type)+'/'+str(id)+'/get_video_info')
    stub = bvideo_pb2_grpc.BvideoStub(channel)
        #error code 10 ABORTED
    try:
        logger.debug('发送视频信息查询 {}',url)# log
        response = stub.Info(bvideo_pb2.BvideoContentReq(content=url),metadata=metadata)
        list = []
        for a in response.block:#遍历每一页的视频
            for b in a.list:
                if not b in list:
                    list.append(b)
        info_list = {
            'error':False,
            'blink_result':response.blink_result,
            'video_cover':response.video_cover,
            'video_title':response.video_title,
            'video_filename':response.video_filename,
            'video_desc':response.video_desc,
            'sub_sort':response.sub_sort,
            'sort':response.sort,
            'up_name':response.up_name,
            'up_mid':response.up_mid,
            'up_face':response.up_face,
            'bili_pubdate_str':response.bili_pubdate_str,
            'is_stein_gate':response.is_stein_gate,
            'block':response.block,
            'list':list
            }
    except grpc._channel._InactiveRpcError as e:
        code_name = e.code().name# 错误类型
        code_value = e.code().value
        if e.details() == "GetUpSpaceSeriesAndCollectionList It's a premium feature":#获取up视频列表和合集无权限
            logger.warning('无唧唧会员权限')
            logger.warning('无法获取UP视频列表和合集信息')
            out.toast('无唧唧会员权限,无法获取UP视频列表和合集信息',duration=3,position='center',color='warn')
        elif e.details() == "GetBangumiList function not allowed":
            logger.warning('无权限')
            logger.warning('不允许获取番剧信息')
            out.toast('不允许获取番剧信息',duration=3,position='center',color='warn')
        elif e.details() == "GetFavoriteList It's a premium feature":
            logger.warning('无唧唧会员权限')
            logger.warning('无法获取收藏夹信息')
            out.toast('无唧唧会员权限,无法获取收藏夹信息',duration=3,position='center',color='warn')
        elif e.code().value[0] == 14:#核心无响应
            logger.warning('核心无响应,重试中')
            out.toast('核心无响应,重试中',duration=3,position='center',color='warn')
            time.sleep(1)
            info(url)
        return {'error':True,'msg':e.details(),'error_value':code_value[0],'error_name':code_name}
    except Exception as e:#出现grpc异常
            code_name = e.code().name# 错误类型
            code_value = e.code().value
            logger.error('出现未定义错误 '+e.details())# log
            out.toast('出现未定义错误 '+e.details(),duration=3,position='center',color='warn')
            logger.error('错误类型 '+code_name)
            return {'error':True,'msg':e.details(),'error_value':code_value[0],'error_name':code_name}
    return info_list

################################################################## video quality层
def enchange(data,type):
    return_data = {}
    return_data['quality_id']:int = int(data.quality_id)
    return_data['quality_text']:str = data.quality_text
    if type == 0:
        return_data['codec']:str = data.codec
    else:
        return_data['codec']:str = data.codec_text
    if type == 0:
        return_data['frame_rate']:str = data.frame_rate
    return_data['bit_rate']:str = data.bit_rate
    return_data['stream_size']:str = data.stream_size
    return_data['api_type']:int = data.api_type
    return_data['error']:bool = False
    return_data['msg']:str = '成功'
    return_data['error_value']:int = 0
    return_data['error_name']:str = ''
    return return_data

# 获取分辨率
def quality(bvid:str, cid:int) -> dict:
    """
    获取视频清晰度
    av 为视频AV号 cid 为分P的id
    """
    # 获取指定分P清晰度
    #one_video_info = get(base_url+'/bili/1/'+str(av) +'/'+str(cid)+'/get_video_quality')

    new_video_info = {}  # 新建分辨率排序
    new_video_info['audio'] = {}
    new_video_info['video'] = {}
    new_video_info['audio']['WEB'] = []
    new_video_info['audio']['TV'] = []
    new_video_info['audio']['APP'] = []
    new_video_info['video']['WEB'] = []
    new_video_info['video']['TV'] = []
    new_video_info['video']['APP'] = []

    stub = bvideo_pb2_grpc.BvideoStub(channel)
    logger.debug('发送清晰度查询 bvid={} cid={}',bvid,cid)# log
    try:
        response = stub.AllQuality(bvideo_pb2.BvideoAllQualityReq(bvid=bvid,cid=cid),metadata=metadata)
    except grpc._channel._InactiveRpcError:#无权限
        logger.warning('无唧唧会员权限')
        logger.warning('无法获取分辨率列表')
        out.toast('无唧唧会员权限,无法获取分辨率列表',duration=3,position='center',color='warning')
        return new_video_info
    #except Exception as e:#出现grpc异常
        #code_name = e.code().name# 错误类型
        #code_value = e.code().value
        #logger.error('出现错误 '+e.details())# log
        #logger.error('错误类型 '+code_name)# log
        #return

    for quality in response.video:  # 视频分类
        quality = code(enchange(quality,type=0))
        if quality['api_type'] == 0:
            new_video_info['video']['WEB'].append(quality)
        elif quality['api_type'] == 1:
            new_video_info['video']['TV'].append(quality)
        elif quality['api_type'] == 2:
            new_video_info['video']['APP'].append(quality)
    for quality in response.audio:  # 音频分类
        quality = code(enchange(quality,type=1))
        if quality['api_type'] == 0:
            new_video_info['audio']['WEB'].append(quality)
            continue

        if quality['api_type'] == 1:
            new_video_info['audio']['TV'].append(quality)
            continue

        if quality['api_type'] == 2:
            new_video_info['audio']['APP'].append(quality)
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
def post_new_task(bvid:int,cid:int,video_quality:int,audio_quality:int,save_filename:str,video_codec:str='WEB',api_type:int=0,audio_only:bool=False) -> dict:
    """
    video_quality为1000时使用默认最高分辨率下载
    以下参数仅在video_quality不等于1000时生效
    api_type 指示使用的下载接口,在1000时默认走WEB接口

    返回 data['task_id']
    """
    stub = task_pb2_grpc.TaskStub(channel)
    #data = post(base_url+'/task/post_new_task',json)
    response = stub.New(task_pb2.TaskNewReq(bvid=bvid,cid=cid,video_quality=video_quality,audio_quality=audio_quality,video_codec=video_codec,api_type=api_type,save_filename=save_filename,audio_only=audio_only),metadata=metadata)
    data = {}
    data['task_id'] = response.task_id
    data['quality_video'] =response.quality_video
    data['quality_audio'] = response.quality_audio

    #download_danmaku(avid,cid,video_filename)#下载弹幕
    return data

#下载弹幕
def download_danmaku(avid:int,cid:int,video_filename:str):
    #return_data = get(base_url+'/danmaku/'+avid+'/'+cid+'/download_danmaku?file='+video_filename)
    pass

#暂停任务
def patch_pause_task(task_id:str):
    stub = task_pb2_grpc.TaskStub(channel)
    response = stub.Control(task_pb2.TaskControlReq(task_id=task_id,do=1),metadata=metadata)
    #return_data = patch(base_url+'/task/'+control_name+'/patch_pause_task')

#继续任务
def patch_resume_task(task_id:str):
    stub = task_pb2_grpc.TaskStub(channel)
    response = stub.Control(task_pb2.TaskControlReq(task_id=task_id,do=2),metadata=metadata)
    #return_data = patch(base_url+'/task/'+control_name+'/patch_resume_task')

#删除任务和文件
def delete_task(task_id:str):
    stub = task_pb2_grpc.TaskStub(channel)
    response = stub.Control(task_pb2.TaskControlReq(task_id=task_id,do=4),metadata=metadata)
    #return_data = patch(base_url+'/task/'+control_name+'/delete_task_and_file')

def status_ping():
    """
    检查操作系统
    server_name = 服务器名称
    os.icon = 服务器图标
    os_system_name = 操作系统名称
    """
    stub = status_pb2_grpc.StatusStub(channel)
    try:
        response = stub.Ping(empty_pb2.Empty(),metadata=metadata)
    except grpc._channel._InactiveRpcError as e:
        if e.code().value[0] == 14:
            return {'server_name':'null','os_icon':'null','os_system_name':'null'}
    return {'server_name':response.server_name,'os_icon':response.os_icon,'os_system_name':response.os_system_name}
