import re
import socket
import time

import paramiko


class Ssh2Client:
    """
    ssh2客户端封装
    """

    def __init__(self, host: str, port: int):
        """
        功能描述：构造函数

        :param host: 主机地址
        :param port: 端口信息
        """
        self.__host = host
        self.__port = port
        self.__ssh = None
        self.__channel = None

        # 7-bit C1 ANSI sequences
        self.__ansi_escape = re.compile(r'''
                \x1B  # ESC
                (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
                |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)

    def __del__(self):
        self.__close()

    def connect(self, user: str, pwd: str) -> bool:
        """
        功能描述：连接远程主机
        :param user: 用户名
        :param pwd:  用户密码
        :return: 连接成功还是失败
        """
        self.__close()

        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.connect(self.__host, username=user, password=pwd, port=self.__port)
        return True

    def exec(self, cmd: str, end_str=('# ', '$ ', '? ', '% ', '#', '$', '?', '%'), timeout=5) -> str:
        """
        功能描述：执行命令
        :param cmd: shell命令
        :param end_str: 提示符
        :param timeout: 超时间时间
        :return: 命令执行结果
        """
        if not self.__channel:
            self.__channel = self.__ssh.invoke_shell(term='xterm', width=4096, height=48)
            time.sleep(0.1)
            self.__channel.recv(4096).decode()

        if cmd.endswith('\n'):
            self.__channel.send(cmd)
        else:
            self.__channel.send(cmd + '\n')

        if end_str is None:
            return self.__recv_without_end(cmd, timeout)

        result = self.__recv(end_str, timeout)
        begin_pos = result.find('\r\n')
        end_pos = result.rfind('\r\n')
        if begin_pos == end_pos:
            return ''
        return result[begin_pos + 2:end_pos]

    def __recv_without_end(self, cmd, timeout):
        """
        功能描述：接收命令执行结果，不进行任何比对。
        :param cmd: 命令
        :param timeout:超时时间，最长等待3秒
        :return: 命令执行结果
        """
        out_str = ''
        if timeout > 3:
            timeout = 3
        max_wait_time = timeout * 1000
        self.__channel.settimeout(0.1)
        while max_wait_time > 0.0:
            try:
                start = time.perf_counter()
                out = self.__channel.recv(1024 * 1024).decode()
                out_str = out_str + out
                max_wait_time = max_wait_time - (time.perf_counter() - start) * 1000
            except socket.timeout:
                max_wait_time -= 100
        return out_str

    def __recv(self, end_str, timeout) -> str:
        """
        功能描述：根据提示符，接收命令执行结果
        :param end_str: 预期结果结尾
        :param timeout: 超时间
        :return: 命令执行结果，去除命令输入提示符
        """
        out_str = ''
        max_wait_time = timeout * 1000
        self.__channel.settimeout(0.05)
        while max_wait_time > 0.0:
            try:
                out = self.__channel.recv(1024 * 1024).decode()

                if not out or out == '':
                    continue
                out_str = out_str + out

                match, result = self.__match(out_str, end_str)
                if match is True:
                    return result.strip()
                else:
                    max_wait_time -= 50
            except socket.timeout:
                max_wait_time -= 50

        raise Exception('recv data timeout')

    def __match(self, out_str: str, end_str: list) -> (bool, str):
        result = self.__ansi_escape.sub('', out_str)

        for it in end_str:
            if result.endswith(it):
                return True, result
        return False, result

    def __close(self):
        if not self.__ssh:
            return
        self.__ssh.close()
        self.__ssh = None
