import re
import os
import time
import threading #多进程库
from pathlib import Path #路径库
import platform#获取系统信息

import requests
import pywebio as io
out = io.output
ioin = io.input
pin = io.pin

import core #导入python核心接口

######TODO 防止核心和前端任务不同步，暂时删除下载列表保存功能
data = {}
data['need_down_list'] = []
data['fin_down_list'] = []
core.save_json(data)
#声明下载列表
set_info = core.load_json()
#获取当前平台
system_type = platform.system()#系统名称
system_bit = platform.architecture()[0]#操作系统位数
#启动时间
local_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

#挂载核心
def start_core():
    """
    挂载核心
    """
    print("windows核心已启动")
    os.system('taskkill /f /t /im "JiJiDownCore-win64.exe"')#关闭核心
    core_out = os.popen(str(Path('resources/JiJiDownCore-win64.exe'))+'>>'+str(Path('resources/log_'+local_time+'.log')))#启动核心

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

#检查输入链接类型
def get_video_id(url) -> list:
    """
    检查输入链接类型
    输出为list [序号:int,id:str]
    """
    #判断输入url类型
    #手机端链接处理
    if "b23.tv" in url:
        url = re.findall('(https://b23.tv/.......)',url)[0]
        video_info = requests.get(url,allow_redirects=False).text#转换为网页版链接
        get_video_id(video_info)#重新检查
    #ep类型处理
    if "ep" in url:
        video_info = re.findall('ep(\d*)',url)[0]
        if video_info != '':
            return [3,video_info]
    #ss类型处理
    if "ss" in url:
        video_info = re.findall('ss(\d*)',url)[0]
        if video_info != '':
            return [4,video_info]
    #media类型处理
    if "media/md" in url:#https://www.bilibili.com/bangumi/media/md28234644
        video_info = re.findall('md(\d*)',url)[0]
        if video_info != '':
            return [5,video_info]
    #收藏夹处理
    if "favlist?fid=" in url:#https://space.bilibili.com/1118188465/favlist?fid=1228786865
        video_info = re.findall('fid.([0-9]*)',url)[0]
        if video_info != '':
            return [7,video_info]
    #up主合集处理
    if "?sid=" in url:#https://space.bilibili.com/1118188465/channel/collectiondetail?sid=28413
        video_info = re.findall('?sid=(\d*)',url)[0]
        if video_info != '':
            return [8,video_info]
    #up主投稿处理
    if "space.bilibili.com" in url:#https://space.bilibili.com/1118188465
        video_info = re.findall('space.bilibili.com/(\d*)',url)[0]
        if video_info != '':
            return [6,video_info]
    #BV解析
    if "BV" in url:
        video_info = re.findall('BV(..........)',url)[0]
        if video_info != '':
            return [2,video_info]
    #AV解析
    if "av" in url:
        video_info = re.findall('av(\d*)',url)[0]
        if video_info != '':
            return [1,video_info]
    return ''

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

#将下载完成的移动到完成任务列表中
def remove_fin_task(control_name:str):
    data = core.load_json()#读取配置
    for one in data['need_down_list']:#遍历正在进行的任务列表
        if control_name == one['control_name']:
            data['fin_down_list'].append(one)
            data['need_down_list'].remove(one)
            break
    core.save_json(data)
    return

#从任务列表中移除任务（暂时）TODO 未来实现自动恢复下载进度
def remove_task(control_name:str):
    data = core.load_json()#读取配置
    for one in data['need_down_list']:#遍历正在进行的任务列表
        if control_name == one['control_name']:
            core.delete_task(one['control_name'])#删除任务
            data['need_down_list'].remove(one)
            break
    core.save_json(data)
    return

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
    out_audio_list.append({'label':'默认最高音质','value':{'quality':30280}})#默认选中
    out_video_list.append({'label':'默认最高画质','value':{'quality':1000}})#默认选中
    for type in ['WEB','TV','APP']:#遍历不同接口
        for one_info in data['audio'][type]:#处理返回数据
            label = type+' '+one_info['quality_str']+' - ['+one_info['codec']+']   '+one_info['stream_size']#选项标签
            value = one_info#选项值
            return_dict = {'label':label,'value':value}
            out_audio_list.append(return_dict)
        for one_info in data['video'][type]:#处理返回数据
            label = type+' '+one_info['quality_str']+' - ['+one_info['codec']+']   '+one_info['stream_size']#选项标签
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
    return video_data['video_filename']

