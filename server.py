"""
date: 2018-10-5
auther: cjw
project_name: server.py
dest: 通过单进程单线程非阻塞的方式实现完成多任务 
"""

import socket


def response_data(new_tcp_socket):
    rensponse_body = 'hahaha'
    response_header = 'http/1.1 200 OK\r\n'
    # Content_length 目的建立长连接时，告诉浏览器要显示的内容
    response_header += 'Content-Length:%d\r\n' % (len(rensponse_body))
    response_header += '\r\n'
    rensponse_body = 'hahaha'
    response = response_header + rensponse_body
    new_tcp_socket.send(response.encode('utf-8'))
    

def main():
    # 创建tcp套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置端口重用
    tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # 绑定地址
    localhost = ('', 8000)
    tcp_socket.bind(localhost)

    # 设置监听套接字
    tcp_socket.listen(128)

    # 设置为非阻塞
    tcp_socket.setblocking(False)
    new_tcp_sockets = list()

    while True:
        # 监听客户端连接
        try:
            new_tcp_socket, new_addr = tcp_socket.accept()
        except Exception as ret:
            print('还没有客户端连接')
        else:
            # 保存到列表中
            new_tcp_sockets.append(new_tcp_socket)

            # 设置为非阻塞套接字
            new_tcp_socket.setblocking(False)

        # 遍历列表
        for new_tcp_socket in new_tcp_sockets:
            try:
                revc_data = new_tcp_socket.recv(1024)
            except Exception as ret:
                print('客户端还没有发起数据')
            else:
                # 判断revc_data 数据　
                if revc_data :
                    # 处理客户端请求
                    response_data(new_tcp_socket)
                else:
                    # 关闭套接字
                    new_tcp_socket.close()
                    # 从列表中删除套接字
                    new_tcp_sockets.remove(new_tcp_socket)

    # 关闭监听套接字
    tcp_socket.close()



if __name__ == "__main__":
    main()
