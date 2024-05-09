# SUAIM溯物-Flask服务端
Small-Scale Universal Asset/Inventory Management 泛用小型资产/库存管理系统<br>

> 旧的旅途尚未结束，新的征程已经开始。  
> 这次 SUAIM 将引入 Vue3 作为前端开发框架，并对 Flask 后端进行一定程度的重构。  


## 开源信息

### 本项目使用的开源协议：Apache License Version 2.0
- Apache License Version 2.0 开源协议见 `LICENSE`
### 本项目部分或全部使用： HarmonyOS Sans 开源字体
- HarmonyOS Sans 开源协议见 `font/HarmonyOS_Sans_SC/LICENSE.txt`
- HarmonyOS Sans 字体版权所有 © 2021 华为设备有限公司，根据 HarmonyOS Sans 字体许可协议使用。
### 本项目主要基于：Python3.10、Flask 和 sqlite3
- Flask 使用 [BSD-3-Clause license](https://github.com/pallets/flask/#BSD-3-Clause-1-ov-file)
- Python 及其内置库 sqlite3 使用 [PSF 开源许可协议](https://github.com/python/cpython/blob/3.12/LICENSE)
- 详细依赖见 `requirements.txt`

## 背景
> 现有的大型资产/库存管理系统多为ERP/WMS系统的子模块，而小型（应用于个人/小团队）的资产/库存管理系统，多为操作重复且封闭的各种小程序，难以二次开发。

- ERP/WMS系统
    - 部署复杂
    - 功能繁多，库存管理针对性不强
    - 强调过程/进度，而不是结果
- 小程序
    - 难以二次开发
    - 支持平台少
    - 无法自托管
- IT/实验室等资产管理系统
    - 泛用性不强
    - 对某一专业针对性太强
    - 难以二次开发/功能固化
## 目标
> 打造一款开源、轻量级、自托管、支持docker部署、泛用性强、开发便利且拥有多平台终端的现代化小型库存/资产管理系统。  
> 
> 初期尽量采用现成框架，实现基础框架，具备开源、较轻量级、自托管、手机扫码出入库管理等特性。  
> 
> 逐步实现高拓展性、多平台终端、现代化ui、docker部署。  
> 尽量缩短出入库流程，降低重复操作。  
> 
> - 后端采用Python+Flask+SQLite数据库  
> - ~~前端采用Dart+Flutter多端开发~~  
> - 前端采用Vue3+Element-Plus开发  
> - 备选Django框架+h5开发  


## 关键事项

- 基础框架构建
- 数据库接口开发
- 逻辑开发
- 调用开源ocr和识别码生成库

## 框架
- 服务端
    - 客户端后端（待定）
    - 服务器后端（可选）
        - python——flask
- 客户端
    - Web 客户端
        - vue3
    - Windows 客户端
        - flutter
    - 安卓客户端
        - flutter

## 注意事项
> Database、table名字务必用英文，否则可能会出现问题。<br>
> 
> 数据库最好放在程序目录（源目录）下。<br>
> 
## 另
> - 因为技术有限，开发缓慢，目标难以定期定量完成，欢迎加入开发  
> - 原[SUAIM-Flutter客户端](https://github.com/tdccj/SUAIM-Flutter)已经搁置，正在开发Vue新客户端


