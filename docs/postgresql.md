

一、PostgreSQL 统计所有数据表各自的总行数


一般来说，可以使用 count(*) 来获取具体某张表的总行数：

SELECT count(0) FROM t_user;
如果想获得所有表的行数信息，可以使用以下 SQL 语句：

SELECT
    relname,
    reltuples 
FROM
    pg_class
    CLS LEFT JOIN pg_namespace N ON ( N.oid = CLS.relnamespace ) 
WHERE
    nspname NOT IN ( 'pg_catalog', 'information_schema' ) 
    AND relkind = 'r' 
ORDER BY
    reltuples DESC;

该语句执行非常迅速，但不太精准，用于数据规模估算时非常有用。

更精确的计算方法是创建一个函数来实现统计功能：

CREATE TYPE table_count AS (table_name TEXT, num_rows INTEGER); 
CREATE OR REPLACE FUNCTION count_em_all () RETURNS SETOF table_count  AS '
DECLARE 
    the_count RECORD; 
    t_name RECORD; 
    r table_count%ROWTYPE; 
BEGIN
    FOR t_name IN 
        SELECT 
            c.relname
        FROM
            pg_catalog.pg_class c LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE 
            c.relkind = ''r''
            AND n.nspname = ''public'' 
        ORDER BY 1 
        LOOP
            FOR the_count IN EXECUTE ''SELECT COUNT(*) AS "count" FROM '' || t_name.relname 
            LOOP 
            END LOOP; 
            r.table_name := t_name.relname; 
            r.num_rows := the_count.count; 
            RETURN NEXT r; 
        END LOOP; 
        RETURN; 
END;
' LANGUAGE plpgsql; 

这段代码创建了一个名为 count_em_all 的函数，调用该函数即可获得准确的统计信息。需要注意的是，如果数据库中数据较多，该函数执行时会消耗更多的时间：

SELECT
    * 
FROM
    count_em_all ( ) AS r 
ORDER BY
    r.num_rows DESC;
