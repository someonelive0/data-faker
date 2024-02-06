
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
    "name": 'field("person.name")',
    "username": 'field("person.username")',
    "memo": 'field("text.word")',
    "text": 'fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)',
    "version": 'field("version")',
    "timestamp": 'field("timestamp", fmt=TimestampFormat.RFC_3339)',
    "email": 'field("person.email", domains=["idss-cn.com"])',
    "creator": 'field("full_name", gender=Gender.FEMALE)',
    "apiKeys": 'field("uuid")',
}

# 从上述字典名称字典中，随机抽取一些字段组成新的字段名称和模拟值的新字典，而且字典名称后要加随机数来使字段名不一致
import copy
import random
def mkfields():
    fields = {}
    tmp_fields = copy.deepcopy(fields_template)

    # 设置输出字段数量，数量是随机取5到默认字典的一个随机数
    random_count = random.randint(5, len(fields_template))
    for i in range(random_count):
        item = tmp_fields.popitem()
        # print(item[0], item[1])
        k = item[0] + '_' + str(random.randint(100,10000))
        fields[k] = item[1]

    # 创建动态匿名函数的字符串，然后用eval产生匿名动态函数
    s = '''lambda: {
'''
    for k in fields.keys():
        s += '    "' + k + '": ' + fields[k] + ',\n'
    s += '}'
    print(s)
    return eval(s)

    # print(erase_count, len(fields_template)-erase_count)
    # for i in range(len(fields_template)-erase_count):
    #     fields.popitem()
    # return fields


if __name__ == '__main__':
    print('test make fields definition from template dict')
    for i in range(5):
        fields = mkfields()
        print(type(fields), fields())
