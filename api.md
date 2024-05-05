# SUAIM API文档

## 1. 库（Database）

### 1.1 连接或创建数据库
`POST /api/connect/{db_path}`  
连接到一个已存在的数据库，或者创建一个新的数据库。  

**参数**  
- db_path: 数据库的路径

**返回**  
- db_path: 返回连接或创建的数据库路径

### 1.2 获取所有表
`GET /api/get/{db_path}/table_all`  
获取数据库中所有表的列表。

**参数**  
- db_path: 数据库的路径

**返回**  
- 所有表的列表

## 2. 表（Table）

### 2.1 连接或创建表
`GET /api/connect/{db_path}/{db_table}`  
连接到一个已存在的表，或者创建一个新的表。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称

**返回**  
- 表中所有数据的列表

### 2.2 删除表
`DELETE /api/delete/{db_path}/{db_table}`  
删除指定的表。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称

**返回**  
- 成功消息

### 2.3 重命名表
`POST /api/rename/{db_path}/table`  
重命名指定的表。

**参数**  
- old_name: 旧表名  
- new_name: 新表名

**返回**  
- 重命名结果

## 3. 物品（Item）

### 3.1 获取物品信息
`GET /api/get/{db_path}/{db_table}/{item_id}`  
根据物品ID获取物品的详细信息。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- item_id: 物品的ID

**返回**  
- 物品的详细信息

### 3.2 创建新物品
`POST /api/create/{db_path}/{db_table}/item`  
在表中创建一个新的物品。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- name: 物品名称  
- type: 物品类型  
- quantity: 数量  
- ascription: 归属  
- tag (可选): 标签  
- price (可选): 价格  
- consumables (可选): 消耗品  
- remark (可选): 备注

**返回**  
- 创建成功消息及物品ID

### 3.3 删除物品
`DELETE /api/delete/{db_path}/{db_table}/{db_id}`  
删除指定的物品。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID

**返回**  
- 成功消息

### 3.4 修改物品
`POST /api/update/{db_path}/{db_table}/{db_id}`  
更新指定物品的信息。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID  
- column_name: 要更新的列名  
- data: 更新的数据

**返回**  
- 更新后的物品信息

## 4. 二维码（QRCode）

### 4.1 获取二维码
`GET /api/get/{db_path}/{db_table}/{db_id}/qrcode`  
生成并获取物品的二维码。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID

**返回**  
- 二维码图片

### 4.2 创建并打印标签
`POST /api/get/{db_path}/{db_table}/{db_id}/print_label`  
创建物品的二维码，并打印物品标签。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID  
- text: 标签上的文本

**返回**  
- 打印标签的图片

### 4.3 简单打印标签
`GET /api/print_label/{db_path}/{db_table}/{db_id}`  
快速调用打印机打印物品标签。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID

**返回**  
- 成功消息