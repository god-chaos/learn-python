import pytest

from common.Ssh2Client import Ssh2Client


class TestSsh2Client:
    def test_nfs(self):
        ssh = Ssh2Client('192.168.50.227', 22)
        ssh.connect('root', '******')

        result = ssh.exec('ls -l /')
        print(result)

    def test_local(self):
        ssh = Ssh2Client('127.0.0.1', 22)
        ssh.connect('sniper', '******')

        result = ssh.exec('ls -l /')
        print(result)
        pass


if __name__ == '__main__':
    pytest.main(["-qq"], plugins=[TestSsh2Client()])
