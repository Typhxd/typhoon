'''
****************************************************
*             任务执行模块                         *          
*          1. 检查任务队列是否存在任务             *
*          2. 从任务队列中取任务并执行             *
*          3. 发送控制命令到指定的智能体           *
*          4. 读取全部任务队列中任务，并依次执行   *
*          5. 未来或许可以根据配置的智能体参数，   *
*             动态修改智能体的计算资源等           *
*                                                  *
*             author： joliu<joliu@s-an.org>       *
*             date: 2018-3-22                      *
****************************************************
'''

from listenSer import sendBySocket
from listenSer import sendCommandToDevice

import sqlite3
import time

def findTask():
    try:
        sql = "select * from task"
        conn = sqlite3.connect("task.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
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


# 根据任务队列中任务，依次执行
def doTask():
    (status, outputs) = findTask()
    if status != 1:
        return (status, outputs)
    for output in outputs:
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
        (status, data) = sendCommandToDevice(method)
        # 千杀的dht11，需要处理下数据
        data = data.split('&')[0]
        print(output)
        if status == -1:
            print("get device data failed! ip: %s, method: %s" % (ip, method))
            return (status, "get device data failed! ip: %s, method: %s" % (ip, method))

        if compare(condition[0], float(data), float(condition[1:])):
            # 当结果为真，向目标传感器发出指令
            (status, recvdata) = sendBySocket(ip, int(port), method)
            print(recvdata)
            time.sleep(ctime)
        else:
            pass

    return (1, 'success')


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
    while True:
        print("cycle time :" + str(input_ctime))
        time.sleep(input_ctime)
        (status, output) = doTask()
        print(output)


if __name__ == "__main__":
    mainWhileProcess(5)
