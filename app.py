import pywebio as io

def main():#主函数
    io.output.put_scope('main')
    io.output.put_text('hello world')

#启动服务器
io.start_server(port=8080, debug=True)