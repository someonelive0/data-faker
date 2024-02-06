
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import tablename_faker, field_faker, mksql
from mimesis.schema import Field, Fieldset, Schema
import random


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
def make_sql_create(tables):
    sentences = ''
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        item = fields_lambda()
        # print(len(item), item)

        sentence = mksql.mkcreate(item, tablename)
        # print(sentence)
        sentences += sentence + '\n'

    return sentences

# 根据表的字典即{ tablename: fields_lambda }，输出模拟数据的INSERT的SQL
def make_sql_insert(tables):
    sentences = ''
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        schema = Schema(schema=fields_lambda, iterations=random.randint(item_min, item_max))
        items = schema.create()
        print(len(items))

        for item in items:
            sentence = mksql.mkinsert(item, tablename)
            sentences += sentence + '\n'

    return sentences


if __name__ == '__main__':
    tables = make_tables()
    sql_creates = make_sql_create(tables)
    print(sql_creates)

    sql_inserts = make_sql_insert(tables)
    print(sql_inserts)
