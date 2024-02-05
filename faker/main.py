from mimesis.enums import TimestampFormat
from mimesis.locales import Locale
from mimesis.keys import maybe
from mimesis.schema import Field, Fieldset, Schema
from mimesis.enums import Gender


field = Field(locale=Locale.ZH)
fieldset = Fieldset(Locale.ZH, seed=0xff)

schema_definition = lambda: {
    "pk": field("increment"),
    "uid": field("uuid"),
    "name": field("person.name"),
    "username": field("person.username"),
    "memo": field("text.word"),
    "version": field("version"),
    "timestamp": field("timestamp", fmt=TimestampFormat.RFC_3339),
    "email": field("person.email", domains=["idss-cn.com"]),
    "creator": field("full_name", gender=Gender.FEMALE),
    "apiKeys": field("uuid"),
}
schema = Schema(schema=schema_definition, iterations=3)

# schema = Schema(
#     schema=lambda: {
#         'id': field('uuid'),
#         'name': field('person.name'),
#         'version': field('version'),
#         'timestamp': field('timestamp', TimestampFormat.RFC_3339),
#         'owner': {
#             'email': field('person.email', domains=['test.com'], key=str.lower),
#             'token': field('token_hex'),
#             'creator': field('full_name', gender=Gender.FEMALE)
#         },
#         'address': {
#             'country': field('address.country'),
#             'province': field('address.province'),
#             'city': field('address.city')
#         }
#     },
#     iterations=3
# )

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

