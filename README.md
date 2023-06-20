# SUAIM溯物-Flaks后端
Small-Scale Universal Asset/Inventory Management 泛用小型资产/库存管理系统<br>
[SUAIM-Flutter前端](https://github.com/tdccj/SUAIM-Flutter)

## 背景
> 现有的大型资产/库存管理系统多为ERP/WMS系统的子模块，而小型（应用于个人/小团队）的资产/库存管理系统多为操作重复且封闭的各种小程序

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
> 打造一款开源、轻量级、自托管、支持docker部署、泛用性强、开发便利且拥有多平台终端的现代化小型库存/资产管理系统
> 初期尽量采用现成框架，实现基础框架，具备开源、较轻量级、自托管、手机扫码出入库管理等特性
> 逐步实现高拓展性、多平台终端、现代化ui、docker部署
> 尽量缩短出入库流程，降低重复操作
> 后端采用Python+Flaks+SQLite数据库
> 前端采用Dart+Flutter多端开发
> 备选Django框架+h5开发


## 关键事项

- 基础框架构建
- 数据库接口开发
- 逻辑开发
- 调用开源ocr和识别码生成库

## 注意事项
> Database、table名字务必用英文，否则可能会出现问题<br>
> 数据库最好放在程序目录下（源目录）
## 另
> 因为技术有限，开发缓慢，目标难以定期定量完成，如果你也需要这么一款开源自托管管理系统，欢迎加入开发


