# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import version, tablename_faker, field_faker, mksql
from mimesis.schema import Schema
import random, time, sys, logging, argparse
from datetime import datetime



logger = logging.getLogger('data-faker')
ARG_TABLE_NUMBER = 2
ARG_ITEM_MIN = 100
ARG_ITEM_MAX = 1000
ARG_DB = 'mysql'
ARG_INSERT_BENTCH = 40


def init():
    logger.setLevel(logging.INFO)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler("data-faker.log", encoding="utf-8")
    sh.setFormatter(formator)
    fh.setFormatter(formator)
    logger.addHandler(sh)
    logger.addHandler(fh)

    global ARG_TABLE_NUMBER, ARG_ITEM_MIN, ARG_ITEM_MAX, ARG_DB
    parser = argparse.ArgumentParser(description='data-faker argparse')
    parser.add_argument('-n', '--number', type=int, help='args of table number')
    parser.add_argument('--min', type=int, default=100, help='min lines in a table')
    parser.add_argument('--max', type=int, default=1000, help='max lines in a table')
    parser.add_argument('--db', type=str, default='mysql', help='target database, such as mysql, postgresql or oracle')
    parser.add_argument('--batch', type=int, default=40, help='extend insert number in one batch')
    args = parser.parse_args()
    logger.info('args %s' % args)
    if args.number:
        ARG_TABLE_NUMBER = args.number
    ARG_ITEM_MIN, ARG_ITEM_MAX, ARG_DB, ARG_INSERT_BENTCH = args.min, args.max, args.db, args.batch

# 产生表名和字段动态函数的字典，即{ tablename: fields_lambda }
def make_tables():
    logger.info('make %d tablenames in one time' % ARG_TABLE_NUMBER)
    tablenames = tablename_faker.mktablenames(ARG_TABLE_NUMBER)
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

# Python对列表按数量分割
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


# 根据表的字典即{ tablename: fields_lambda }，输出模拟数据的INSERT的SQL的条数
def make_sql_insert(tables, filename=None):
    logger.info('make tables records min=%d max=%d' % (ARG_ITEM_MIN, ARG_ITEM_MAX))
    sentences = '-- created by %s version %s\n' % (version.APP_NAME, version.VERSION)
    sentences += '-- created on ' + time.strftime("%Y-%m-%dT%H:%M:%S %Z", time.localtime()) + '\n'
    fp = sys.stdout
    if filename is not None:
        fp = open(filename, 'w', encoding='utf-8')
    fp.write(sentences)

    count = 0
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        schema = Schema(schema=fields_lambda, iterations=random.randint(ARG_ITEM_MIN, ARG_ITEM_MAX))
        items = schema.create()
        # logger.debug(len(items))

        sentences = '\n--\n-- datas of %s\n' % tablename
        sentences += '-- item number %d\n--\n' % len(items)
        if ARG_DB == 'mysql':
            for items_tmp in batch(items, ARG_INSERT_BENTCH):
                sentence = mksql.mkinsert_ext(items_tmp, tablename)
                sentences += sentence + '\n'
                count += len(items_tmp)
        else:
            for item in items:
                sentence = mksql.mkinsert(item, tablename)
                sentences += sentence + '\n'
                count += 1

        fp.write(sentences)

    if filename is not None: # if output to file then close it
        fp.close()

    return count


if __name__ == '__main__':
    init()

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
    logger.info('running time: %s Seconds' % (datetime.fromtimestamp(time.mktime(time.localtime(end_time)))
                                               - datetime.fromtimestamp(time.mktime(time.localtime(start_time)))))
    logger.info(time.strftime('END %Y-%m-%d %H:%M:%S',time.localtime(end_time)))
