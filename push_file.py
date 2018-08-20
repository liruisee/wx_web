import sys
from os.path import dirname, abspath, exists
import subprocess


# 捕获系统异常
def system_exe_output(cmd):
    assert(type(cmd) == str)
    status, result = subprocess.getstatusoutput(cmd)
    if int(status) != 0:
        raise Exception(result)
    return result


# 把本地文件推送到远端服务器（需要ssh）
def push_file(src_path, dest_user, dest_host, dest_path=None, is_cover=True):
    cmd_conf = '-avz'
    if not is_cover:
        cmd_conf += 'u'
    if dest_path is None:
        root_path = abspath(__file__).rsplit('/wx_web', 1)[0]
        dest_root_path = '/root/page_test_pro'
        dest_path = dirname(dest_root_path + src_path.replace(root_path, ''))
        print("上传的本地路径为：%s" % src_path)
        print("上传到服务器的路径为：%s" % dest_path)
    result = system_exe_output("rsync %s %s %s@%s:%s" % (cmd_conf, src_path, dest_user, dest_host, dest_path))
    print(result)
    return result


if __name__ == '__main__':
    # file_path = '你要上传的文件路径'
    file_path = '/Users/ruili/pyproject/wx_web/wx_app/migrations/__init__.py'
    if not exists(file_path):
        print("上传的文件路径不存在，请确认路径")
        exit(1)
    push_file(file_path, 'root', '118.89.222.232')
    # pull_file('sf', '118.89.112.211', '/cloud/data/lirui/projects/data_scripts/scripts/moxie_small_number/files', '/Users/ruili/svn/data_scripts/common_util/system_util')
