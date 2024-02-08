

1. 查询所有表
show tables;

select count(table_name) from information_schema.tables
where table_schema = 'fakedb'

select table_name, table_schema from information_schema.tables
where table_schema = 'fakedb'

2. 显示表的统计信息
select * from mysql.innodb_table_stats 

3. 分析表，会更新表的统计信息
analyze table animation_4830;

4. mysql 的数据库结构信息，大部分都保存在了 information_schema 的表中。

这些语句在项目部署过程中经常使用，需要用于验证是否完成数据初始化；
也经常用于逆向工程，通过分析数据库表结构，生成可能出现的代码。
-- 展示所有数据库
SHOW DATABASES;
-- 展示所有表格
SHOW TABLES;

-- 展示某个数据库的所有表
SHOW TABLES FROM med;

-- 查看 cls 表的字段
DESCRIBE cls;
-- 查看 cls 表的字段，包括权限和注解
SHOW FULL COLUMNS FROM cls;

-- 查看表的所有字段
SELECT * FROM information_schema.COLUMNS WHERE TABLE_NAME = 'cls';
-- 查看库中的所有表
SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA ='med';
