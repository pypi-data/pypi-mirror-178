import sys
import os
from optparse import OptionParser
from rosdep2.main import rosdep_main


import locale
encoding = locale.getpreferredencoding()
encoding_utf8 = encoding.find("UTF")>-1

hints = dict()
hints['welcome'] = """
欢迎使用国内版rosdep之rosdepc，我是作者小鱼！
欢迎关注公众号《鱼香ROS》加入交流群
小鱼rosdepc正式为您服务
"""
hints["init_success"] = """
小鱼提示：恭喜你完成初始化，快点使用\n\n rosdepc update\n\n更新吧
因为有一些小伙伴更新使用rosdep update,老是搞错,小鱼就直接帮你进行更新了!请稍等!
"""
hints["update_success"] = """
小鱼恭喜：rosdepc已为您完成更新!!
如果在上述更新中遇到错误,请查看rosdepc常见错误解决方案:https://fishros.org.cn/forum/topic/676
"""
hints["final_tip"] = """
如果在使用过程中遇到任何问题，欢迎通过fishros.org.cn反馈，最后加入QQ交流群 686914208(入群口令：一键安装)
"""

if not encoding_utf8:
    hints['welcome'] = """
Welcome to the Chinese version of the ROSDEP rosdepc, I am the author of small fish!
Welcome to join the exchange group on wechat public account“FISHROS”
The Little Fish rosdepc is officially at your service!
"""
    hints["init_success"] = """
Small fish tip: Congratulations on your initialization, and hurry up with the
rosdepc update
Because there are some small partners update using ROSDEP update, always get it wrong, small fish directly to help you with the update! One moment, please!
"""
    hints["update_success"] = """
Fish congratulations: rosdedpc has completed the update for you! !
"""
    hints["final_tip"] = """
If you encounter any problems in the process of using, welcome to use fishros.org.cn feedback, and finally join QQ Exchange Group 686914208(password: one-click installation)
"""

def main(args=None):
    if len(sys.argv)==1:
        os.system("rosdep")
        return
    command = sys.argv[1]
    print(hints['welcome'])
    print("---------------------------------------------------------------------------")
    if command=="init":
        os.system("sudo mkdir -p /etc/ros/rosdep/sources.list.d/ >> /dev/null")
        os.system("sudo wget https://mirrors.tuna.tsinghua.edu.cn/github-raw/ros/rosdistro/master/rosdep/sources.list.d/20-default.list -O /etc/ros/rosdep/sources.list.d/20-default.list ")
        print(hints["init_success"])
        os.system("export ROSDISTRO_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/rosdistro/index-v4.yaml && rosdep update")
        print(hints["update_success"])
    elif command=='update':
        os.system("export ROSDISTRO_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/rosdistro/index-v4.yaml && rosdep update")
        print(hints["update_success"])
    else:
        rosdep_main(sys.argv[1:])
    print("---------------------------------------------------------------------------")
    print(hints["final_tip"])

