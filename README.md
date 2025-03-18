# Image Batch Processing Tools --AOSAI

## Introduction

This project demonstrates how to create a bilingual README file.

For the Chinese version of this README, see [README.zh-CN.md](README.zh-CN.md).

## 项目目录结构

```
image_tools_by_aosai/
├── main.py                # 程序主入口
├── app/                   # PyQt 界面相关
│   ├── __init__.py
│   ├── ui_main.py         # 主窗口 UI
│   └── components.py      # 其他自定义组件（如进度条、日志框）
├── crawler/               # 爬虫逻辑模块
│   ├── __init__.py
│   ├── downloader.py      # 图片下载逻辑
│   ├── parser.py          # HTML 解析逻辑
│   └── scheduler.py       # 下载调度管理
├── utils/                 # 工具模块
│   ├── __init__.py
│   ├── logger.py          # 日志工具
│   ├── file_utils.py      # 文件处理工具（如去重、重命名）
│   └── validators.py      # 输入验证工具
├── resources/             # 资源文件（如图标、默认配置）
│   ├── icon.png
│   └── default_config.json
├── functionTests/         # 单元测试
│   ├── test_downloader.py
│   ├── test_parser.py
│   └── test_utils.py
├── requirements.txt       # 依赖库
└── README.md              # 使用说明
```

#### 软件架构

- dist 打包后的文件位置

- src 开发模块

  - docs 日志，说明文档
  - fileProcessing 文件压缩解压模块
  - imageProcessing 图像批量处理模块
  - public 静态资源
  - Main 主函数入口

- gitignore
- LICENSE
- README.md

工具包中目前集成的功能有：

1. JPG 图片的批量压缩、批量调整分辨率、批量裁剪形状。
2. 文件的压缩解压。

#### 安装使用

- 开发者模式 master 分支

1.  开发环境我用的是 Anaconda3-2023.07-2-Windows-x86_64，[链接在此](https://docs.anaconda.com/free/anaconda/reference/packages/oldpkglists/)
2.  安装 Git，配置环境、账号密码、Gitee 的 SSH 密钥
3.  下载代码，用什么 IDE 打开都能运行

- 使用者模式 release 分支

还在摸索 QAQ

#### 虚拟环境

conda create -n [虚拟环境名字] Python==3.11.4
conda install pyqt==5.15.7
conda install pillow==9.4.0

#### 参与贡献
