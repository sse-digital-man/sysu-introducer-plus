# 简介

## 项目背景

在 2022 年中山大学软件工程学院的三下乡实践活动中，实践团队利用大语言模型、文本转语音和虚幻引擎等技术，推出数字人 1.0 版本，为丰阳镇电商中心打造一个“24 小时直播间”，提供全天候的善品介绍和产品展示

如今，正值中山大学百年校庆，为了将新时代的信息技术与中大百年悠久的历史相结合，
我们项目团队延用数字人 1.0 的系统架构和技术实现，推出中大介绍官的虚拟数字人。

## 项目架构

本系统的总体架构如下所示。

![总体架构图](./img/structure.svg)

## 项目亮点

### 1. 易用性

- 部署简单：本系统通过 Git 的 [Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) 和 [Docker](https://www.docker.com/) 等方式，尽可能减少和降低用户进行部署所需要时间和经理。
- 启动简单：本系统的各项功能，包括模块控制、Docker 控制、WebUI 控制器都集成在一起，只需一次运行，就能全盘启动。
- 交互简单：本系统提供 WebUI 的控制器，提供可视化的方式允许用户查看系统**运行状态**和**日志**。

### 2. 拓展性

由于**模块化**的系统框架，各个模块之间的耦合度极低。当用户需要增加新的模块实现实例时，他只需要关注如何实现即可，模块的创建和使用都会用系统框架处理，大大降低系统拓展的成本。

- 依赖关系：由 `modules.yaml` 注册
- 通信方式：由模块接口规定，同个模块的任何实现共用一套接口

### 3. 实用性

- 专业知识：人工搜集和整理中大相关的知识数据，并自建数据库，再结合 RAG 等方法思想，尽可能提高数字人回答问题的准确性。
- 弹幕筛选：动态消息队能够排序和筛选大量同时涌入的弹幕信息，获得当前时间内最具有回答价值的问题，从而减少了回答无用问题的可能，高效利用数字人回答问题的机会。
- 回答响应：通过引入**异步处理**的方式，数字人在说话时也可以思考下一个问题的答案，提高回答的响应速度。

## 相关链接

* 主代码仓库：[sysu-introducer-plus](https://github.com/sse-digital-man/sysu-introducer-plus)
* 控制器代码仓库：[sysu-introducer-controller](https://github.com/sse-digital-man/sysu-introducer-controller)
* 项目文档仓库：[sysu-introducer-wiki](https://github.com/sse-digital-man/sysu-introducer-wiki)
* 项目文档链接：[fucloud.gitbook.io](https://fucloud.gitbook.io/sysu-introducer)
