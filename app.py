import re
import os
import time

import requests
import pywebio as io
out = io.output
ioin = io.input
pin = io.pin
import core

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

#获取被勾选视频数据
def get_video_list_info(num:int) -> list:
    """
    获取被勾选的视频数据
    """
    info_list = []
    for checkbox_one in range(1,num):
        if len(pin.pin['check_'+str(checkbox_one)]) != 0:
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

#处理下载文件名
def make_down_name(info_date:dict,video_data:dict) -> str:
    """
    下载文件名处理
    预留接口
    """
    return video_data['video_filename'][:-3]

#显示视频下载界面
def print_video_info(info) -> list:
    """
    创建视频下载界面
    返回[视频信息,需下载视频列表,清晰度]
    """
    with out.use_scope('video_info'):#进入视频信息域
        data = info['data']
        with out.use_scope('up_info'):#切换到up信息域
            face = requests.get(data['up_face']).content#缓存图片
            out.put_row([out.put_image(face,height='50px'),out.put_text(data['up_name'])])#限制up头像大小
        out.put_text(data['video_title'])#视频标题
        if data['video_cover'] != '':
            cover = requests.get(data['video_cover']).content#缓存图片
            out.put_image(cover)#视频封面
        out.put_text(data['video_desc'])#视频简介
        out.put_text('视频类型 '+str(data['sort'])+'-'+str(data['sub_sort']))
        out.put_text('视频发布时间 '+data['bili_pubdate_str'])
        #out.put_column([info_title,info_cover,info_desc,info_sort])#设置为垂直排布
        #创建清晰度选择
        get_video_quality_info = get_video_quality_list(core.quality(data['list'][0]['page_av'],data['list'][0]['page_cid']))#读取视频列表第一个的清晰度
        with out.use_scope('quality'):#创建清晰度选择域
            pin.put_select(name='select_video',options=get_video_quality_info[0],value={'quality':1000})#创建视频选择
            pin.put_select(name='select_audio',options=get_video_quality_info[1],value={'quality':30280})#创建音频选择

        #创建列表
        table_list = []
        num = 0
        table_list.append(['选择','标题'])
        for one in data['list']:#遍历列表
            num += 1
            list_one = []
            list_one.append(pin.put_checkbox(name='check_'+str(num),options=[{'label':str(num),'value':one}]))#创建单选框
            list_one.append(one['page_name'])#标题
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
        elif control_buttom == '1':#如果选择下载全部
            need_video_list:list = data['list']
        elif control_buttom == '2':#如果选择退出
            return 'out'
        if  len(need_video_list) == 0:#如果未选择任何视频
            out.toast('未选择任何视频',color='info',duration='0')#弹出错误弹窗
            return 'out'
    return [data,need_video_list,need_quality]

def main():#主函数
    with out.use_scope('main'):#创建并进入main域
        out.scroll_to('main','top')
        out.clear('main')
        #检查登录
        user_info = core.get_user_info()
        if user_info['code'] == True:#如果已登录
            with out.use_scope('user_info'):#切换到用户信息域
                face = requests.get(user_info['face']).content#缓存图片
                out.put_row([out.put_image(face,height='50px'),out.put_text(user_info['uname']+user_info['vip_label_text'])])#限制用户头像大小
        else:
            return_data = core.get_login_status()#获取二维码
            with out.use_scope('login'):
                out.put_text('请扫描二维码登录')
                out.put_image(return_data['image'])
            while 1==1:
                check_user_info = core.get_user_info()#循环检查是否扫描
                if check_user_info['code'] == True:#如果登录成功
                    out.clear('login')
                    out.remove('login')
                    main()
                time.sleep(1)
        
        #添加设置
        with out.use_scope('set',position=-1):#创建域,并设置位置为底部
            out.put_row([out.put_text('目前下载地址：'),pin.put_input(name='change_dir',value=core.get_down_dir()),out.put_button('确认修改',onclick=check_dir)])
        
        #创建url输入框
        url = ioin.input('请输入链接',type='text',validate=check_input_url,position=1)#限制类型为url,使用check_input_url检查内容
        #显示加载提示
        with out.use_scope('load'):
            out.put_loading()
            out.put_text('解析中')
        #解析url
        out_url = get_video_id(url)
        get_video_info = core.info(out_url[0],out_url[1])
        return_data = print_video_info(get_video_info)#显示视频信息,返回视频信息
        if return_data == 'out':#如果选择退出界面
            out.clear('video_info')
            main()
        #开始下载任务
        down_list = []
        video_data = return_data[2]['video']
        audio_data = return_data[2]['audio']
        #滚动到最底下
        out.scroll_to('main','buttom')
        out.put_processbar('loading',init=0)#设置进度条
        num = 0
        for need_video in return_data[1]:
            return_down_data:dict = core.post_new_task(need_video['page_av'],need_video['page_cid'],video_data,audio_data,make_down_name(return_data,need_video))
            down_list.append(return_down_data['data']['control_name'])#添加控制字节段至列表
            num += 1
            out.set_processbar('loading',num / len(return_data[1]))#设置进度条进度

#启动服务器
#io.start_server(main,port=8080, debug=True)
main()