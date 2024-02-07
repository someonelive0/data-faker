# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import version, tablename_faker, field_faker, mksql
from mimesis.schema import Field, Fieldset, Schema
import random, time, datetime, sys, logging


table_count = 2000
item_min = 100
item_max = 3000

logger = logging.getLogger('data-faker')
logger.setLevel(logging.INFO)
formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
sh = logging.StreamHandler()
fh = logging.FileHandler("data-faker.log", encoding="utf-8")
sh.setFormatter(formator)
fh.setFormatter(formator)
logger.addHandler(sh)
logger.addHandler(fh)


# 产生表名和字段动态函数的字典，即{ tablename: fields_lambda }
def make_tables():
    logger.info('random make %d tablenames in one time' % table_count)
    tablenames = tablename_faker.mktablenames(table_count)
    # logger.debug(len(tablenames), tablenames)

    tables = {}
    for tablename in tablenames:
        # logger.debug('tablename: ', tablename)
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
        # logger.debug(len(item), item)

        sentence = mksql.mkcreate(item, tablename)
        # logger.debug(sentence)
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
        # logger.debug(len(items))

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
    logger.info(time.strftime('BEGIN %Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    # 产生表的定义
    tables = make_tables()
    logger.info('make tables %d' % len(tables))

    count = make_sql_create(tables, 'fake_tables.sql')
    logger.info('create table of sql sentences:  %d' %  count)

    count = make_sql_insert(tables, 'fake_tables_data.sql')
    logger.info('insert of sql sentences: %d' % count)

    end_time = time.time()
    logger.info('running time: %s Seconds' % (datetime.datetime.fromtimestamp(time.mktime(time.localtime(end_time)))
                                               - datetime.datetime.fromtimestamp(time.mktime(time.localtime(start_time)))))
    logger.info(time.strftime('END %Y-%m-%d %H:%M:%S',time.localtime(end_time)))
