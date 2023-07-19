import re
import os
import sys
import time
import subprocess
import threading #多进程库
from pathlib import Path #路径库
import platform#获取系统信息

import grpc
from loguru import logger#日志库
import requests
import pywebio as io
out = io.output
ioin = io.input
pin = io.pin

import core #导入python核心接口

from grpc_core import task_pb2
from grpc_core import task_pb2_grpc
######TODO 防止核心和前端任务不同步，暂时删除下载列表保存功能
data = {}
data['need_down_list'] = []
data['fin_down_list'] = []
#获取当前平台
system_type = platform.system()#系统名称
system_bit = platform.machine()#操作系统位数
#启动时间
local_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
#设置窗口标题
os.system('title Jithon 3.0 Beta')

#挂载核心
def start_core():
    """
    挂载核心
    """
    while 1==1:
        logger.info("核心已启动")
        #os.popen('taskkill /f /t /im "JiJiDownCore-win64.exe"')#关闭核心
        log_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        if system_type == 'Windows':#如果平台为windows
            exe_path = str(Path('resources/JiJiDownCore-win64.exe').resolve())
        elif system_type == 'Linux':
            if system_bit == 'AMD64':#如果系统为x86平台
                exe_path = str(Path('resources/JiJiDownCore-linux-amd64').resolve())
            elif system_bit == 'aarch64':#如果系统为x86平台
                exe_path = str(Path('resources/JiJiDownCore-linux-arm64').resolve())
        log_path = str(Path('temp/log_'+log_time+'.log').resolve())
        #os.chdir(str(Path('resources').resolve()))
        #input(exe_path)
        with open(log_path,'w+',encoding='UTF-8') as f:
            subprocess.run(exe_path,shell=True,stdout=f,text=True,cwd=str(Path('resources').resolve()))#启动核心且设置工作目录为resources
        logger.error('核心关闭,尝试重启,检查异常信息') # log
        with open(log_path,'r',encoding='UTF-8') as f:
            return_data = f.read()
            error = 0
            if 'nice try' in return_data:
                logger.warning('系统时间错误,请手动校正时间')
            if 'External controller gRPC listen error' in return_data:
                logger.warning('核心gRPC端口被占用(localhost:64000)')
                error = 1
            if 'External controller listen error' in return_data:
                logger.warning('核心RESTful端口被占用(localhost:64001)')
                error = 1
            if error == 1:#端口被占用
                logger.info('尝试修复端口占用问题')
                if system_type == 'Windows':#如果平台为windows
                    os.popen('taskkill /f /t /im "JiJiDownCore-win64.exe"')#关闭核心
                logger.info('修复完成,尝试重启核心')
            time.sleep(5)
            continue

#检查下载路径
def check_dir():
    """
    检查下载路径
    """
    new_dir = pin.pin['change_dir']
    if os.path.exists(new_dir):
        core.change_down_dir(new_dir)#修改路径
        out.toast('修改成功',color='success',duration='0')#弹出错误弹窗
        return
    out.toast('路径无效',color='error',duration='0')#弹出错误弹窗
    return

#校验输入是否正确
def check_input_url(url):
    #判断输入url类型
    if "BV" in url:
        video_info = re.findall('BV(..........)',url)[0]
        return
    elif "av" in url:
        video_info = re.findall('av(\d*)',url)[0]
        return
    elif "b23.tv" in url:
        url = re.findall('(https://b23.tv/.......)',url)[0]
        video_info = requests.get(url,allow_redirects=False).text#转换为网页版链接
        check_input_url(video_info)#重新检查
    elif "ep" in url:
        video_info = re.findall('ep(\d*)',url)[0]
        return
    elif "ss" in url:
        video_info = re.findall('ss(\d*)',url)[0]
        return
    elif "media/md" in url:#https://www.bilibili.com/bangumi/media/md28234644
        video_info = re.findall('md(\d*)',url)[0]
        return
    elif "space.bilibili.com" in url:#https://space.bilibili.com/1118188465
        video_info = re.findall('space.bilibili.com/(\d*)',url)[0]
        return
    #收藏夹处理
    elif "favlist?fid=" in url:#https://space.bilibili.com/1118188465/favlist?fid=1228786865
        video_info = re.findall('fid=(\d*)',url)[0]
        return
    #up主合集处理
    elif "?sid=" in url:#https://space.bilibili.com/1118188465/channel/collectiondetail?sid=28413
        video_info = re.findall('?sid=(\d*)',url)[0]
        return
    return '链接无效'

