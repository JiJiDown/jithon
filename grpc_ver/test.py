import grpc
import json
from grpc_core import user_pb2
from grpc_core import user_pb2_grpc
import base64
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
run()
print

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