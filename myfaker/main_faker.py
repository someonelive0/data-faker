from mimesis.enums import TimestampFormat
from mimesis.locales import Locale
from mimesis.keys import maybe
from mimesis.schema import Field, Fieldset, Schema
from mimesis.enums import Gender
from faker import Faker
 
fake = Faker(locale='zh_CN')

field = Field(locale=Locale.ZH)
fieldset = Fieldset(Locale.ZH, seed=0xff)

schema_definition = lambda: {
    "pk": field("increment"),
    "uid": field("uuid"),
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

schema_definition1 = {
    "pk": field("increment"),
    "uid": field("uuid"),
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
schema_definition1["ext"] = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
print(type(schema_definition1))

schema_definition2 = lambda: schema_definition1
print(type(schema_definition2))

schema = Schema(schema=schema_definition2, iterations=3)


# print(dir(schema._Schema__schema))
# print(field)
# print(dir(schema_definition))

# schema.to_csv(file_path='data.csv')
# schema.to_json(file_path='data.json')
# schema.to_pickle(file_path='data.obj')

datas = schema.create()
print(len(datas))


# import json
# print(json.dumps(datas))

import mksql
if len(datas) > 0:
     sentence = mksql.mkcreate(datas[0], 'table2')
     print(sentence)

for data in datas:
    # print(data)
    # print(data.keys())
    # print(data.items())
    sentence = mksql.mkinsert(data, 'table2')
    print(sentence)

