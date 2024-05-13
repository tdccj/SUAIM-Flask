# SUAIM API文档

## 前言

 SUAIM-溯物 的大部分标准 API 将采用由 `src/Execute.execute( )` 函数定义的 Ee 标准返回。



**> 使用 Ee 标准化返回的 API 将有 _返回 Ee_ 字样：**
- 由于状态几乎固定， API 文档中返回内容默认为 `message` 加可选 `result`的示例或描述。


- API 文档中可能表述 `message` 返回的几种情况，服务器将视情况返回对应 `message`

 
 **> 其主要由两对必要键值对和一对可选键值对组成，分别为：**
 - `status`：状态，用于指示执行结果。

 
 - `message`：执行结果消息。
 
 
 - `result`：有数据返回时将会增加可选的 result 键值对，用以返回数据。
 
**> 其中 `status` 有以下状态：**
- `success`: 执行成功。
 

- `failed`: 执行失败。



**\* 状态为 `failed` 时，将不会返回 `result`。** 这将强制前端校验是否执行成功。


## 1. 库（Database）

### 1.1 连接或创建数据库
`GET /api/connect/{db_path}`  
连接到一个已存在的数据库，或者创建一个新的数据库。  

**参数**  
- db_path: 数据库的路径

**返回  
Ee message:**
- `Get database '{db_name}' connect result [successfully|failed]`


## 2. 表（Table）

### 2.1 连接或创建表
`GET /api/create/{db_path}/{db_table}`  
连接到一个已存在的表，或者创建一个新的表。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称

**返回   
Ee message:**
- `Create table '{table_name}' [successfully|failed]`  
- 表单已存在 `Table '{table_name}' is already exists`

### 2.2 删除表
`DELETE /api/delete/{db_path}/{db_table}`  
删除指定的表。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称

**返回   
Ee message:**
- `Delete table '{table_name}' [successfully|failed]`  
- 表单不存在 `Table '{table_name}' is not exists`

### 2.3 重命名表
`POST /api/rename/{db_path}/table`  
重命名指定的表。

**参数**  
- old_name: 旧表名  
- new_name: 新表名

**返回   
Ee message:**
- `Rename table '{old_name}' to '{new_name}' [successfully|failed]`
- 旧表单不存在 `Table '{old_name}' is not exists`
- 新表单已存在 `Table '{new_name}' is already exists`

### 2.4 获取所有表
`GET /api/get/{db_path}/all`  
获取数据库中所有表的列表。

**参数**  
- db_path: 数据库的路径

**返回   
Ee message:**
- `Get all tables from '{db_name}' [successfully|failed]`  

**Ee result:**
- `[('{table_name}',),...]`




## 3. 物品（Item）

### 3.1 获取物品信息
`GET /api/get/{db_path}/{db_table}/{item_id}`  
根据物品ID获取物品的详细信息。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- item_id: 物品的ID

**返回**  
- `{'status': 'success', "data": item_info, 'def': 'get_item_data'}`

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
- consumables (可选): 是否为消耗品  
- remark (可选): 备注

**返回**  
- `{'status': 'success', "id": row_id, 'def': 'create_item'}`

### 3.3 删除物品
`DELETE /api/delete/{db_path}/{db_table}/{db_id}`  
删除指定的物品。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID

**返回**  
- `{'status': 'success', "id": row_id, 'def': 'delete_item'}`

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
- `{'status': 'success', "item": str(item), 'def': 'update_item'}`

### 3.5 获取表中的所有 item
`GET /api/get/{db_path}/{db_table}/all`  
连接到一个已存在的表，或者创建一个新的表。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称

**返回**  
- `{'status': "success", "columns": columns,
    "data": all_data, 'def': 'get_all_item'}`

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
> 在使用此 api 前，请确保服务器连接且能正常访问受支持的打印机。  
> 该特性可能会被移除，改为客户端执行。

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
> 在使用此 api 前，请确保服务器连接且能正常访问受支持的打印机。  
> 该特性可能会被移除，改为客户端执行。

`GET /api/print_label/{db_path}/{db_table}/{db_id}`  
快速调用打印机打印物品标签。

**参数**  
- db_path: 数据库的路径  
- db_table: 表的名称  
- db_id: 物品的ID

**返回**  
- `{'status': 'success', 'def': 'print_label_simple'}`
