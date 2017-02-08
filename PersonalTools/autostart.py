#!python 3.5
#coding:utf-8
#该脚本功能是, Windows开机后探测磁盘空置率, 若高于95%, 即启动测试虚拟机(vm_ops), 然后探测虚拟磁盘G是否挂载, 若已挂载, 打开Dropbox.
import subprocess
import psutil
import os
import time


#commands
vm_ops = ['C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe', 'start', 'E:\\Virtual Machines\\CentOS7.2\\CentOS7.2.vmx']
dbx_start = ['C:\\Program Files (x86)\\Dropbox\\Client\\Dropbox.exe']
vm_ping = ['ping', '-n', '1', '-w', '800', '192.168.116.128']
disk_per = """typeperf "LogicalDisk(_Total)\% Idle Time" -sc 1"""

#processes and files
process_dbx = 'dropbox.exe'
dbx_dir = 'g:\\dropbox'

def execute(command):
    """
    无阻塞无反馈信息执行命令
    """
    exec_cmd = subprocess.Popen(command)
    print('Command {} excuted'.format(command))
    time.sleep(3)
    return exec_cmd

def execute_full(command):
    """
    命令执行函数, 可获取全返回信息, 可能会阻塞
    """
    exec_cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return ('Command {} excuted'.format(command), exec_cmd.communicate()[0].decode('gbk'))

def ping(vm_ping):
    try:
        output = subprocess.check_output(vm_ping)
        print(output)
        return 0
    except Exception as e:
        print(e)
        return 1

def proc_find(process):
    proc_lst = [ p.name().lower() for p in psutil.process_iter()]
    return True if process in proc_lst else False

def exists(obj):
    return os.path.exists(obj)

def main():
    while 1:
        isdbx = proc_find(process_dbx)
        isdir = exists(dbx_dir)
        disk_percent = execute_full(disk_per)[1].split('"')[7]
        if float(disk_percent) > 95:
            print('当前IO空闲率: {}%'.format(float(disk_percent)))
            execute(vm_ops)
            if isdir and not isdbx:
                execute(dbx_start)
                break
            elif isdir and isdbx:
                print('Disk mounted and Dropbox is running, exit')
                time.sleep(3)
                break
        time.sleep(3)

if __name__ == '__main__':
    main()
