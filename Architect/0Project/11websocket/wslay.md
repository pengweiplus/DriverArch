# wslay 详解
&nbsp;&nbsp;&nbsp;&nbsp;wslay是一个是以C语言实现的websocket开发库，提供基于事件API和基于帧的底层API，非阻塞式（函数回调）；只支持websocket协议的数据传输部分，不执行http的握手过程。

## queue队列
> queue主要是通过一个双向链表来是管理数据，提供了new、free、pop、push、push_front、top、tail、empty等方法。
> ### 数据结构
> ```c
> ///< 单向列表
> struct wslay_queue_cell {
> 	void *data;
> 	struct wslay_queue_cell *next;
> };
> ///< 队列
> struct wslay_queue {
>	struct wslay_queue_cell *top;
>	struct wslay_queue_cell *tail;
>};
> ```
> ### 方法
> * new 实例化队列
> ```c
> ///< 从内存中实例化一个队列，并初始化
> struct wslay_queue *wslay_queue_new(void)
> {
>   struct wslay_queue *queue = (struct wslay_queue *)malloc(sizeof(struct wslay_queue));
>   if (!queue) {
> 	    return NULL;
>   }
>   queue->top = queue->tail = NULL;
>   return queue;
> }
> 
>  ```
> 
> * free 释放队列
> ```c
> ///< 释放队列中所有元素，并最终释放掉队列
> void wslay_queue_free(struct wslay_queue *queue)
> {
>   if (!queue) {
> 	    return;
>   } else {
> 	    struct wslay_queue_cell *p = queue->top;
> 	    while (p) {
> 		    struct wslay_queue_cell *next = p->next;
> 		    free(p);
> 		    p = next;
> 	}
> 	free(queue);
> }
> 
>  ```
> ```c
> ///< 添加一个元素到指定队列末尾，如果队列为空则添加到队首 
> int wslay_queue_push(struct wslay_queue *queue, void *data);
> 
> ///< 添加一个元素到指定队列队首
> int wslay_queue_push_front(struct wslay_queue *queue, void *data);
> 
> ///< 弹出指定队列队首元素
> void wslay_queue_pop(struct wslay_queue *queue);
> 
> ///< 返回指定队列队首元素
> void *wslay_queue_top(struct wslay_queue *queue)；
> 
> ///< 弹出指定队列队尾元素
> void *wslay_queue_tail(struct wslay_queue *queue)；
> 
> ///< 快速释放队列（将队列头标记为空）
> int wslay_queue_empty(struct wslay_queue *queue)
> ```

## stack堆
> stack堆主要通过一个单向链表来管理数据，提供了new、free、push、pop、top、empty等方法。
> ### 数据结构
> ```c
>///< 堆元素
> struct wslay_stack_cell {
>	void *data;
>	struct wslay_stack_cell *next;
>};
>
>///< 堆
> struct wslay_stack {
>	struct wslay_stack_cell *top;
>};
> ```
> ### 方法
> ```c
> ///< 实例化一个堆，并初始化为空
> struct wslay_stack *wslay_stack_new();
> 
> ///< 释放掉指定堆的所有元素
> void wslay_stack_free(struct wslay_stack *stack)；
> 
> ///< 向指定堆压入一个元素
> int wslay_stack_push(struct wslay_stack *stack, void *data)；
> 
> ///< 从指定堆中弹出一个元素
> void wslay_stack_pop(struct wslay_stack *stack)
> 
> ///< 从指定堆中返回堆首元素
> void *wslay_stack_top(struct wslay_stack *stack)；
> 
> ///< 快速释放堆（将堆首元素标记为空）
> int wslay_stack_empty(struct wslay_stack *stack)；
> 
> ```
## frame帧
> frame帧主要是对websocket协议传输的报文及其过程数据进行管理，提供了frame_context_init、frame_context_free、frame_send、frame_recv、frame_shift_ibuf等方法
> ### 数据结构
> ```c
> struct wslay_frame_context {
> ///< 接收过程数据
> 	uint8_t ibuf[4096];
> 	uint8_t *ibufmark;
> 	uint8_t *ibuflimit;
> 	struct wslay_frame_opcode_memo iom;
> 	uint64_t ipayloadlen;
> 	uint64_t ipayloadoff;
> 	uint8_t imask;
> 	uint8_t imaskkey[4];
> 	enum wslay_frame_state istate;
> 	size_t ireqread;
> ///< 发送过程数据 
> 	uint8_t oheader[14];
> 	uint8_t *oheadermark;
> 	uint8_t *oheaderlimit;
> 	uint64_t opayloadlen;
> 	uint64_t opayloadoff;
> 	uint8_t omask;
> 	uint8_t omaskkey[4];
> 	enum wslay_frame_state ostate;
> ///< 回调函数及用户数据指针
> 	struct wslay_frame_callbacks callbacks;
> 	void *user_data;
> };
> ///< 回调函数（发送、接收、标记）
> struct wslay_frame_callbacks {
>	wslay_frame_send_callback send_callback;
>	wslay_frame_recv_callback recv_callback;
>	wslay_frame_genmask_callback genmask_callback;
>};
> ``` 
> ### 方法
> * 
> ```c
> ///< 实例化一个frame_context上下文
> ///< 初始化接收状态：RECV_HEADER1
> ///< 初始化发送状态：PREP_HEADER
> ///< 初始化回调函数
> int wslay_frame_context_init(wslay_frame_context_ptr *ctx, const struct wslay_frame_callbacks *callbacks, void *user_data);
> 
> ///< 释放frame_context上下文
> void wslay_frame_context_free(wslay_frame_context_ptr ctx)
> ```
