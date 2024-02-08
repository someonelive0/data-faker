

一、如何手动更新所有表的统计信息？
在Oracle数据库中，有多种方法可以手动更新所有表的统计信息，我们将介绍两种常用方法：使用DBMS_STATS包和使用ANALYZE语句。

1. 使用DBMS_STATS包
DBMS_STATS是一个Oracle提供的包，用于管理统计信息。通过调用该包中的过程和函数，可以手动更新表的统计信息。

以下是使用DBMS_STATS包更新所有表的统计信息的步骤：

创建一个存储过程或脚本来更新统计信息：
CREATE OR REPLACE PROCEDURE UPDATE_ALL_TABLE_STATS AS
BEGIN
 FOR t IN (SELECT owner, table_name FROM all_tables WHERE owner='TESTUSER') LOOP
   DBMS_STATS.gather_table_stats(t.owner, t.table_name);
 END LOOP;
END;

这个存储过程会遍历所有的表，并调用DBMS_STATS.gather_table_stats过程来更新统计信息。

执行存储过程：

EXECUTE UPDATE_ALL_TABLE_STATS;

或者
BEGIN
	UPDATE_ALL_TABLE_STATS;
END;

执行该存储过程将会更新所有表的统计信息。

2. 使用ANALYZE语句
ANALYZE语句是Oracle提供的另一种手动更新统计信息的方法。

以下是使用ANALYZE语句更新所有表的统计信息的步骤：

创建一个存储过程或脚本来更新统计信息：
CREATE OR REPLACE PROCEDURE UPDATE_ALL_TABLE_STATS AS
BEGIN
 FOR t IN (SELECT owner, table_name FROM all_tables WHERE owner='TESTUSER') LOOP
   EXECUTE IMMEDIATE 'ANALYZE TABLE ' || t.owner || '.' || t.table_name || ' COMPUTE STATISTICS';
 END LOOP;
END;

这个存储过程会遍历所有的表，并使用ANALYZE语句来更新统计信息。

执行存储过程：

EXECUTE UPDATE_ALL_TABLE_STATS;

或者
BEGIN
	UPDATE_ALL_TABLE_STATS;
END;

执行该存储过程将会更新所有表的统计信息。


二、获取表的行数

逐个表统计数据行数，使用Select count语句统计，比较蛮烦，而且慢，可以使用如下语句直接用户下的所有表的数据行数。
    select TABLE_NAME, T.num_rows, T.last_analyzed  from tabs T

但是，从tabs表中获取的数据不是非常准确，在tabs表中存在一个字段last_analyzed，有最后分析的日期，一般都不是最新，所以导致数据不是非常准确，可以通过在command下面执行
     EXEC dbms_stats.gather_table_stats('【空间名称】','【tablename】',cascade=>true);
可以刷新tabs表中的num_rows列，以及最后更新时间。
