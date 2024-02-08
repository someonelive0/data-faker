
# -*- coding: utf-8 -*-
# Mysql use `` and Oracle use "" for field name.

DB_TPYE = ''      # such as mysql, postgresql, oracle
DB_QUOTE = ''     # mysql use `` as quote, postgresql and oracle use "" as quote
DB_TEXT_TYPE = 'TEXT'

# 创建建表语句
def mkcreate(data, tablename, dbtype='mysql'):
    global DB_TPYE, DB_QUOTE, DB_TEXT_TYPE
    DB_TPYE = dbtype
    if DB_TPYE == 'mysql':
        DB_QUOTE = '`'
    elif DB_TPYE == 'postgresql':
        DB_QUOTE = '"'
    elif DB_TPYE == 'oracle':
        DB_QUOTE = '"'
        DB_TEXT_TYPE = 'VARCHAR(2048)'

    ls = [(k, v) for k, v in data.items() if v is not None ]
    if len(ls) == 0:
        return '-- no fields in data'

    sentence = '''
--
-- create table %s within %s
--
CREATE TABLE %s ''' % (tablename, DB_TPYE, tablename) + '(\n'
    for i in ls:
        if isinstance(i[1], int):
            field = '    ' + DB_QUOTE + i[0] + DB_QUOTE + ' INTEGER'
        elif isinstance(i[1], float):
            field = '    ' + DB_QUOTE + i[0] + DB_QUOTE + ' FLOAT'
        else:
            field = '    ' + DB_QUOTE + i[0] + DB_QUOTE + ' ' + DB_TEXT_TYPE
        sentence += field + ', \n'
    sentence = sentence[:-3] + '\n);'
    
    return sentence

# 创建INSERT一条数据语句，每个字段加回车是为了避免oracle的单行超过300个字符的错误
def mkinsert(data, tablename):
    ls = [(k, v) for k, v in data.items() if v is not None ]
    # print('-->', ls)
    sentence = 'INSERT INTO %s (' % tablename + ',\n'.join(DB_QUOTE+i[0]+DB_QUOTE for i in ls) + \
               ')\n  VALUES (' +  ',\n'.join(repr(i[1]) for i in ls) + ');'
    return sentence

# 创建扩展INSERT语句，即插入多条数据，输入参数datas是list集合
def mkinsert_ext(datas, tablename):
    if len(datas) == 0:
        return ''
    
    ls = [(k, v) for k, v in datas[0].items() if v is not None ]
    # print('-->', ls)
    sentence = '\nINSERT INTO %s (' % tablename + ', '.join(DB_QUOTE+i[0]+DB_QUOTE for i in ls) + ') VALUES '

    for data in datas:
        ls = [(k, v) for k, v in data.items() if v is not None ]
        sentence += '\n  (' +  ','.join(repr(i[1]) for i in ls) + '),'
    return sentence[:-1] + ';'


if __name__ == '__main__':
    print('test make sql sentence from dict')
    data = {'pk': 3, 'flo': 12.22, 'userid': '9b2c8812-db39-48d6-a547-a688ebe80899', 'name': '职能', 'version': '76.93.71', 'timestamp': '2024-03-21T19:34:01Z',  'email': 'budget2021@mimesis.name', 'creator': '梦阳  须', 'apiKeys': '7a5f45d02610810f'}

    sentence = mkcreate(data, 'table1', 'postgresql')
    print('-- make CREATE from dict: \n', sentence)

    sentence = mkinsert(data, 'table1')
    print('-- make INSERT from dict: \n', sentence)

    datas = [data, data]
    sentence = mkinsert_ext(datas, 'table1')
    print('-- make Extent INSERT from dict: \n', sentence)
