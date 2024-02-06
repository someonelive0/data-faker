# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import version, tablename_faker, field_faker, mksql
from mimesis.schema import Field, Fieldset, Schema
import random, time, sys


table_count = 200
item_min = 100
item_max = 30000

# 产生表名和字段动态函数的字典，即{ tablename: fields_lambda }
def make_tables():
    print('random make tablenames in one time')
    tablenames = tablename_faker.mktablenames(table_count)
    # print(len(tablenames), tablenames)

    tables = {}
    for tablename in tablenames:
        # print('tablename: ', tablename)
        fields_lambda = field_faker.mkfields_lambda()
        tables[tablename] = fields_lambda

    return tables

# 根据表的字典即{ tablename: fields_lambda }，输出创建表的SQL
def make_sql_create(tables, filename=None):
    sentences = '-- created by %s version %s\n' % (version.APP_NAME, version.VERSION)
    sentences += '-- created on ' + time.strftime("%Y-%m-%dT%H:%M:%S %Z", time.localtime()) + '\n'
    sentences += '-- tables number %d\n' % len(tables)
    fp = sys.stdout
    if filename is not None:
        fp = open(filename, 'w', encoding='utf-8')
    fp.write(sentences)

    count = 0
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        item = fields_lambda()
        # print(len(item), item)

        sentence = mksql.mkcreate(item, tablename)
        # print(sentence)
        fp.write(sentence + '\n')
        count += 1

    return count

# 根据表的字典即{ tablename: fields_lambda }，输出模拟数据的INSERT的SQL的条数
def make_sql_insert(tables, filename=None):
    sentences = '-- created by %s version %s\n' % (version.APP_NAME, version.VERSION)
    sentences += '-- created on ' + time.strftime("%Y-%m-%dT%H:%M:%S %Z", time.localtime()) + '\n'
    fp = sys.stdout
    if filename is not None:
        fp = open(filename, 'w', encoding='utf-8')
    fp.write(sentences)

    count = 0
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        schema = Schema(schema=fields_lambda, iterations=random.randint(item_min, item_max))
        items = schema.create()
        # print(len(items))

        sentences = '\n--\n-- datas of %s\n' % tablename
        sentences += '-- item number %d\n--\n' % len(items)
        for item in items:
            sentence = mksql.mkinsert(item, tablename)
            sentences += sentence + '\n'
            count += 1

        fp.write(sentences)

    if filename is not None: # if output to file then close it
        fp.close()

    return count


if __name__ == '__main__':
    start_time = time.time()
    print(time.strftime('BEGIN %Y-%m-%d %H:%M:%S',time.localtime(start_time)))

    # 产生表的定义
    tables = make_tables()
    print('make tables %d' % len(tables))

    count = make_sql_create(tables, 'fake_tables.sql')
    print('create table of sql sentences: ', count)

    count = make_sql_insert(tables, 'fake_tables_data.sql')
    print('insert of sql sentences: ', count)

    end_time = time.time()
    print('Running time: %s Seconds'%(end_time - start_time))
    print(time.strftime('END %Y-%m-%d %H:%M:%S',time.localtime(end_time)))
