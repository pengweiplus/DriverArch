# 开源嵌入式项目
## 简介
文档记录了嵌入式软件开发过程中经常使用的开源项目、库，方便日常记录和查阅
## RTOS
## Components
### BootLoader
* [WolfBoot](https://www.wolfssl.com/products/wolfboot/)
<br> WolfBoot是一款针对32位微控制器开发的固件引导更新软件,支持SPI、UART接口通信。
* [OpenBLT](https://www.feaser.com/openblt/doku.php)
<br> OpenBLT是一款支持STM32、XMC4、XMC1、Tricore、HCS12等基于ARM CORTEX内核微控制器固件引导更新软件，支持RS-232、CAN、TCP/IP、USB接口通信以及SD-card更新。
### 文件及文件系统
* [smartFS](https://cwiki.apache.org/confluence/display/NUTTX/Using+SmartFS)
<br>smartFS是一个精简小巧的文件系统，支持NorFlash、NandFlash。
* [cJSON](https://formulae.brew.sh/formula/cjson)
<br> cJSON是一款用于资源受限环境下进行JSON文件解析库
* [JSMN](https://zserge.com/jsmn/)
<br> JSMN是一款用C编写的JSON文件解析库。
### IPC
* [LCM](http://lcm-proj.github.io/)
<br> Lightweight Communications and Marshalling (LCM)是一款强大的去中心化的实时高带宽、低延迟异步通信库，支持c、C++、C#、python的语言。
* [PSMQ](https://bitbucket.org/atlassian/psmq/src/master/)
<br> **p**ublish **s**subscribe **m**essage **q**ueue（PSMQ）是一种内部线程通信库，基于messag queue支持多点间通信。
* [uORB](https://docs.px4.io/master/en/middleware/uorb.html)
<br> uORB是一个针对内部线程或进程间的异步通信API。
### 网络
* [wslay](https://tatsuhiro-t.github.io/wslay/)
<br> wslay是一款基于RFC-6455由c编写的WebSocket库，Wslay仅仅支持数据传输，未实现HTTP协议层的握手逻辑。
* [CANopenNode](https://liberapay.com/CANopenNode)
<br> CANopenNode是一款开源且免费的CANopen协议栈。