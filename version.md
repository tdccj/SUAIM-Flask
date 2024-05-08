# SUAIM-溯物 版本日志
>从 2024/5/7 开始，SUAIM-溯物 将开始以版本号提交，并记录版本日志。

## version 0.1
- 以模块化重构上个时代的代码，使其更加现代化标准化。
- 尽量适配新的 Web 前端。
- 为大部分组件提供日志记录功能。
- 添加登录验证提高安全性。
### `v0.1.1`开发中
- 重构 Database 为 DatabaseX ，以期解决低可靠性问题，将提供 容错、验证、
备份、恢复、日志记录等功能。
#### `v0.1.1-1`
- 添加开发日志
- 逐步替换 api_database 中的 DB 类为 DBX
- 完成 DBX create_table
#### `v0.1.1-2`
- 考虑将 item 的删除改为标记删除和实质删除两种
- 完成 DBX delete_table
- 修改 DBX create_table 返回内容的语法和警告机制
- 将第一个日志文件加上了.log后缀，但是后续文件会出现两个log后缀
#### `v0.1.1-3`
- 创建 DBX rename_table
- 修正 log 中的字符串显示
#### `v0.1.1-4`
- 由于 DBX 中的异常处理过于繁琐，将部分操作整理为一个通用模块 Execute
- Execute 已创建，尚未完成，在测试逻辑
- Execute 传入 IgnoreList 忽略多个异常
#### `v0.1.1-5`
- Execute 基本完成
- DBX create_table 成功应用 Execute
#### `v0.1.1-6`
- 将 DBX 中的 Execute 引用移动到 init 中
- 去除 Execute 中多余的引号
- 删除 DBX create_table 的旧代码
- DBX delete_table 成功应用 Execute
