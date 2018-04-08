# opencps-agent

新版本 智能体版本

### 迭代历史
##### 2018-3-21  

1. 完成智能体单元模块

##### 2018-3-22

1. 添加任务循环监听处理模块
2. 更改一些智能体单元模块bug

##### 2018-3-23

1. 完成控制器基本通信模块

##### 2018-3-25

1. 在docker上测试代码（存在bug未修复）
2. 已知问题：dht11的数据类型比较奇怪，需要进行额外处理，需要相应修改workProcess代码

##### 2018-3-26
1. 完成在Docker上的第一版代码测试（已修复BUG）
2. 搭建了一套完整的本地测试系统（包括dht102和switch104）
3. 搭建同时执行多条任务代码
4. 设计多条件输入的执行逻辑

##### 2018-3-27
1. 输入与输出分别存储，并做简单映射关系。
2. 实现将控制信息转存至input和output列表中

##### 2018-4-7
1. 构建服务器后台核心代码框架,需要安装Flask Module

##### 2018-4-8
1. 完成单链表结构的代码生产
2. 完成多链表并行结构代码的功能（明日计划)
## 版本说明

智能体虚拟化模块主要有两大功能

1. 监听控制器的配置请求
2. 监听其他传感器的控制请求

### 目前智能体支持的控制命令
|控制命令|说明|范例|
|--------|----|----|
|add|添加一条任务|controller&add&>30;192.168.1.1:3000:off:2&20|
|clear|清空任务队列|controller&clear|
|period|更新任务执行周期|controller&period&20|
|show|查看任务队列中项目|controller&show&0|

注： 控制器命令目前由`./tests/testListenSer.py`代为执行
 
### 版本目前存在问题
1. 任务队列中只能存在一条任务 (已解决)
2.  
### 未来要支持的功能

控制器：

1. 任务队列的异常发现与处理功能
2. 控制命令支持本地命令，eg:sleep, 查询本体数据，等等

### 使用说明

|传感器名称| 映射端口 |
|----------|----------|
|dht102|33333|
|switch104|33334|
|switch103|33335|

程序范例:

当温度大于30时，启动switch104,10s后启动switch103

```
python3 testListenSer.py 33333 "controller&add&>30;192.168.12.19.3000:on:2&20"
python3 testListenSer.py 33333 "controller&add&<30;192.168.12.19:33335:on:2&0"
```

清空任务队列

```
python3 testListenSer.py 33333 "controller&clear"
```


