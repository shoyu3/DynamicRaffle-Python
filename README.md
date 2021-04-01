# DynamicRaffle-Python
哔哩哔哩动态抽奖工具，项目开始于2021年3月16日

[![version](https://img.shields.io/github/v/release/shoyu3/DynamicRaffle-Python.svg?label=最新版本)](https://github.com/shoyu3/DynamicRaffle-Python/releases)
[![Issue](https://img.shields.io/github/issues/shoyu3/DynamicRaffle-Python.svg?label=Issues)](https://github.com/shoyu3/DynamicRaffle-Python/issues)
[![Language](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87-brightgreen.svg)](#)
[![DevLanguage](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E8%AF%AD%E8%A8%80-Python-brightgreen.svg)](#)
[![GitHub license](https://img.shields.io/github/license/shoyu3/DynamicRaffle-Python.svg?label=许可证)](https://github.com/LeoChen98/BiliRaffle/blob/master/LICENSE)


## 部分功能截图

最新版本（1.1.0）：

![image](https://user-images.githubusercontent.com/75879378/113187997-17f5e600-928c-11eb-94a1-61d03f978f0f.png)

旧版本（1.0.5）：

![截图1](https://user-images.githubusercontent.com/75879378/112523063-4fbae480-8dd9-11eb-879b-3d9a4182fc12.png)

某个旧版：

![截图2](https://user-images.githubusercontent.com/75879378/112303896-cd96c700-8cd7-11eb-9a5a-0de24521d512.png)

部分实现方法源自项目：https://github.com/LeoChen98/BiliRaffle

## 如何使用

前往[本项目最新的Release](https://github.com/shoyu3/DynamicRaffle-Python/releases/latest)，点击文件列表中的RaffleGUI.exe文件下载，双击运行

## 关于关注检测

检测关注需要登录自己的B站账号，在最近的版本里已经整合进了getcookie.exe的功能，另外还增加了注销cookie的选项，可以快速注销此次登录

芍芋建议如果不是很经常使用抽奖关注检测功能的话应该在使用完之后注销cookie，保护账号安全（当然就算不注销只要不对外泄露就不会出问题）

## 源码目录

- RaffleGUI.py 主程序
- icon.ico 窗口图标
- iconwin.py 包含窗口图标base64码的文件，打包exe需要使用
- icopyspawn.py 将当前目录下的icon.ico转换生成iconwin.py，更新图标时需要使用
