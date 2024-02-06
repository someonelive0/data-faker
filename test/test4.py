# 测试动态匿名函数

import types

module_code = compile('def foobar(): return "foobar"', '', 'exec')
function_code = [c for c in module_code.co_consts if isinstance(c, types.CodeType)][0]
foobar = types.FunctionType(function_code, {})
print(foobar())

from faker import Faker
from mimesis.schema import Field
from mimesis.locales import Locale
from mimesis.enums import TimestampFormat
from mimesis.enums import Gender

fake = Faker(locale='zh_CN')
field = Field(locale=Locale.ZH)
# 字段名称和对应模拟值的字典，动态匿名函数
fields_template = {
    "pk": 'field("increment")',
    "uid": 'field("uuid")',
    "name": field("person.name"),
    "username": field("person.username"),
    "memo": field("text.word"),
    "text": fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None) ,
    "version": field("version"),
    "timestamp": field("timestamp", fmt=TimestampFormat.RFC_3339),
    "email": field("person.email", domains=["idss-cn.com"]),
    "creator": field("full_name", gender=Gender.FEMALE),
    "apiKeys": field("uuid"),
}
print(fields_template)

s = '''lambda: {
    "pk": field("increment"),
    "uid": field("uuid"),
    }'''
print(s)

f = eval(s)
print(type(f), f())