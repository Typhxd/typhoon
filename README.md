# opencps-agent

新版本 智能体版本

##### 2018-3-21  

1. 完成智能体单元模块

##### 2018-3-22

1. 添加任务循环监听处理模块
2. 更改一些智能体单元模块bug

## 版本说明

智能体虚拟化模块主要有两大功能

1. 监听控制器的配置请求
2. 监听其他传感器的控制请求

### 目前智能体支持的控制命令
|控制命令|说明|范例|
|--------|----|----|
|add|添加一条任务|controller&add&>30;192.168.1.1:3000:off&20|
|clear|清空任务队列|controller&clear|
|period|更新任务执行周期|controller&period&20|

注： 控制器命令目前由`./tests/testListenSer.py`代为执行
 
### 版本目前存在问题
1. 任务队列中只能存在一条任务

