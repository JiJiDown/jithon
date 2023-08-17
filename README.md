# Jithon
## 鸡枞

Jithon(**鸡枞**)2.0是Jithon 1.0**重构开发**的基于**webUI**界面的唧唧**2.0**前端
拥有**现代化的外观**、**人性化的交互**以及支持**跨平台运行**的特点

本次更新重点：

1. 实现了**彻底无需旧前端**的新前端发布
2. 基于多线程实现了下载列表的**实时刷新**
3. 支持**批量**视频下载
4. 支持**一键下载**收藏夹等视频集合
5. 支持**批量选定分辨率**下载
6. webUI的特点使得该前端可以部署在**任何设备上**实现远程下载
7. 已经**完全支持**唧唧2.0核心支持的各种链接解析
8. 可以和旧UI共存互不干扰（仅需下载Jithon_2.0_Beta.exe)
9. 支持**自动修复核心启动错误**
10. 支持**cookies登录**或者自动通过浏览器缓存**一键登录**

在经历2023/1/11的更新过后，主程序已经会**自动配置**核心以及配置文件了  
仅需下载主程序并放到合适位置启动  
主程序会自动根据当前系统下载核心、配置相关环境、自动设置主程序位置为下载目录

## 下载Jithon
预编译完成的二进制文件可以在 [Github releases](https://github.com/JiJiDown/jithon/releases) 找到  
目前有两个平台的版本
- Windows7-11 **AMD64**
- Linux 2.6.23及之后版本 **ARM64**(Ubuntu系)
- Linux 2.6.23及之后版本 **AMD64**(Ubuntu系)
## 软件截图

[![image.png](https://i.postimg.cc/mDpyp3jL/image.png)](https://postimg.cc/jwNfL7Bm)

[![17-12-2022-5455-127-0-0-1.jpg](https://i.postimg.cc/xd4Ptyt0/17-12-2022-5455-127-0-0-1.jpg)](https://postimg.cc/xkLHdmw7)

## 自行构建步骤
0. 从Github下载代码
1. 安装python**3.8**或以上版本
2. 使用pip指令安装依赖  
```Plain
requests
pywebio
pyinstaller
grpcio
grpcio-tools
tqdm
pyuac
loguru
plyer
```
3. 创建pyinstaller spec (specification) 文件  
```Plain
pyi-makespec app.py
```  
或者如下，选择使用pyinstall参数生成单文件
```Plain
pyi-makespec -F app.py
```
4. 编辑生成的spec文件，将其中`Analysis`的`data`参数修改为:  
```Python
from pywebio.utils import pyinstaller_datas

a = Analysis(
    ...
    datas=pyinstaller_datas(),
    ...
```
5. 使用spec文件来构建可执行文件:  
```Plain
pyinstaller app.spec
```
6. 构建成功会显示类似如下所示的内容  
>`39416 INFO: Building EXE from EXE-00.toc completed successfully.`  

构建的二进制文件会出现在当前目录下的`dist`文件夹