#显示视频下载选择界面
def print_video_info(info) -> list:
    """
    创建视频下载界面
    返回[视频信息,需下载视频列表,清晰度]
    """
    with out.use_scope('video_info'):#进入视频信息域
        data = info['data']
        with out.use_scope('up_info'):#切换到up信息域
            face = requests.get(data['up_face']).content#缓存图片
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
            cover = requests.get(data['video_cover']).content#缓存图片
            info_cover = out.put_image(cover).style('border-radius: 30px;box-shadow: 15px 15px 30px #bebebe,-15px -15px 30px #ffffff;')#视频封面
        info_desc = out.put_text(data['video_desc']).style('border: 1px solid #e9ecef;border-radius: .25rem')#视频简介
        info_two = out.put_column([
            None,
            out.put_text('视频类型   '+str(data['sort'])+'-'+str(data['sub_sort'])).style('text-align:center'),
            None,
            out.put_text('视频发布时间   '+data['bili_pubdate_str']).style('text-align:center;line-height:0.5'),
            None
            ],size='0.5em auto 0.5em auto 0.5em').style('border: 1px solid #e9ecef;border-radius: .25rem')
        if data['video_cover'] != '':
            out.put_column([info_title,None,info_cover,None,info_desc,None,info_two],size='auto 1em auto 2em auto 1em auto').style('margin-top: 0.5rem;margin-bottom: 0.5rem')#设置为垂直排布
        else:
            out.put_column([info_title,None,info_desc,None,info_two],size='auto 10px auto 10px auto').style('margin-top: 0.5rem;margin-bottom: 0.5rem')#设置为垂直排布
            
        #创建清晰度选择
        get_video_quality_info = get_video_quality_list(core.quality(data['list'][0]['page_av'],data['list'][0]['page_cid']))#读取视频列表第一个的清晰度
        with out.use_scope('quality'):#创建清晰度选择域
            out.put_column([
                pin.put_select(name='select_video',options=get_video_quality_info[0],value={'quality':1000}),#创建视频选择
                pin.put_select(name='select_audio',options=get_video_quality_info[1],value={'quality':30280})#创建音频选择
            ])
        #创建列表
        table_list = []
        num = 0
        table_list.append(['选择','标题'])
        for one in data['list']:#遍历列表
            num += 1
            list_one = []
            list_one.append(pin.put_checkbox(name='check_'+str(num),options=[{'label':str(num),'value':one}]).style('line-height:0.5'))#创建单选框
            list_one.append(out.put_text(one['page_name']).style('width:100%'))#标题
            table_list.append(list_one)
        out.put_table(table_list,position=-1).style('width:100%')
        
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
        elif control_buttom == '1':#如果选择下载全部
            need_video_list:list = data['list']
        elif control_buttom == '2':#如果选择退出
            return 'out'
        if len(need_video_list) == 0:#如果未选择任何视频
            out.toast('未选择任何视频',color='info',duration='0')#弹出错误弹窗
            return 'out'
    return [data,need_video_list,need_quality]

#显示完成列表
def show_fin_list():
    """
    处理下载列表并显示
    {'need_video','control_name'}
    """
    #加载任务列表
    data_list = core.load_json()['fin_down_list']#获取需要下载的列表
    if len(data_list) == 0:#如果列表为空则等待
        time.sleep(1)
        show_fin_list()
    show_list = []
    #初始化
    for list_one in data_list:#遍历创建下载列表
        show_list.append([
            out.put_row([
                out.put_text(list_one['video_info']['page_name']),#TODO 创建标题
                out.put_column([
                    out.put_scope('sta_text_'+list_one['control_name']),#创建用于进度提示的域,控制值为'sta_text_'+list_one['control_name']
                    out.put_processbar(list_one['control_name'],init=0)#下载列表,控制值为list_one['control_name']
                    ]),
                out.put_scope('sta_worktype_'+list_one['control_name']),#创建用于显示任务状态的域,控制值为'sta_worktype_'+list_one['control_name']
                ])
        ])# 创建显示
    
    #显示列表
    with out.use_scope('fin_work',clear=True):#清除域
        out.put_table(show_list)

        #刷新状态
        while 1==1:
            for list_one in data_list:#遍历下载列表
                get_task_info = core.get_task_status(list_one['control_name'])#获取下载任务状态
                if get_task_info == None:#如果类型为None说明该任务不在下载器中 TODO 未来实现自动添加任务继续下载
                    remove_task(list_one['control_name'])#移除任务
                    show_down_list()#重新启动下载列表维护进程
                out.set_processbar(list_one['control_name'],value= get_task_info['progress'] / 100)#刷新进度条状态
                with out.use_scope('sta_text_'+list_one['control_name'],clear=True):#进入用于进度提示的域并清空
                    out.put_text(get_task_info['status_text'])#显示进度提示文本
                with out.use_scope('sta_worktype_'+list_one['control_name'],clear=True):#进入用于显示任务状态提示文本的域并清空
                    out.put_text(get_task_status(int(get_task_info['task_status'])))#显示任务状态提示文本
                    if int(get_task_info['task_status']) == 6:#如果任务下载完成
                        remove_fin_task(list_one['control_name'])#将任务移入完成列表
                if get_task_info['msg'] != '':#如果出现错误信息
                    out.toast(list_one['video_info']['video_filename']+'   '+get_task_info['msg'],color='error')
            time.sleep(1)#等待1秒
            #如果下载列表更新
            if data_list != core.load_json()['need_fin_list']:#如果现在维护的和存储的不一样
                show_fin_list()

