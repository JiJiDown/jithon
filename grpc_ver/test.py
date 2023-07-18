import grpc
import json
from grpc_core import user_pb2
from grpc_core import user_pb2_grpc
from grpc_core import task_pb2
from grpc_core import task_pb2_grpc
from grpc_core import status_pb2
from grpc_core import status_pb2_grpc
from grpc_core import bvideo_pb2
from grpc_core import bvideo_pb2_grpc
import base64
import core
import subprocess
import ctypes,sys,os

import requests

import google.protobuf.empty_pb2 as empty_pb2
import os
#需要创建pyi文件不然pb2不知道使用哪个类

#错误处理
def run():
    channel = grpc.insecure_channel('localhost:64000')
    stub = user_pb2_grpc.UserStub(channel)
    #a = stub.LoginQRCode(user_pb2.UserLoginQRCodeReq(api=0),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    #input(a.id)
    try:
        b = stub.LoginStatus(user_pb2.UserLoginStatusReq(id='da546958-fd3d-4369-ae8c-bfd382028f8e'),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
        for c in b:
            print(c.status)
    except Exception as e:
            code_name = e.code().name       # 错误类型
            code_value = e.code().value
            print(e.details())#错误信息
            print(code_name)#错误类型
            print(code_value)#错误状态码

def runb():
    channel = grpc.insecure_channel('localhost:64000')
    stub = user_pb2_grpc.UserStub(channel)
    try:
        response = stub.Info(user_pb2.UserInfoReply(),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    except Exception as e:#捕获错误
        print(e)
        input()
    b = ''
    for a in response.face:
            b += str(a)
    with open('face.png','wb') as f:
        f.write(response.face)

def runc():
    channel = grpc.insecure_channel('localhost:64000')
    stub = bvideo_pb2_grpc.BvideoStub(channel)
    response = stub.Info(bvideo_pb2.BvideoContentReq(content='https://www.bilibili.com/video/BV1us4y167zF/?spm_id_from=333.1007.tianma.1-3-3.click&vd_source=32f2f4d0d74594e0b5a183b394bf9a49'),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    print(response.video_title)
    a = response.block[0].list[0]
    print(a.page_bv)
    print

def rund():
    channel = grpc.insecure_channel('localhost:64000')
    stub = bvideo_pb2_grpc.BvideoStub(channel)
    response = stub.Info(bvideo_pb2.BvideoContentReq(content='https://www.bilibili.com/video/BV1us4y167zF/?spm_id_from=333.1007.tianma.1-3-3.click&vd_source=32f2f4d0d74594e0b5a183b394bf9a49'),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    response = stub.AllQuality(bvideo_pb2.BvideoAllQualityReq(aid=response.block[0].list[0].page_av,cid=response.block[0].list[0].page_cid),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    print

def rune():
    out = core.info('https://www.bilibili.com/video/BV1us4y167zF')
    response = core.quality(bvid=out['block'][0].list[0].page_bv,cid=out['block'][0].list[0].page_cid)
    print(response)

def login():
    channel = grpc.insecure_channel('localhost:64000')
    stub = user_pb2_grpc.UserStub(channel)
    response = stub.LoginQRCode(user_pb2.UserLoginQRCodeReq(api=1),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    login_image:bytes = response.qr_code
    with open('qr.png','wb') as f:
         f.write(login_image)

def update():
    channel = grpc.insecure_channel('localhost:64000')
    stub = status_pb2_grpc.StatusStub(channel)
    response =stub.CheckUpdate(empty_pb2.Empty(),metadata=[('client_sdk','JiJiDownPython/1.0.0')])
    for one in response:
        print(one.status)
        print(one.change_log)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
	print("以管理员权限运行")
	# 杀掉名字为Au_.exe的进程
	os.system("taskkill /im Au_.exe /f")
else:
	if sys.version_info[0] == 3:
		print("无管理员权限")
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
