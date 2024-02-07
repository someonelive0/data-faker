
# Mysql use `` and Oracle use "" for field name.

def mkcreate(data, tablename):
    ls = [(k, v) for k, v in data.items() if v is not None ]
    if len(ls) == 0:
        return '-- no fields in data'
    
    sentence = '''
--
-- create table %s
--
CREATE TABLE %s ''' % (tablename, tablename) + '(\n'
    for i in ls:
        if isinstance(i[1], int):
            field = '    `' + i[0] + '` INTEGER'
        elif isinstance(i[1], float):
            field = '    `' + i[0] + '` FLOAT'
        else:
            field = '    `' + i[0] + '` TEXT'
        sentence += field + ', \n'
    sentence = sentence[:-3] + '\n);'
    return sentence

def mkinsert(data, tablename):
    ls = [(k, v) for k, v in data.items() if v is not None ]
    # print('-->', ls)
    sentence = 'INSERT INTO %s (' % tablename + ', '.join('`'+i[0]+'`' for i in ls) + \
               ')\n  VALUES (' +  ','.join(repr(i[1]) for i in ls) + ');'
    return sentence


if __name__ == '__main__':
    print('test make sql sentence from dict')
    data = {'pk': 3, 'flo': 12.22, 'userid': '9b2c8812-db39-48d6-a547-a688ebe80899', 'name': '职能', 'version': '76.93.71', 'timestamp': '2024-03-21T19:34:01Z',  'email': 'budget2021@mimesis.name', 'creator': '梦阳  须', 'apiKeys': '7a5f45d02610810f'}


    sentence = mkcreate(data, 'table1')
    print('make CREATE from dict: ', sentence)

    sentence = mkinsert(data, 'table1')
    print('make INSERT from dict: ', sentence)