#检查任务状态类型
def get_task_status(data:int) -> str:
    """
    从代码查找对应的任务状态
    """
    if data == 0:
        return '错误'
    if data == 1:
        return '暂停'
    if data == 2:
        return '运行中'
    if data == 3:
        return '等待'
    if data == 4:
        return '正在进行合并'
    if data == 5:
        return '正在提取MP3'
    if data == 6:
        return '完成'

#获取被勾选视频数据
def get_video_list_info(num:int) -> list:
    """
    获取被勾选的视频数据
    """
    info_list = []
    for checkbox_one in range(1,num+1):
        if len(pin.pin['check_'+str(checkbox_one)]) != 0:#判断是否勾选了至少一个
            info_list.append(pin.pin['check_'+str(checkbox_one)][0])
    return info_list

#获取选择的清晰度
def get_choice_quality() -> dict:
    """
    获取选择的视频清晰度
    返回值为{'video','audio'}
    """
    return_dict = {}
    return_dict['video'] = pin.pin['select_video']
    return_dict['audio'] = pin.pin['select_audio']
    return return_dict

#创建清晰度列表
def get_video_quality_list(data:dict) -> list:
    """
    返回[视频清晰度,音频清晰度]
    """
    out_audio_list = []
    out_video_list = []
    out_audio_list.append({'label':'默认最高音质','value':{'quality_id':30280,'codec':'AAC'}})#默认选中
    out_video_list.append({'label':'默认最高画质','value':{'quality_id':0,'codec':2,'api_type':0,'codec_text':'H265'}})#默认选中
    for type in ['WEB','TV','APP']:#遍历不同接口
        for one_info in data['audio'][type]:#处理返回数据
            label = type+' '+one_info['quality_text']+' - ['+one_info['codec']+']   '+one_info['bit_rate']+'   '+one_info['stream_size']#选项标签
            value = one_info#选项值
            return_dict = {'label':label,'value':value}
            out_audio_list.append(return_dict)
        for one_info in data['video'][type]:#处理返回数据
            label = type+' '+one_info['quality_text']+' - ['+one_info['codec_text']+']   '+one_info['bit_rate']+'   '+one_info['stream_size']#选项标签
            if type == 'WEB':
                one_info['api_type'] = 0
            elif type == 'TV':
                one_info['api_type'] = 1
            elif type == 'APP':
                one_info['api_type'] = 2
            value = one_info#选项值
            return_dict = {'label':label,'value':value}
            out_video_list.append(return_dict)
    return [out_video_list,out_audio_list]

#处理下载文件名
def make_down_name(info_date:dict,video_data:dict) -> str:
    """
    下载文件名处理
    预留接口
    """
    info_date['title'] = re.sub(r'[\/:*?"<>|]', "_", info_date['title'])
    return info_date['title']

