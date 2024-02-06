# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import version, tablename_faker, field_faker, mksql
from mimesis.schema import Field, Fieldset, Schema
import random, time


table_count = 2
item_min = 1
item_max = 3

# 产生表名和字段动态函数的字典，即{ tablename: fields_lambda }
def make_tables():
    print('random make tablenames in one time')
    tablenames = tablename_faker.mktablenames(table_count)
    print(len(tablenames), tablenames)

    tables = {}
    for tablename in tablenames:
        print('tablename: ', tablename)
        fields_lambda = field_faker.mkfields_lambda()
        tables[tablename] = fields_lambda

    return tables

# 根据表的字典即{ tablename: fields_lambda }，输出创建表的SQL
def make_sql_create(tables, filename=None):
    sentences = '-- created by %s version %s\n' % (version.APP_NAME, version.VERSION)
    sentences += '-- created on ' + time.strftime("%Y-%m-%dT%H:%M:%S %Z", time.localtime()) + '\n'
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        item = fields_lambda()
        # print(len(item), item)

        sentence = mksql.mkcreate(item, tablename)
        # print(sentence)
        sentences += sentence + '\n'

    if filename is not None:
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(sentences)

    return sentences

# 根据表的字典即{ tablename: fields_lambda }，输出模拟数据的INSERT的SQL
def make_sql_insert(tables, filename=None):
    sentences = '-- created by %s version %s\n' % (version.APP_NAME, version.VERSION)
    sentences += '-- created on ' + time.strftime("%Y-%m-%dT%H:%M:%S %Z", time.localtime()) + '\n'
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        schema = Schema(schema=fields_lambda, iterations=random.randint(item_min, item_max))
        items = schema.create()
        # print(len(items))

        sentences += '\n--\n-- datas of %s\n--\n' % tablename
        for item in items:
            sentence = mksql.mkinsert(item, tablename)
            sentences += sentence + '\n'

    if filename is not None:
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(sentences)

    return sentences


if __name__ == '__main__':
    tables = make_tables()
    sql_creates = make_sql_create(tables, 'fake_tables.sql')
    print(sql_creates)

    sql_inserts = make_sql_insert(tables, 'fake_tables_data.sql')
    print(sql_inserts)
