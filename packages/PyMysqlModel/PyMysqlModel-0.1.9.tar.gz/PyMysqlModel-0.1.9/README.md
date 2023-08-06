# PyMysqlModel

#### 描述
基于 pymysql 的模型创建及使用 

内置 create、all、update、delete、filter、get 等常用方法

支持聚合查询、原生sql、子查询

安装

```python
pip install PyMysqlModel
```

更新

```python
pip install -U PyMysqlModel
```

**example 目录下为示例程序**



# 使用介绍

#### 连接数据库

```python
# database=None,
# user=None,
# password=None,
# host="localhost", 默认
# port=3306, 默认
# charset="utf8" 默认
from PyMysqlModel import Model
```

方式一

```python
# 连接数据库     指定   数据库名             用户   密码
StudentModel = Model(database="model_test",user="root",password=123)
```

方式二

```python
# 读取根目录下 settings 配置文件连接数据库
# 推荐
StudentModel = Model()
```

全部代码

```python
from PyMysqlModel import Model

# 连接数据库     指定   数据库名             用户   密码
StudentModel = Model(database="model_test",user="root",password=123)

# 读取目录下 settings 配置文件连接数据库
# 推荐
# StudentModel = Model()

# 表名
table_name = "student_tb"

# 表字段
# 支持原生 sql 语句
student_table_fields = [
    "id int NOT NULL AUTO_INCREMENT",
    "name varchar(20)",  # 一个字符串为一个字段
    "age int",
    "gender enum('男','女')",
    "phone varchar(11)",
]

# 连接表
# 当该表不存在时 则会自动创建该表
# 注意：当表存在时，但表字段不一致时，无法操作该表
# 推荐删除该表(注意备份表数据)，并重新运行，自动创建该表，
StudentModel.link_table(table_name,student_table_fields)
```

#### create 添加数据

```python
# 添加数据
name = "张三1"
age = "18"
gender = 1
phone = "17613355211"

# 添加数据
# 接受一个 NULL 空 字段类型允
flag = StudentModel.create(name=name,age=age,gender=gender,phone=phone)

print(f"是否成功标志：{flag}")
# 添加成功 return True
# 添加失败 return False

# 关键字传参 位置随便
flag = StudentModel.create(age=age,name=name,phone=phone,gender=gender)

# 接受 NULL 空字段类型
# 不传，或传入一个 None
flag = StudentModel.create(name=name,gender=gender,phone=phone)
flag = StudentModel.create(name=name,age=None,gender=gender,phone=phone)

# 每张表 自带自增 id
# 可以指定
flag = StudentModel.create(id=66,name=name,age=age,gender=gender,phone=phone)
```

#### update 修改数据

```python
# 修改数据
# 修改后的数据
pk = 3
name = "李四"
age = 21
gender = 2
phone = "17613355211"

# 目前仅支持 根据 id 修改数据
# 传入要修改数据项的 id
# 其他字段为修改后的值
# id 字段为必传项

# 修改全部
flag = StudentModel.update(id=pk,name=name, age=age, gender=gender, phone=phone)
print(f"是否成功标志：{flag}")

# 修改 age 值为 None
flag = StudentModel.update(id=pk,name=name, age=None, gender=gender, phone=phone)

# 修改部分字段
flag = StudentModel.update(id=pk,name=name, phone=phone)
```

#### delete 删除数据

```python
# 删除数据
pk = 1
name = "张三"

# 根据 id 删除
num = StudentModel.delete(id=pk)
print(f"删除数据的条数：{num}")
# num： 返回删除数据的条数

# 根据条件删除
num = StudentModel.delete(name=name)

# 支持原生 sql 语句
num = StudentModel.delete(native_sql="age > 18")
```

#### all 查询数据

```python
# 获取所有数据
# result： 返回查询结果列表， list 类型
# data = StudentModel.all() # 查询全部
# for i in data:
#     print(i)
"""结果:
{'id': 2, 'name': '李四', 'age': 21, 'gender': '女', 'phone': '17613355211'}
{'id': 4, 'name': '张三', 'age': 18, 'gender': '男', 'phone': '17613355211'}
"""

# 获取指定字段值
# data = StudentModel.all("id","name") # 查询指定字段1
# for i in data:
#     print(i)
"""结果:
{'id': 2, 'name': '李四'}
{'id': 4, 'name': '张三'}
"""

# 聚合查询
# all filter get 全部支持聚合查询

result = StudentModel.all("avg(age)")
print(result)
"""结果:
[{'avg(age)': Decimal('18.3750')}]
"""
```

#### filter 查询数据

```python

# 根据表字段进行过滤查询
name = "张三"
age = 18

# 查询条件为 and 关系
# result： 返回查询列表， list 类型
result = StudentModel.filter(name=name,age=age)
for i in result:
    print(i)
"""结果:
{'id': 4, 'name': '张三', 'age': 18, 'gender': '男', 'phone': '17613355211'}
{'id': 5, 'name': '张三', 'age': 18, 'gender': '男', 'phone': '17613355211'}
"""


# 指定查询结果字段
# result = StudentModel.filter("id","name",age=age)
# for i in result:
#     print(i)
"""结果:
{'id': 4, 'name': '张三'}
{'id': 5, 'name': '张三'}
"""

# 聚合查询
# all filter get 全部支持聚合查询
# result = StudentModel.all("avg(age)")

# result = StudentModel.filter("avg(age)",gender="男")
# print(f"查询结果：{result}")
"""结果:
[{'avg(age)': Decimal('18.0000')}]
"""

# 原生查询
# 查询条件为 and 关系
# result = StudentModel.filter(native_sql="name like '张%'")
# for i in result:
#     print(i)
"""结果:
{'id': 7, 'name': '张三', 'age': None, 'gender': '男', 'phone': '17613355211'}
{'id': 8, 'name': '张三1', 'age': 18, 'gender': '男', 'phone': '17613355211'}
"""
```

#### get 查询数据

```python
# 根据表字段进行过滤查询
name = "张三"
age = 18

# 查询条件为 and 关系
# result： 返回第一条数据，dict 类型
result = StudentModel.get(name=name,age=age)
print(f"查询结果：{result}")
"""结果:
{'id': 4, 'name': '张三', 'age': 18, 'gender': '男', 'phone': '17613355211'}
"""

# 指定查询结果字段
# result = StudentModel.get("id","name",age=age)
# print(f"查询结果：{result}")
"""结果:
{'id': 4, 'name': '张三'}
"""

# result = StudentModel.get(native_sql="name like '李%'")
# print(f"查询结果：{result}")
"""结果:
{'id': 2, 'name': '李四', 'age': 21, 'gender': '女', 'phone': '17613355211'}
"""
```

#### 聚合查询

```python
# 聚合查询
result = StudentModel.all("avg(age)")
# all filter get 全部支持聚合查询
"""结果:
[{'avg(age)': Decimal('18.0000')}]
"""
```

#### 原生查询

```python
# 查询字段
result_field = ['name','age']

# sql 语句
sql = f"""
    select {",".join(result_field)}  from {StudentModel.table_name} where name like '张%'
"""

# 调用实例属性 获取游标对象 执行sql语句
StudentModel.mysql.execute(sql)
data = StudentModel.mysql.fetchall() # 获取查询结果

# 调用实例方法 组织数据
student_list = StudentModel.result(result_field,data)
for i in student_list:
    print(i)
"""结果:
{'name': '张三', 'age': 18}
{'name': '张三', 'age': 18}
{'name': '张三', 'age': 18}
{'name': '张三', 'age': None}
"""
```