#显示视频下载选择界面
def print_video_info(info) -> list:
    """
    创建视频下载界面
    返回[视频信息,需下载视频列表,清晰度]
    """
    def enchange(list):#rpc对象转json对象
        return_all_list = []
        for one in list:
            return_list = {}
            return_list['avid'] = one.page_av
            return_list['bvid'] = one.page_bv
            return_list['cid'] = one.page_cid
            return_list['index'] = one.page_index
            return_list['info'] = one.page_info
            return_list['title'] = one.page_title
            return_all_list.append(return_list)
        return return_all_list

    with out.use_scope('video_info'):#进入视频信息域
        data = info
        with out.use_scope('up_info'):#切换到up信息域
            face = data['up_face']#缓存图片
            out.put_row([
                    None,
                    out.put_image(face,height='50px').style('margin-top: 1rem;margin-bottom: 1rem;border:1px solid;border-radius:50%;box-shadow: 5px 5px 5px #A9A9A9'),
                    None,
                    out.put_column([
                        None,
                        out.put_text(data['up_name']).style('font-size:1.25em;line-height: 0'),
                        ],size='1fr 1fr'),
                    None
                ],size='1fr 50px 25px auto 1fr').style('border: 1px solid #e9ecef;border-radius: .25rem')#限制up头像大小
        info_title = out.put_text(data['video_title']).style('border: 1px solid #e9ecef;border-radius: .25rem;font-size:2em;font-weight:bold;text-align:center')#视频标题
        if data['video_cover'] != '':
            cover = data['video_cover']#缓存图片
            info_cover = out.put_image(cover).style('border-radius: 30px;box-shadow: 15px 15px 30px #bebebe,-15px -15px 30px #ffffff;')#视频封面
        info_desc = out.put_text(data['video_desc']).style('border: 1px solid #e9ecef;border-radius: .25rem')#视频简介
        info_two = out.put_column([
            None,
            out.put_text('类型   '+str(data['sort'])+'-'+str(data['sub_sort'])).style('text-align:center'),
            None,
            out.put_text('发布时间   '+data['bili_pubdate_str']).style('text-align:center;line-height:0.5'),
            None
            ],size='0.5em auto 0.5em auto 0.5em').style('border: 1px solid #e9ecef;border-radius: .25rem')
        if data['video_cover'] != '':
            out.put_column([info_title,None,info_cover,None,info_desc,None,info_two],size='auto 1em auto 2em auto 1em auto').style('margin-top: 0.5rem;margin-bottom: 0.5rem')#设置为垂直排布
        else:
            out.put_column([info_title,None,info_desc,None,info_two],size='auto 10px auto 10px auto').style('margin-top: 0.5rem;margin-bottom: 0.5rem')#设置为垂直排布
            
        #创建清晰度选择
        get_video_quality_info = get_video_quality_list(core.quality(bvid=data['block'][0].list[0].page_bv,cid=data['block'][0].list[0].page_cid))#读取视频列表第一个的清晰度
        with out.use_scope('quality'):#创建清晰度选择域
            out.put_column([
                pin.put_select(name='select_video',options=get_video_quality_info[0],value={'quality_id':1000,'codec':2,'api_type':2}),#创建视频选择
                pin.put_select(name='select_audio',options=get_video_quality_info[1],value={'quality_id':30280})#创建音频选择
            ])
        #创建列表
        table_list = []
        num = 0
        table_list.append(['选择','标题'])
        for one in data['list']:#遍历列表
            num += 1
            list_one = []
            need_data = {'bvid':one.page_bv,'cid':one.page_cid,'title':one.page_title,'info':[one.page_info[0],one.page_info[1]]}#把rpc数据json化
            list_one.append(pin.put_checkbox(name='check_'+str(num),options=[{'label':num,'value':need_data}]).style('line-height:0.5'))#创建单选框
            list_one.append(out.put_text(one.page_title).style('width:100%'))#标题
            table_list.append(list_one)
        out.put_table(table_list,position=-1)
        
        #移除加载提示
        out.clear('load')
        out.remove('load')
        #使页面滚动到分辨率选择置顶
        out.scroll_to('quality','top')
        #创建下载控制组件
        control_buttom = ioin.actions(buttons=[{'label':'开始下载','value':'0'},{'label':'下载全部','value':'1'},{'label':'退出界面','value':'2','color':'danger'}])#创建按键
        need_quality:dict = get_choice_quality()#获取选择的清晰度
        if control_buttom == '0':#如果选择下载被勾选部分
            need_video_list:list = get_video_list_info(len(data['list']))#获取被勾选的视频列表
            logger.debug('有 '+str(len(need_video_list))+'/'+str(len(data['list']))+' 个视频被勾选') # log
        elif control_buttom == '1':#如果选择下载全部
            logger.debug('所有视频被选中') # log
            need_video_list:list = data['list']
            need_video_list = enchange(need_video_list)
        elif control_buttom == '2':#如果选择退出
            logger.debug('选择退出') # log
            return 'out'
        if len(need_video_list) == 0:#如果未选择任何视频
            logger.debug('未选择任何视频') # log
            out.toast('未选择任何视频',color='info',duration='0')#弹出错误弹窗
            return 'out'
    return [data,need_video_list,need_quality]

