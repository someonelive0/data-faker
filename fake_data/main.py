# -*- coding: utf-8 -*-
# 产生模拟表和模拟字段，并产生模拟数据，进而生产SQL

import version, tablename_faker, field_faker, mksql
from mimesis.schema import Schema
import random, time, sys, logging, argparse, pathlib
from datetime import datetime


logger = logging.getLogger('fake_data')
ARG_TABLE_NUMBER = 2
ARG_ITEM_MIN = 20
ARG_ITEM_MAX = 100
ARG_DB = 'mysql'
ARG_INSERT_BENTCH = 40


def init():
    logger.setLevel(logging.DEBUG)
    formator = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d行 | [ %(levelname)s ] | [%(message)s]", datefmt="%Y/%m/%d/%X")
    sh = logging.StreamHandler()
    fh = logging.FileHandler("fake_data.log", encoding="utf-8")
    sh.setFormatter(formator)
    fh.setFormatter(formator)
    logger.addHandler(sh)
    logger.addHandler(fh)

    global ARG_TABLE_NUMBER, ARG_ITEM_MIN, ARG_ITEM_MAX, ARG_DB, ARG_INSERT_BENTCH
    parser = argparse.ArgumentParser(description='fake_data argparse')
    parser.add_argument('-n', '--number', type=int, help='args of table number, default 2')
    parser.add_argument('--min', type=int, default=20, help='min lines in a table, default 20')
    parser.add_argument('--max', type=int, default=100, help='max lines in a table, default 100')
    parser.add_argument('--db', type=str, default='mysql', help='target database, such as mysql, postgresql or oracle, default mysql')
    parser.add_argument('--batch', type=int, default=40, help='extend insert number in one batch, default 40 in one insert')
    args = parser.parse_args()
    logger.info('args %s' % args)
    if args.number:
        ARG_TABLE_NUMBER = args.number
    ARG_ITEM_MIN, ARG_ITEM_MAX, ARG_DB, ARG_INSERT_BENTCH = args.min, args.max, args.db, args.batch
    if ARG_ITEM_MAX < ARG_ITEM_MIN:
        ARG_ITEM_MAX = ARG_ITEM_MIN

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

        sentence = mksql.mkcreate(item, tablename, ARG_DB)
        # logger.debug(sentence)
        fp.write(sentence + '\n')
        count += 1
        if count % 1000 == 0:
            logger.debug('make_sql_create count %d' % count)

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

    # 由于 & 字符被sqlplus当成变量前缀，需要关闭，在sqlplus中先执行语句： set define off
    if ARG_DB == 'oracle':
        sentences += 'set define off;\n'

    fp = sys.stdout
    if filename is not None:
        fp = open(filename, 'w', encoding='utf-8')
    fp.write(sentences)

    count, table_count = 0, 0
    for tablename in tables.keys():
        fields_lambda = tables[tablename]
        schema = Schema(schema=fields_lambda, iterations=random.randint(ARG_ITEM_MIN, ARG_ITEM_MAX))
        items = schema.create()
        # logger.debug(len(items))
        table_count += 1
        if table_count % 1000 == 0:
            logger.debug('make_sql_insert table_count %d, items %d' % (table_count, count))

        sentences = '\n--\n-- datas of table %s within %s\n' % (tablename, ARG_DB)
        sentences += '-- item number %d\n--\n' % len(items)
        if ARG_DB == 'mysql' or ARG_DB == 'postgresql':  # mysql and postgresql support extend insert
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

    pathlib.Path('sql').mkdir(parents=True, exist_ok=True) 
    count = make_sql_create(tables, 'sql/fake_tables.sql')
    logger.info('create table of sql sentences:  %d in file sql/fake_tables.sql' %  count)

    count = make_sql_insert(tables, 'sql/fake_tables_data.sql')
    logger.info('insert of sql sentences: %d in file sql/fake_tables_data.sql' % count)

    end_time = time.time()
    logger.info('running time: %s Seconds' % (datetime.fromtimestamp(time.mktime(time.localtime(end_time)))
                                               - datetime.fromtimestamp(time.mktime(time.localtime(start_time)))))
    logger.info(time.strftime('END %Y-%m-%d %H:%M:%S',time.localtime(end_time)))
