# DynamicRaffle-Python
哔哩哔哩动态抽奖工具，项目开始于2021年3月16日

[![version](https://img.shields.io/github/v/release/shoyu3/DynamicRaffle-Python.svg?label=最新版本)](https://github.com/shoyu3/DynamicRaffle-Python/releases)
[![Issue](https://img.shields.io/github/issues/shoyu3/DynamicRaffle-Python.svg?label=Issues)](https://github.com/shoyu3/DynamicRaffle-Python/issues)
[![Language](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87-brightgreen.svg)](#)
[![DevLanguage](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E8%AF%AD%E8%A8%80-Python-brightgreen.svg)](#)
[![GitHub license](https://img.shields.io/github/license/shoyu3/DynamicRaffle-Python.svg?label=开源许可)](https://github.com/shoyu3/DynamicRaffle-Python/blob/master/LICENSE)

## ⚠使用前必看

此工具无法突破B站对转发接口获取上限的限制（550条左右），因此将最高转发量设置为600，如想要抽奖的动态已经超出此指标，则建议改为在评论区抽

## 🧱工具截图

![image](https://user-images.githubusercontent.com/75879378/116866639-56d9db80-ac3e-11eb-951a-604d813dff42.png)

<!--
![image](https://user-images.githubusercontent.com/75879378/116789074-ad7cd380-aadf-11eb-890c-37c57a7c3aea.png)
最新版本（1.1.4）：
![图片](https://user-images.githubusercontent.com/75879378/115114829-d4a5b200-9fc3-11eb-915e-d662a2c55319.png)
旧版本（1.1.0）：
![image](https://user-images.githubusercontent.com/75879378/113187997-17f5e600-928c-11eb-94a1-61d03f978f0f.png)
旧版本（1.0.5）：
![截图1](https://user-images.githubusercontent.com/75879378/112523063-4fbae480-8dd9-11eb-879b-3d9a4182fc12.png)
某个旧版：
![截图2](https://user-images.githubusercontent.com/75879378/112303896-cd96c700-8cd7-11eb-9a5a-0de24521d512.png)
-->
部分实现方法和思路参考此项目：https://github.com/LeoChen98/BiliRaffle

## 🛠如何使用

**Windows平台（win10/win8）：**

前往[本项目最新的Release](https://github.com/shoyu3/DynamicRaffle-Python/releases/latest)，点击文件列表中的RaffleGUI.exe文件下载，双击运行

**Windows平台（win7，或无法直接运行exe的电脑）：**

下载python3安装包并安装（假设以前没有安装过，不能安装最新的3.9，推荐安装3.8），完成后在命令提示符（CMD）运行下面的命令：

```bash
pip install requests
pip install qrcode
pip install pyperclip
pip install Pillow
pip install Image
```

之后点击代码目录右上角的下载zip，解压，再在解压后的目录里按住```Shift```右键打开命令提示符输入```py RaffleGUI.py```并运行，或右键RaffleGUI.py，在菜单中选择“Edit with IDLE”，待窗口弹出后按键盘上的```F5```运行

**Windows平台（XP/Vista）：**

下载python3安装包并安装（假设以前没有安装过，不能安装3.5及以后的版本，推荐安装3.4），完成后在命令提示符（CMD）运行下面的命令：

```bash
pip install requests
```

之后点击代码目录右上角的下载zip，解压，由于本程序用到的部分库不支持python低版本，所以需要手动修改部分代码

右键RaffleGUI.py，在菜单中选择“Edit with IDLE”，待窗口弹出后在开头的以下两行代码前加“#”或直接删除对应代码：

```python
import qrcode
import pyperclip
```

修改完成后保存文件，按键盘上的```F5```运行

注意：按照此教程做完后，扫码登录和自动复制用户名两个功能将失效，其他功能不受影响

**Linux（Debian/Ubuntu/Deepin）平台：**

如果之前没有进行过相关配置，需要先在终端（Terminal）依次运行下列命令：（假设已自带python3，如果不是很确定直接运行也可以）

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo apt install python3-tk
pip3 install requests
pip3 install qrcode
pip3 install pyperclip
pip3 install Pillow
pip3 install Image
```

之后点击代码目录右上角的下载zip，解压，并在解压后的目录里打开终端输入```python3 RaffleGUI.py```后运行

注：如果已经安装wine可以尝试直接运行打包后的exe文件（但不建议这么做，wine直接运行存在部分兼容性问题）

**MacOS平台：**

下载python3安装包并安装（假设以前没有安装过，MacOS只自带了python2），完成后在终端（Terminal）运行下面的命令：<!--（如果提示找不到命令在每条的pip后面加一个3）-->

```bash
pip3 install requests
pip3 install qrcode
pip3 install pyperclip
pip3 install Pillow
pip3 install Image
```

之后点击代码目录右上角的下载zip，解压，再在解压后的目录里打开终端输入```python3 RaffleGUI.py```并运行

**Android平台（需要手机屏幕分辨率为1080P及以上）：**

在手机上下载并安装Pydroid3，打开，在侧边栏选择“终端（Terminal）”，输入下面的命令并运行：

```bash
pip install requests
pip install qrcode
pip install pyperclip
pip install Pillow
pip install Image
```

之后点击代码目录右上角的下载zip，解压到手机的任一目录，在Pydroid3中打开该目录下的RaffleGUIforPydroid.py，点击右下角悬浮按钮运行

注：安卓版可以直接在输入框粘贴从B站客户端分享页面复制的b23.tv短链，但因运行器限制自动复制用户名功能不可用（已屏蔽）

注2：安卓版更新频率极低（没精力同时维护和测试），最后一次更新版本是1.1.1.010（2021-4-3）

## 🧶关于关注检测

检测关注需要登录自己的B站账号，在最近的版本里已经整合进了getcookie.exe的功能，另外还增加了注销cookie的选项，可以快速注销此次登录

一般建议如果不是十分使用抽奖关注检测功能的话可以在使用完之后注销cookie，保护账号安全（当然就算不注销只要不对外泄露就不会有风险）

## ❤赞助开发者

☞[前往爱发电](https://afdian.net/@shoyu)

## ✔源码目录

- RaffleGUI.py 主程序
- RaffleGUIforPydroid.py 安卓平台主程序
- icon.ico 窗口图标
- iconwin.py 包含窗口图标base64码的文件，打包exe需要使用
- icopyspawn.py 将当前目录下的icon.ico转换生成iconwin.py，更新图标时需要使用
- rc4.py 加密解密cookie需要使用