#监视下载任务进程
def watch_status(task_id:str,name:str):
    def del_task():
        core.delete_task(task_id)#向核心发送删除任务消息
        out.remove(task_id)
        return
    def resume_task():
        core.patch_resume_task(task_id)#继续任务
        watch_status(task_id=task_id,name=name)
    #连接到核心
    try:
        stub = task_pb2_grpc.TaskStub(core.channel)
        response = stub.Status(task_pb2.TaskStatusReq(task_id=task_id),metadata=core.metadata)
        logger.info(name+' 加入任务监视阵列')# log
        #with out.use_scope('down_work'):#进入downwork建立显示区域
            #out.put_scope(task_id)# 定义域
        need_print = out.put_row([
            None,
            out.put_column([
                None,
                out.put_text(name).style('text-align:left;font-size:1em;max-height:3em'),#TODO 创建标题
                out.put_scope('sta_text_'+task_id).style('text-align:center;font-size:0.875em;max-height:2em'),#创建用于进度提示的域,控制值为'sta_text_'+list_one['control_name']
                out.put_processbar('bar_'+task_id,init=0).style('width:100%;height=1em'),#下载列表,控制值为list_one['control_name']
                ],size='0.5fr 1fr 1fr 1fr 0.5fr'),
            out.put_column([
                None,
                out.put_scope('sta_worktype_'+task_id),
                None
            ],size='1fr auto 1fr').style('height=100%'),#创建用于显示任务状态的域,控制值为'sta_worktype_'+list_one['control_name']
            out.put_column([
                None,
                out.put_button('暂停',onclick=lambda:core.patch_pause_task(task_id),color='warning').style('margin-left: auto;margin-right: auto'),#暂停按钮
                out.put_button('继续',onclick=lambda:resume_task(),color='success'),#继续按钮
                out.put_button('删除',onclick=lambda:del_task(),color='danger'),
                None
            ])#删除按钮
            ],size='10px 80% 10% 10%').style('border: 1px solid #ccc')# 创建显示

        with out.use_scope('down_work'):
            with out.use_scope(task_id,clear=True):
                out.put_scope('bar_'+task_id,need_print)#写入初始标题及进度条
                for sec_print in response:
                    try:#监视流
                        out.set_processbar('bar_'+task_id,value= sec_print.progress / 100)#刷新进度条状态
                        with out.use_scope('sta_text_'+task_id,clear=True):#进入用于进度提示的域并清空
                            out.put_text(sec_print.text)#显示进度提示文本
                        with out.use_scope('sta_worktype_'+task_id,clear=True):#进入用于显示任务状态提示文本的域并清空
                            out.put_column([
                                out.put_text(get_task_status(int(sec_print.task_status))).style('text-align:center;font-size:0.5em'),
                                None,
                                out.put_text(sec_print.average_speed).style('text-align:center;font-size:0.5em'),#显示任务状态提示文本
                            ],size='auto auto auto auto auto')
                        if sec_print.task_status == 6:#任务完成
                            logger.success(name+' 下载完成')# log
                            return

                    except Exception as e:#如果核心突然断联
                        if e.details() == "Stream removed":#流终止
                            logger.error('线程出现致命错误 '+e.details())
                            time.sleep(1)
                            continue#试图重试
    except Exception as e:
        logger.error('线程出现错误,无法获取下载进度')
        #time.sleep(1)
        #watch_status(task_id=task_id,name=name)#试图重试

