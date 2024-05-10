# 中大介绍官 Plus

## 使用说明

1. 使用 `pip install -r requirements.txt` 安装项目依赖
2. 复制`config.example.json`到`config.json`（仍在项目根目录中），并按照需求配置其相关文件。
3. **保证工作路径在项目根目录**，通过`src/app.py`/`src/cli.py` 运行本程序

    > 前者是运行 Web Server，后者则是通过命令行的方式运行。
    > 目前仅提供命令行的运行方式。

> 本项目中的所有相对路径都是根据项目的根目录 `sysu-introducer-plus`。

## 文件结构

```lua
.
├── docs
└── src
    ├── core
    │   ├── msg_queue   -- 消息队列
    │   └── basic_core  -- 实现最基础的内核
    ├── module
    │   ├── bot         -- LLM 模块
    │   ├── tts         -- TTS 模块
    │   ├── crawler     -- 直播监听 接口
    │   └── view        -- View 接口
    ├── utils
    │   └── config      -- 配置文件
    ├── booter.py       -- 引导程序
    ├── app.py          -- Webui 控制器
    └── cli.py          -- cli 控制器
```

## 项目架构

本系统本质上是将各种技术的有机结合，并且在具体实现上，
也通过分层、模块化等思想，保证系统中整体的可维护性和可拓展性。
此外，我们也提供 cli 和 webui 等方式对数字进行控制。

### 1. Core

`Core` 是消息的处理核心，
其中 `Handler` 会从 `Dynamic Message Queue`中获取消息，
并通过 `LLM` 和 `TTS` 模块生成对应回答和语音。
`Dynamic Message Queue` 会存储 `Booter` 传递过来的消息，
然后根据重要性指标来对各个消息进行优先级排序，
这样就更加充分地利用到了数字人回答问题的机会。

消息队列的设计，能让 `Handler` 异步处理消息，
将生产和处理两个步骤进行分离，从而降低了系统的耦合度。

### 2. Booter

`Booter` 属于组织模块，
它作为一条纽带串联了处理核心，和与外部交互的模块。
此外，它也决定了整个系统的生命周期。
当管理员通过 `Controller` 向其发送了起停指令，
这时 `Booter` 则需要控制整个系统的开启与结束。

![basic_structure](./docs/img/basic_structure.svg)

## 开发文档

开发文档请见[此处](https://fucloud.gitbook.io/sysu-introducer)。