#显示下载列表
def show_down_list():
    """
    处理下载列表并显示
    {'need_video','control_name'}
    """
    #加载任务列表
    data_list = core.load_json()['need_down_list']#获取需要下载的列表
    if len(data_list) == 0:#如果列表为空则等待
        time.sleep(1)
        show_down_list()
    show_list = []
    #初始化
    for list_one in data_list:#遍历创建下载列表
        show_list.append([
            out.put_row([
                out.put_text(list_one['video_info']['page_name']),#TODO 创建标题
                out.put_column([
                    out.put_scope('sta_text_'+list_one['control_name']),#创建用于进度提示的域,控制值为'sta_text_'+list_one['control_name']
                    out.put_processbar(list_one['control_name'],init=0)#下载列表,控制值为list_one['control_name']
                    ]),
                out.put_scope('sta_worktype_'+list_one['control_name']),#创建用于显示任务状态的域,控制值为'sta_worktype_'+list_one['control_name']
                #out.put_button('暂停',onclick=lambda:core.patch_pause_task(list_one['control_name']),color='warning'),#暂停按钮
                out.put_button('删除',onclick=lambda:remove_task(list_one['control_name']),color='danger'),#删除按钮
                ])
        ])# 创建显示
    
    #显示列表
    with out.use_scope('down_work',clear=True):#清除域
        out.put_table(show_list)

    #刷新状态
    while 1==1:
        for list_one in data_list:#遍历下载列表
            get_task_info = core.get_task_status(list_one['control_name'])#获取下载任务状态
            if get_task_info == None:#如果类型为None说明该任务不在下载器中 TODO 未来实现自动添加任务继续下载
                remove_task(list_one['control_name'])#移除任务
                show_down_list()#重新启动下载列表维护进程
            out.set_processbar(list_one['control_name'],value= get_task_info['progress'] / 100)#刷新进度条状态
            with out.use_scope('sta_text_'+list_one['control_name'],clear=True):#进入用于进度提示的域并清空
                out.put_text(get_task_info['status_text'])#显示进度提示文本
            with out.use_scope('sta_worktype_'+list_one['control_name'],clear=True):#进入用于显示任务状态提示文本的域并清空
                out.put_text(get_task_status(int(get_task_info['task_status'])))#显示任务状态提示文本
                if int(get_task_info['task_status']) == 6:#如果任务下载完成
                    remove_fin_task(list_one['control_name'])#将任务移入完成列表
            if get_task_info['msg'] != '':#如果出现错误信息
                out.toast(list_one['video_info']['video_filename']+'   '+get_task_info['msg'],color='error')
        time.sleep(1)#等待1秒
        #如果下载列表更新
        if data_list != core.load_json()['need_down_list']:#如果现在维护的和存储的不一样
            show_down_list()

#解析输入的url
def start_url():
    url = pin.pin['url_input']#获取输入
    check_return = check_input_url(url)
    if check_return != None:
        out.toast(check_return,duration=3,color='error')#显示错误信息
        return
    #清除旧显示内容
    out.clear('video_info')
    with out.use_scope('main'):
    #显示加载提示
        with out.use_scope('load'):
            out.put_row([
                None,
                out.put_loading(),
                out.put_text('解析中'),
                None
                ],size='1fr auto auto 1fr')
            
        #解析url
        out_url = get_video_id(url)
        get_video_info = core.info(out_url[0],out_url[1])
        return_data = print_video_info(get_video_info)#显示视频信息,返回视频信息
        if return_data == 'out':#如果选择退出界面或未勾选任何视频
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
            return_down_data:dict = core.post_new_task(need_video['page_av'],need_video['page_cid'],video_data,audio_data,make_down_name(return_data,need_video))
            set_info['need_down_list'].append({'control_name':return_down_data['data']['control_name'],'video_info':need_video})#添加控制字节段至下载列表
            core.save_json(set_info)#刷新设置里的下载列表
            num += 1
            out.set_processbar('loading',num / len(return_data[1]))#设置进度条进度
        out.clear('loading')
        out.put_text('任务发送完成')
    return