#解析输入的url
def start_url():
    url = pin.pin['url_input']#获取输入
    check_return = check_input_url(url)
    if check_return != None:
        out.toast(check_return,duration=3,color='error')#显示错误信息
        return
    #清除旧显示内容
    out.clear('video_info')
    out.clear('posting')#任务发送进度条
    with out.use_scope('main'):
    #显示加载提示
        with out.use_scope('load'):
            out.put_row([
                out.put_loading(),
                None,
                out.put_text('解析中'),
                ],size='1fr 20px 1fr')

        #解析url
        get_video_info = core.info(url)
        out.remove('load')#移除加载提示
        if get_video_info['error']:#出现权限问题
            logger.warning('解析失败')
            out.toast('解析失败',duration=3,position='center',color='warn')
            out.remove('posting')
            out.clear('video_info')#清空video_info域
            return
        return_data = print_video_info(get_video_info)#显示视频信息,返回视频信息
        if return_data == 'out':#如果选择退出界面或未勾选任何视频
            out.remove('posting')
            out.clear('video_info')#清空video_info域
            return
        #开始下载任务
        video_data = return_data[2]['video']
        audio_data = return_data[2]['audio']
        #滚动到最底下
        out.scroll_to('main','buttom')
        with out.use_scope('posting'):
            out.put_column([
                out.put_text('任务发送中').style('line-height: 0.5'),
                out.put_processbar('loading',init=0)#设置进度条
            ]).style('border: 1px solid #e9ecef;border-radius: .25rem')
            num = 0
            for need_video in return_data[1]:
                return_down_data:dict = core.post_new_task(bvid=need_video['bvid'],cid=need_video['cid'],video_quality=video_data['quality_id'],audio_quality=audio_data['quality_id'],api_type=video_data['api_type'],video_codec=video_data['codec'],save_filename=make_down_name(need_video,return_data[2]))
                #set_info['need_down_list'].append({'task_id':return_down_data['task_id'],'video_info':need_video})#添加控制字节段至下载列表
                #core.save_json(set_info)#刷新设置里的下载列表
                num += 1
                out.set_processbar('loading',num / len(return_data[1]))#设置进度条进度
                #建立下载任务监视线程
                start_watch_status = threading.Thread(target=watch_status,args=(return_down_data['task_id'],need_video['title'],))
                io.session.register_thread(start_watch_status)
                start_watch_status.start()#启动监视进程
                #写入下载列表
                data['need_down_list'].append([return_down_data['task_id'],need_video['title']])

            out.clear('loading')
            out.put_text('任务发送完成')
        out.remove('posting')
    return

