'''
****************************************************
*             任务执行模块                         *          
*          1. 检查任务队列是否存在任务             *
*          2. 从任务队列中取任务并执行             *
*          3. 发送控制命令到指定的智能体           *
*          4. 未来或许可以根据配置的智能体参数，   *
*             动态修改智能体的计算资源等           *
*                                                  *
*             author： joliu<joliu@s-an.org>       *
*             date: 2018-3-22                      *
****************************************************
'''
import sqlite3
import time
import socket


# 发送控制指令到Device
def sendCommandToDevice(cmd):
    # 通过容器的环境变量HOST获取绑定传感器的IP地址
    ip, port = "192.168.12.75", 8085
    return sendBySocket(ip, port, cmd)



def findTask():
    try:
        sql = "select * from task LIMIT 1"
        conn = sqlite3.connect("task.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            (status, output) = (-1, 'database is empty!')
        else:
            (status, output) = (1, data)
    except sqlite3.Error as err_msg:
        (status, output) = (-1, err_msg)
    except Exception as err_msg:
        (status, output) = (-1, err_msg)
    finally:
        return (status, output)


# 通过socket发送信息
def sendBySocket(ip, port, cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err_msg:
        print("Error creating socket:%s" % err_msg)
        s.close()
        return (-1, err_msg)
    try:
        s.connect((ip, port))
    except socket.error as err_msg:
        print("Address-related error connecting to server: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    print("****************send:" + cmd)
    try:
        s.sendall(cmd.encode())
    except socket.error as err_msg:
        print("Error sending data: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    try:
        response = s.recv(1024).decode()
        print(response)
    except socket.error as err_msg:
        print("Error receiving data: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    #print(str(response))
    s.close()
    # 程序运行正常返回目标传感器返回的数据
    return (1, str(response))

# 根据符号来比较两个数值的大小
def compare(signal, value1, value2):
    if signal == '>':
        return value1 > value2
    elif signal == '<':
        return value1 < value2
    elif signal == '=':
        return value1 == value2
    else:
        return False


def mainWhileProcess(input_ctime):
    ctime = input_ctime
    while True:
        print(ctime)
        time.sleep(ctime)
        (status, output) = findTask()
        if status == -1:
            print(output)
            # 如果数据库为空，或者错误，恢复初始设置
            ctime = input_ctime
            continue

        (task, taskid, ctime) = output
        if len(task.split(';')) != 2 or len(task.split(':')) != 3:
            print("Error task: %s" % task)
            continue
    
        # 初步定义task字符串模式 eg: >30;192.168.1.1:3000:off
    
        (condition, command) = task.split(';')
        (ip, port, method) = command.split(':')
        # 构建控制命令
        method = 'device&' + method
        # 读取传感器数值
        (status, output) = sendCommandToDevice(method)
        # 千杀的dht11，需要处理下数据
        output = output.split('&')[0]
        print(output)
        if status == -1:
            print("get device data failed! ip: %s, method: %s" % (ip, method))
            continue

        if compare(condition[0], float(output), float(condition[1:])):
            # 当结果为真，向目标传感器发出指令
            (status, output) = sendBySocket(ip, int(port), method)
            #print(output)
        else:
            pass

        print(1212)


if __name__ == "__main__":
    mainWhileProcess(5)
