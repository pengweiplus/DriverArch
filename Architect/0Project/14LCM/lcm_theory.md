# LCM(Lightweight Communication and Marshalling)
## 简介
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LCM旨在解决多进程间数据安全高效交换问题，消息（message）是整个通信的基本单元，是独立域编程语言之外的数据结构，通过lcm-gen编译为指定语言下的代码片段。</br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消息（message）通过通道（channel）进行传输，通道（channel）是以人为定义的字符串进行区分，同时约定在相同通道（channel）下的消息具备相同的消息类型。</br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LCM应用可以在任何通道（channel）发布消息，同样LCM应用可以订阅并接收任何通道（channel）的数据。

### 使用步骤
* 创建消息类型定义
* 在应用程序中初始化LCM
* 发布消息
* 订阅和接收消息

## 实现原理
### 数据结构
```c```
struct _lcm_t {
    GStaticRecMutex mutex;         // guards data structures
    GStaticRecMutex handle_mutex;  // only one thread allowed in lcm_handle at a time

    GPtrArray *handlers_all;   	// list containing *all* handlers
    GHashTable *handlers_map;	  // map of channel name (string) to GPtrArray
                                   // of matching handlers (lcm_subscription_t*)

    lcm_provider_vtable_t *vtable;
    lcm_provider_t *provider;

    int default_max_num_queued_messages;
    int in_handle;
};
``````
* lcm_provider_vtable_t *vtable,接口实现指针，lcm抽象了provider提供的接口（creat、destory、subscribe、unsubscribe、publish、handle、get_filno），支持udp、tcp、log、multicast、mem</br>
	* udpm_provider
		* create </br>
		根据参数hash表查询出所有参数，并保存至lcm对象</br>
		创建通知管道（notify pipe）</br>
        依据参数配置socket并测试连通性</br>
       ps:create的作用就是按照网络类型创建好环境（提前申请资源，如socket、mem、log等等）</br>
       
		* subscribe </br>
		依据参数配置socket并端口绑定，同时设置socket加入组播 </br>
        创建环形队列，用与消息缓存 </br>
        创建管道（pipe），用来通知主线程和接收线程间消息同步 </br>
        创建接收线程，阻塞接收订阅的消息，并缓存至环形队列 </br>
        
        * publish </br>
        按lcm消息格式填充sendbuf，在与通道（channel）、IP地址一起组装成msg
        调用系统sendmsg接口，将消息发送
        
		* handle </br>
		阻塞接收notify pipe传输的命令字节（只用一个字节）</br>
        获取消息队列信号量，并从队列中读出数据 </br>

	* logprov_provider
	* tcpq_provider
	* mpudpm_provider
	* memq_provider
	
* handler_map用来组织所有订阅该消息（message）的订阅进程的handler
* handler_all是一个链表
* mutex 信号量，用来保证任何是否只有一个线程操作（读取/写入）消息环形队列

### 函数接口
#### lcm_create
```c++```
lcm_t *lcm_create(const char *url)
{
#ifdef WIN32
    WSADATA wsd;
    int status = WSAStartup(MAKEWORD(2, 0), &wsd);
    if (status) {
        return NULL;
    }
#endif

	/*
 	* args,hash表，用来记录和保存url中的参数名称及其数值，例如“ttl=0”
 	* providers，list，用来记录lcm实例支持的provider，例如udpm、tcpq、log等等
 	*/
    char *provider_str = NULL;
    char *network = NULL;
    GHashTable *args = g_hash_table_new_full(g_str_hash, g_str_equal, free, free);
    GPtrArray *providers = g_ptr_array_new();
    lcm_t *lcm = NULL;

	/*
	 * 向providers list中添加支持
 	*/
    // initialize the list of providers
    lcm_udpm_provider_init(providers);
    lcm_logprov_provider_init(providers);
    lcm_tcpq_provider_init(providers);
    lcm_mpudpm_provider_init(providers);
    lcm_memq_provider_init(providers);
    if (providers->len == 0) {
        fprintf(stderr, "Error: no LCM providers found\n");
        goto fail;
    }
    
    /*
     * lcm_prase_url 从url中提取出网络类型、参数列表
     * 遍历providers找出匹配网络类型的provider
     */
    if (!url || !strlen(url))
        url = getenv("LCM_DEFAULT_URL");
    if (!url || !strlen(url))
        url = LCM_DEFAULT_URL;

    if (0 != lcm_parse_url(url, &provider_str, &network, args)) {
        fprintf(stderr, "%s:%d -- invalid URL [%s]\n", __FILE__, __LINE__, url);
        goto fail;
    }

    lcm_provider_info_t *info = NULL;
    /* Find a matching provider */
    for (unsigned int i = 0; i < providers->len; i++) {
        lcm_provider_info_t *pinfo = (lcm_provider_info_t *) g_ptr_array_index(providers, i);
        if (!strcmp(pinfo->name, provider_str)) {
            info = pinfo;
            break;
        }
    }
    if (!info) {
        fprintf(stderr, "Error: LCM provider \"%s\" not found\n", provider_str);
        g_ptr_array_free(providers, TRUE);
        free(provider_str);
        free(network);
        g_hash_table_destroy(args);
        return NULL;
    }

    /*
     * lcm实例初始化
     * 1.保存匹配网络的provider到vtable
     * 2.实例化handlers_all和handler_map
     * 3.调用provider的creat接口实例化一个provider并保存至lcm实例
     */
    lcm = (lcm_t *) calloc(1, sizeof(lcm_t));

    lcm->vtable = info->vtable;
    lcm->handlers_all = g_ptr_array_new();
    lcm->handlers_map = g_hash_table_new(g_str_hash, g_str_equal);

    g_static_rec_mutex_init(&lcm->mutex);
    g_static_rec_mutex_init(&lcm->handle_mutex);

    lcm->provider = info->vtable->create(lcm, network, args);
    lcm->in_handle = 0;

    free(provider_str);
    free(network);
    g_ptr_array_free(providers, TRUE);
    g_hash_table_destroy(args);

    if (!lcm->provider) {
        lcm_destroy(lcm);
        return NULL;
    }

    lcm->default_max_num_queued_messages = 30;

    return lcm;

fail:
    free(provider_str);
    free(network);
    if (args)
        g_hash_table_destroy(args);
    if (providers)
        g_ptr_array_free(providers, TRUE);
    //    if (lcm)
    //        lcm_destroy (lcm);
    return NULL;
}

```