#主函数
@logger.catch
def main():#主函数
    try:
        logger.info('网页服务器启动')
        if not start_jiji_core.is_alive():
            io.session.register_thread(start_jiji_core)
            logger.info('启动核心')
            start_jiji_core.start()
        with out.use_scope('main'):#创建并进入main域
            out.scroll_to('main','top')
            #等待核心响应提示
            with out.use_scope('load'):
                out.put_row([
                    None,
                    out.put_loading(color='primary').style('width:4rem; height:4rem;padding: 15px 0'),
                    None,
                    out.put_column([
                            None,
                            out.put_text('等待核心响应,请检查核心是否启动').style('line-height: 0'),
                        ],size='1fr 1fr'),
                    None
                ],size='1fr auto 20px auto 1fr')
            #检查登录
            while 1==1:
                user_info = core.get_user_info()
                if user_info['code'] != -1:#服务器启动失败
                    break
                logger.debug('核心启动失败,重试')
                time.sleep(1)
            #获取操作系统
            system_info = core.status_ping()
            logger.info('当前服务器名称 '+system_info['server_name']) # log
            logger.info('当前操作系统名称 '+system_info['os_system_name']) # log
            out.clear('load')#清空加载界面
            out.remove('load')#删除加载界面
            #初始化
            out.scroll_to('main','top')
            out.clear('main')
            if user_info['code'] == 0:#如果已登录
                with out.use_scope('user_info'):#切换到用户信息域
                    logger.debug('核心已连接') # log
                    face = user_info['face']#缓存图片
                    put_user = '当前登录用户: '+user_info['uname']
                    if user_info['vip_label_text'] != '':
                        put_user += ' ['+user_info['vip_label_text']+']'
                    if user_info['badge'] != '':
                        put_user += ' ['+user_info['badge']+']'
                    logger.debug(put_user) # log
                    out.put_row([
                        None,
                        out.put_image(face,height='50px').style('margin-top: 1rem;margin-bottom: 1rem;border:1px solid;border-radius:50%;box-shadow: 5px 5px 5px #A9A9A9'),
                        None,
                        out.put_column([
                            None,
                            out.put_text(put_user).style('font-size:1.25em;line-height: 0'),
                            ],size='1fr 1fr'),
                        None
                    ],size='1fr 50px 25px auto 1fr').style('border: 1px solid #e9ecef;border-radius: .25rem')#限制用户头像大小
            elif user_info['code'] == 1:
                logger.debug('核心已连接') # log
                #创建选择弹窗
                qr_type = ioin.actions('选择登录接口',[{'label':'WEB接口','value':0,'color':'primary','type':'submit'},{'label':'TV接口','value':1,'color':'primary','type':'submit'}],help_text='WEB接口仅支持WEB接口下载,TV接口支持全接口下载')
                return_data = core.get_login_status(qr_type)#获取二维码
                with out.use_scope('login'):
                    out.put_row([
                        None,
                        out.put_column([
                            None,
                            out.put_text('请扫描二维码登录').style('line-height: 1;text-align:center'),
                            None,
                            out.put_image(return_data['image'],width='50%').style('margin: auto'),
                        ],size='10px auto 10px auto'),
                        None
                    ],size='20px auto 20px').style('border: 1px solid #e9ecef;border-radius: .25rem;box-shadow: 5px 5px 5px #A9A9A9')
                    check_user_info = core.get_qr_status(id=return_data['id'])#循环检查是否扫描
                    if check_user_info == 1:#如果登录成功
                        out.clear('login')
                        out.remove('login')
                        return
                    elif check_user_info == 2:#如果二维码失效
                        logger.warning('二维码失效,1秒后重试') # log
                        time.sleep(1)
                        main()
                    elif check_user_info == 0:#如果出现未知错误
                        logger.warning('二维码出现未知错误,1秒后重试') # log
                        time.sleep(1)
                        main()
            #创建横向标签栏
            scope_url = out.put_scope('url')#创建url域
            scope_set = out.put_scope('set')#创建set域
            scope_down = out.put_scope('down')#创建down域
            out.put_tabs([{'title':'链接解析','content':scope_url},{'title':'下载列表','content':scope_down},{'title':'设置','content':scope_set}])#创建

            #创建url输入框
            with out.use_scope('url'):#进入域
                pin.put_input('url_input',label='请输入链接',type='text')#限制类型为url,使用check_input_url检查内容
                out.put_button(label='解析链接',onclick=start_url).style('width: 100%')#创建按键
                out.put_scope('video_info')
            
            #创建下载列表
            with out.use_scope('down'):
                scope_down_work = out.put_scope('down_work')
                scope_down_fin = out.put_scope('down_fin')
                out.put_tabs([{'title':'下载中','content':scope_down_work}])#创建横向标签栏

            #创建设置
            with out.use_scope('set'):#进入域
                out.put_text('由于下载地址接口未更新到新协议，暂时不提供实时修改方式')
                #out.put_row([out.put_text('目前下载地址：'),pin.put_input(name='change_dir',value=core.get_down_dir()),out.put_button('确认修改',onclick=check_dir)])


    #错误处理
    except AssertionError:#核心未工作
        out.toast('核心貌似没有启动,10秒后重试',position='center',color='error')
        logger.error('无法与核心通讯,10秒后重试')
        time.sleep(5)
        main()
    except grpc._channel._MultiThreadedRendezvous as e:
        if e.details() == "Stream removed":
            logger.warning('核心异常停止')
            time.sleep(1)
            main()

logger.info('自动更新核心')
core.update_core(system_type,system_bit)#更新核心
core.check_ffmpeg()#检查ffmpeg可用性
start_jiji_core = threading.Thread(target=start_core)#设置核心线程
io.config(title='Jithon 3.0 Beta',description='本应用为唧唧2.0基于python的webui实现',theme='yeti')
#logger.info('申请管理员权限')
#ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
logger.info('主程序启动,如未自动跳转请打开http://127.0.0.1:8080')
try:
    io.start_server(main,host='127.0.0.1',port=8080,debug=True,cdn=False,auto_open_webbrowser=True)
except KeyboardInterrupt:#程序被手动关闭
    logger.info('程序已终止')
    exit()