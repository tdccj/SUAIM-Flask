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
#### `v0.1.1-7`
- 优化 DBX init log
- 优化 Execute log 输出格式
- 删除 DBX delete_table 的旧代码
- DBX rename_table 成功应用 Execute
#### `v0.1.1-8`
- 删除 DBX rename_table 的旧代码
- 将 api_table get_all_item 迁移到 api_item
#### `v0.1.1-9`
- 删除 api_table 中的弃用方法的代码，包括 get_all_name 和 get_all_data
- DBX 中的表级操作已基本重构完成，api_table 适配业已基本完成
- 下个版本将开始在 DBX 中重构 api_item 使用的 项级操作
#### `v0.1.1-10`
- **DBX 将使用多继承模块化开发，和 api 对应，但仍然只有一个主类**
- **已将 Table 从 DBX 中剥离为父类模块之一，DBX 功能性和接口均不变**
#### `v0.1.1-11`
- 删除 Table 多余的依赖
- 将 api_database get_table_all 迁移至api_table
- 修改 api 中含有 get_all一类方法 的 url 连接为后缀添加 `/all` 的格式
#### `v0.1.1-12`
- 修改 DBX 初始化变量名，添加 db_name 中间变量用于传递给父类，功能保持不变
- DBX 已继承 Item
- 为 Execute.execute 添加 fetchall 选项，用于返回查询数据，开发中
- 创建 judgeFetchall 函数辅助 fetchall
#### `v0.1.1-13`
- 修改 judgeFetchall 为 私有函数
- 定义 Response 类用于传参
- 完成 judgeFetchall 有待测试
#### `v0.1.1-14`
- **为了项目的可持续性发展，将开源协议更改为更为宽松的 Apache License Version 2.0**
- 对于依赖的协议声明有待完善
#### `v0.1.1-15`
- 修改 judgeFetchall 函数为 judge_fetchall 符合命名规则
- 修复 judge_fetchall `fetchall==True` 时，返回 None 的问题
- 完成 Table get_table_all 方法
#### `v0.1.1-16`
- 修改 api_table 中的方法为 Ee标准返回(Execute.execute) 直接调用返回
- 为 Execute.execute 添加 enable 参数
  - 使用 `enable = False` 将函数用作标准返回格式化
  - 需要传入 `query = ""`，以避免出现异常
- 为 DBX 添加 result 方法，用以给 connect_database 实现 Ee标准输出
- 修改 api_database 中的方法为 Ee标准返回 直接调用返回
- API 文档更新 Ee标准返回
- 为 Table rename_table 添加 already exists 消息返回
- 修复 Execute.execute 中有关于 ignores 循环的逻辑错误
- 在 README 中添加如下信息：
  - 项目所使用字体开源协议信息，及其版权归属信息
  - 项目所使用依赖开源协议信息
- 修改部分 README 描述和结构
#### `v0.1.1-17`
- 创建 Query 类 为 Execute.execute 添加 query 的 values: tuple 支持
  - 用以传入查询附加参数，防止 sql 注入
- 修改 Ignore 传入参数 name 为 feature，更加便于理解
- 为 Execute.execute 添加新判断，防止 fetchall 返回 None
- 完成 Item get_item_data
- api get_item_data 已应用 DBX
#### `v0.1.1-18`
- 修复由于引号造成的 get_item_data 问题
- 完成 Item create_item
- 删除 Item 中的多余依赖
- api create_item 已应用 DBX
#### `v0.1.1-19`
- 为标准表添加新的 'show' 字段，用于控制显示和标记删除
- 完成 Item delete_item 并默认为标记删除，而不是实质删除
- 修复了一些自然语法错误
- 理论上 sqlite3 默认自动提交，但依旧提供commit选项，可以用于区分查询和增删改
- api delete_item 尚未应用 DBX
#### `v0.1.1-20`
- Execute.execute 传入参数 ignores 修改为 ignore_list
- 完成 Item update_item ，并为其添加是否存的判断条件
- api update_item 尚未应用 DBX
#### `v0.1.1-21`
- 修改 Item delete_item 中的 SQL 不安全行为
- 完成 Item get_items ，为其添加 limit 截取选项，用于限制数据量
  - 并替代原 get_all_items 的全部功能
- 将 Item ItemData 迁移至 Execute
- 在 Execute 中添加 Limit 用于标准化传入 limit 截取范围
- 新建并完成 Item count_item ，用于统计总项数
#### `v0.1.1-22`
- 为 DBX 添加数据库关闭方法的调用
- api get_table_all 已应用 DBX
- api delete_item 已应用 DBX , 并兼容 POST
- 为 logger 添加传入类型指定，增强安全性
- 修改 Execute 描述，使其职能范围更符合
- 为 Execute 添加 ApiExecute 用于 api 的 log 装饰器
- 为 api index() 和 api database 应用 ApiExecute
#### `v0.1.1-23`
- 暂时删除所有 api 调用的 ApiExecute 装饰器，因为装饰器被多次调用
#### `v0.1.1-24`
- 重构 ApiExecute 为 ExeWrapper， 增加传入参数 name，提高泛用性
- 重构 ExeWrapper call 为 try_execute，以便继承 TryExecute
- 重构 Execute类 为 ExeTools 使其更符合命名规则
#### `v0.1.1-25`
- 删除 api table 中的多余引用
- api create_table 方法改为 POST
- 成功解决 ExeWrapper 的问题，并在 api 中成功调用为 try_execute
- api table 已应用 try_execute
#### `v0.1.1-26`
- 所有 api 已应用 try_execute
#### `v0.1.1-27`
- api update_item 已应用 DBX，并删除其二次查询功能
- 将 DBX get_items 的 limit 参数默认值改为0-100，仍支持传入None
- 重构 api get_item_all 为 get_items
- DB 相关 api 已全部应用 DBX，有待测试
#### `v0.1.1-28`
- 为 database.py 添加说明，最早将在 v0.2版本被废弃
- 为 DBX 添加了一些可能没有实际意义的commit
- 修改了 Table create_table sql 语句中的一个 bug ，该 bug 导致无法创建表
- **强制数据库后缀名为.db**，若不是则自动添加
- 删除 README 过时的注意事项 
#### `v0.1.1-29`
- 添加表 db_info，用以实现版本验证、登录验证等功能
- 添加部分 database 管理方法
- 添加 DBInfo 有待迁移管理方法
- 为 DBX create_table 添加可选参数 customize=Query ，用于自定义表
- 现在 DBX 关闭时会自动提交一次
- 在 Table 中创建 get_table_info 方法
- DBX create_item 的传入数据兼容 dict，用于自定义项
#### `v0.1.1-30`
- **将 DBX 的子模块由继承改为调用模式，以实现二级封装**
#### `v0.1.1-31`
- todo 为 DBX 增加 管理最后一条 db_info 的能力
- todo 使用信息表实现隐藏表和软删除功能
- todo 从 connect_database 拆分出 create_database 方法