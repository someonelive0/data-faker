

# Usage

python3 ./fake_data/main.py -h
python3 ./fake_data/main.py -n 100
python3 ./fake_data/main.py -n 100 --min 100 --min 100 --max 1000 --db [mysql|oracle]

参数说明：
usage: main.py [-h] [-n NUMBER] [--min MIN] [--max MAX] [--db DB] [--batch BATCH]

fake_data argparse

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER  args of table number   产生的表的数量
  --min MIN             min lines in a table         每张表最小的记录数量
  --max MAX             max lines in a table         每张表最大的记录数量，具体记录数取最大和最小之间
  --db DB               target database, such as mysql, postgresql or oracle        数据库类型
  --batch BATCH         extend insert number in one batch    对支持扩展INSERT语句的库，每条INSERT的批处理记录数

日志文件: fake_data.log
输出文件: 
 fake_tables.sql       建表SQL文件
 fake_tables_data.sql  插入数据SQL文件

