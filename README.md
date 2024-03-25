# 中大介绍官 Plus

## 开发文档

-   外部接口
    -   直播爬虫：[live.md](./docs/interface/live.md)
-   内部模块：
    -   大语言模型：[llm.md](./docs/module/llm.md)

## 架构说明

本项目本质上是个大型的服务端，
管理员/运营人员可以通过 Webui 编写的 `Controller` 管理和控制数字人的启动和关闭。
在项目启动后，系统会 通过 `Live Interface` 获取直播间中的弹幕信息，
并存储在 `Dynamic Message Queue` 中，
等待 `Handler` 处理生成对应的文本与语音，
最后通过 `View Interface` 的方式发送到 UE5 或者 Unity 中，
以数字人的形象展现出来。

当然，在整体的架构设计上，
我们尽量通过分层的方式减少整个系统中各个组件之间的耦合度。

![basic_structure](./docs/img/basic_structure.svg)

### 1. Booter

`Booter` 本身不会处理很复杂的逻辑，
但它作为一条纽带串联了整个系统中的各个组件。
比如说，它能将管理员发送的消息/信号，
以及直播间观众发送的弹幕信息转交给 `Core`进行处理，
然后将其处理的结果传递给`View Interface`。

此外，它也决定了整个系统的生命周期。
当管理员通过 `Controller` 向其发送了起停指令，
这时 `Booter` 则需要控制各个组件的开启与结束。

### 2. Core

`Core` 是消息的处理核心，
其中 `Handler` 会从 `Dynamic Message Queue`中获取消息，
并通过 `LLM` 和 `TTS` 模块生成对应回答和语音。
`Dynamic Message Queue` 会存储 `Booter` 传递过来的消息，
然后根据重要性指标来对各个消息进行优先级排序，
这样就更加充分地利用到了数字人回答问题的机会。

消息队列的设计，能让 `Handler` 异步处理消息，
将生产和处理两个步骤进行分离，大大地降低了系统的耦合度。

### 3. Message

再系统中，需要处理的消息可以分为以下三类。
当然，前两种消息类型的性质是相同，都是一些文本内容，
只不过是说来自管理员的消息可能会比观众的优先级更高。
而对于信号而言，不是具体的文本，而是一种抽象的动作，
比如说让数字人打招呼，介绍自己等，
它存在固定的逻辑去处理，效果和目的是更直接的。

1. Admin: 来自管理员的消息
2. Watcher: 来自直播间观众的消息
3. Signal: 来自管理员的信号

### 4. Else

-   `Live Interface`: 该接口主要是通过网络爬虫或者说是开放接口的方式获取直播平台上的弹幕消息。

    目前本项目仅支持 `Bilibili` 平台。

-   `View Interface`: `Core`处理的结果会通过该接口传递给 UE5 或 Unity。
