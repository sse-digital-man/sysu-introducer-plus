# 中大介绍官 Plus

在 2022 年中山大学软件工程学院的三下乡实践活动中，实践团队利用大语言模型、文本转语音和虚幻引擎等技术，推迟数字人 1.0 版本，为丰阳镇电商中心打造一个“24 小时直播间”，提供全天候的善品介绍和产品展示

如今，正值中山大学百年校庆，为了将新时代的信息技术与中大百年悠久的历史相结合，
我们项目团队延用数字人 1.0 的系统架构和技术实现，推出中大介绍官的虚拟数字人。

## 项目架构

![项目架构](./img/basic_structure.svg)

## 使用说明

1. 使用 `pip install -r requirements.txt` 安装项目依赖
2. 复制`config.example.json`到`config.json`（仍在项目根目录中），并按照需求配置其相关文件。
3. **保证工作路径在项目根目录**，通过`src/run_server.py`/`src/run_cli.py` 运行本程序

    > 前者是运行 Web Server，后者则是通过命令行的方式运行。

> 本项目中的所有相对路径都是根据项目的根目录 `sysu-introducer-plus`。

## 开发说明

本项目的所有开发文档托管在[Gitbook](https://fucloud.gitbook.io/sysu-introducer)上。

### 代码规范

为了提高本项目代码的规范性，我们引入静态分析的工具。请按照要求按照如下插件。
本项目已经配置好插件的相关设置，在`.vscode/settings.json`中。

-   [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint): Python 静态分析工具
-   [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8): Flake8 静态分析支持
-   [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter): Python 代码格式化工具

插件安装完成之后，请注意解决它们提示的警告和错误。

> 目前仓库中的代码已经基本符合上述规范。
