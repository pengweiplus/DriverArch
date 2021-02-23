# IP协议辅助技术
## DNS
&nbsp;&nbsp;&nbsp;&nbsp;DNS协议可以将字符串自动装换为具体的IP地址，不仅支持IPv4还支持IPv6.
## ARP
&nbsp;&nbsp;&nbsp;&nbsp;ARP协议是解决地址问题的协议。以目标IP地址为线索，用来定位下一个应该接收数据分包的网络设备对应的MAC地址。
> ### 工作机制
> &nbsp;&nbsp;&nbsp;&nbsp;借助ARP查询和ARP响应两种类型的包来确定MAC地址。通过广播ARP请求，来动态的进行解析
> ### 问题
> &nbsp;&nbsp;&nbsp;&nbsp;如果频繁的进行ARP请求，将造成不必要的网络流量，因此通常的做法是把获取到的MAC地址缓存一段时间。

## RARP
&nbsp;&nbsp;&nbsp;&nbsp;从MAC地址定位IP地址的一种协议，当设备无法通过DHCP动态获取IP地址或者没有输入接口时，可以通过架设一台RARP服务器，在这个服务器上注册设备的MAC地址和IP地址。

## 代理ARP
&nbsp;&nbsp;&nbsp;&nbsp;通常ARP包会被路由器隔离，但是采用代理ARP（Proxy ARP）的路由器可以将ARP请求发给临近的网段，由此两个以上的节点之间可以像在一个网段中一样通信。

## ICMP
> ### 辅助IP的ICMP
> &nbsp;&nbsp;&nbsp;&nbsp;主要功能包括，确认IP包是否成功送达目标地址，通知在发送过程中IP包被废弃的原因，改善网络设置等。
> 
> &nbsp;&nbsp;&nbsp;&nbsp;大致分为2类：一类是通知出错原因的错误消息，另一类是用于诊断的查询消息。
> * 目标不可达（3，）