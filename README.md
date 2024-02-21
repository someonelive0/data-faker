
# 数据模拟 Data-facker 

Data fro test data process.

require python-3.10 or higher


## 模拟数据库数据，产生SQL建表语句和插入语句

```
python .\myfaker\main.py
```

## 模拟Rest API，返回模拟数据

```
python .\fakerapi\main.py
```

然后访问 http://127.0.0.1:8000/xxx 即可，xxx表示任意字符。


## Database run the fake sql

### Such as mysql:

```
docker exec -ti mysql /bin/bash
docker cp fake_tables.sql mysql:/tmp
docker cp fake_tables_data.sql  mysql:/tmp
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'source /tmp/fake_tables.sql'
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'source /tmp/fake_tables_data.sql'
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'show tables'
```


### Such as postgresql:

```
docker cp fake_tables.sql postgres:/tmp
docker cp fake_tables_data.sql postgres:/tmp
docker exec -it postgres psql -U postgres -d fakedb -f /tmp/fake_tables.sql
docker exec -it postgres psql -U postgres -d fakedb -f /tmp/fake_tables_data.sql
```


### Such as oracle:

```
docker cp fake_tables.sql oracle:/tmp
docker cp fake_tables_data.sql oracle:/tmp
docker exec -ti oracle sqlplus testuser/<PASSWORD>@localhost:1521/XEPDB1 
docker exec -ti oracle sqlplus sys/<PASSWORD>@localhost:1521/XEPDB1 as sysdba  @/tmp/fake_tables.sql
docker exec -ti oracle sqlplus testuser/<PASSWORD>@localhost:1521/XEPDB1  @/tmp/fake_tables.sql
docker exec -ti oracle sqlplus testuser/<PASSWORD>@localhost:1521/XEPDB1  @/tmp/fake_tables_data.sql
```

说明
docker exec -it <container name> sqlplus <username>/<password>@<service name> @<container path>
  这里的 `<username>` 是数据库用户名，`<password>` 是数据库密码，`<service name>` 是数据库服务名，例如 `ORCLCDB.localdomain`；`<container path>` 是 SQL 文件在容器内的路径，例如 `/tmp/myscript.sql`

由于 & 字符被sqlplus当成变量前缀，需要关闭，在sqlplus中先执行语句： set define off
例如：
docker exec -ti oracle sqlplus testuser/<PASSWORD>@localhost:1521/XEPDB1 
SQL > set define off;
SQL > @/tmp/fake_tables_data.sql