#主函数
def main():#主函数
    print('主函数启动')
    if not start_jiji_core.is_alive():
        print('启动核心')
        io.session.register_thread(start_jiji_core)
        start_jiji_core.setDaemon(True)#设为守护进程
        start_jiji_core.start()
    with out.use_scope('main'):#创建并进入main域
        out.scroll_to('main','top')
        #等待核心响应提示
        with out.use_scope('load'):
            out.put_row([
                None,
                out.put_loading(color='primary').style('width:4rem; height:4rem'),
                None,
                out.put_column([
                        None,
                        out.put_text('等待核心响应,请检查核心是否启动').style('line-height: 0'),
                    ],size='1fr 1fr'),
                None
            ],size='1fr auto 20px auto 1fr')
        while core.check() != 'ok':#当响应不正确
            time.sleep(1)
        out.clear('load')
        out.remove('load')
        #初始化
        out.scroll_to('main','top')
        out.clear('main')
        #检查登录
        user_info = core.get_user_info()
        if user_info['code'] == True:#如果已登录
            with out.use_scope('user_info'):#切换到用户信息域
                face = requests.get(user_info['face']).content#缓存图片
                out.put_row([
                    None,
                    out.put_image(face,height='50px').style('margin-top: 1rem;margin-bottom: 1rem;border:1px solid;border-radius:50%;box-shadow: 5px 5px 5px #A9A9A9'),
                    None,
                    out.put_column([
                        None,
                        out.put_text('当前登录用户:'+user_info['uname']+user_info['vip_label_text']).style('font-size:1.25em;line-height: 0'),
                        ],size='1fr 1fr'),
                    None
                ],size='1fr 50px 25px auto 1fr').style('border: 1px solid #e9ecef;border-radius: .25rem')#限制用户头像大小
        else:
            return_data = core.get_login_status()#获取二维码
            with out.use_scope('login'):
                out.put_row([
                    None,
                    out.put_column([
                        out.put_text('请扫描二维码登录').style('line-height: 1;text-align:center'),
                        out.put_image(return_data['image']),
                        None
                    ],size='auto 1fr 1rem').style('border: 1px solid #e9ecef;border-radius: .25rem;box-shadow: 5px 5px 5px #A9A9A9'),
                    None
                ],size='1fr auto 1fr')
            while 1==1:
                check_user_info = core.get_user_info()#循环检查是否扫描
                if check_user_info['code'] == True:#如果登录成功
                    out.clear('login')
                    out.remove('login')
                    return
                time.sleep(1)
        
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
            out.put_tabs([{'title':'下载中','content':scope_down_work},{'title':'下载完成','content':scope_down_fin}])#创建横向标签栏
            
            # 开启新线程
            thread1 = threading.Thread(target=show_down_list)
            thread2 = threading.Thread(target=show_fin_list)
            if not thread1.is_alive():
                print('启动线程1')
                io.session.register_thread(thread1)
                thread1.setDaemon(True)#设为守护进程
                thread1.start()
            if not thread2.is_alive():
                print('启动线程2')
                io.session.register_thread(thread2)
                thread2.setDaemon(True)#设为守护进程
                thread2.start()

        #创建设置
        with out.use_scope('set'):#进入域
            out.put_row([out.put_text('目前下载地址：'),pin.put_input(name='change_dir',value=core.get_down_dir()),out.put_button('确认修改',onclick=check_dir)])

print('自动更新核心')
core.update_core(system_type,system_bit)#更新核心
start_jiji_core = threading.Thread(target=start_core)
io.config(title='Jithon 2.0 Beta',description='本应用为唧唧2.0基于python的webui实现',theme='yeti')
print('主程序启动,如未自动跳转请打开http://127.0.0.1:8080')
io.start_server(main,host='127.0.0.1',port=8080,debug=True,cdn=False,auto_open_webbrowser=True)