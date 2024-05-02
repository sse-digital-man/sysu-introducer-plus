# 开发文档

## 文件介绍

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

## 目录

-   [架构介绍](./structure.md)
-   [配置文件](./config.md)
-   [控制器](./controller.md)
-   模块：
    -   [大语言模型](./module/bot.md)
    -   [直播爬虫](./module/crawler.md)
