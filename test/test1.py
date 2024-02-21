from mimesis.enums import TimestampFormat
from mimesis.locales import Locale
from mimesis.keys import maybe
from mimesis.schema import Field, Fieldset, Schema
from mimesis.enums import Gender
from faker import Faker
import json


fake = Faker(locale='zh_CN')
field = Field(locale=Locale.ZH, seed=0xae)
fieldset = Fieldset(Locale.ZH, seed=0xff)

schema_definition = lambda: {
    "pk": field("increment"),
    "uid": field("uuid"),
    "name": field("person.surname")+field("person.name"),
    "username": field("person.username"),
    "memo": field("text.word"),
    "sentence2": fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None) ,
    "version": field("version"),
    "timestamp": field("timestamp", fmt=TimestampFormat.RFC_3339),
    "email": field("person.email", domains=["idss-cn.com"]),
    "creator": field("full_name", gender=Gender.FEMALE),
    "token": field("token_hex"),
    "apiKeys": field("token_hex", key=lambda s: s[:16]),

    "academic_degree": field("person.academic_degree"),
    "birthdate": str(field("person.birthdate")),
    "blood_type": field("person.blood_type"),
    "first_name": field("person.first_name"),
    "full_name": field("person.full_name"),
    "gender": field("person.gender"),
    "gender_code": field("person.gender_code"),
    "gender_symbol": field("person.gender_symbol"),
    "height": field("person.height"),
    "identifier": field("person.identifier"),
    "language": field("person.language"),
    "last_name": field("person.last_name"),
    "nationality": field("person.nationality"),
    "occupation": field("person.occupation"),
    "password": field("person.password"),
    "phone_number": field("person.phone_number"),
    "political_views": field("person.political_views"),
    "sex": field("person.sex"),
    "surname": field("person.surname"),
    "telephone": field("person.telephone", mask="###-#######"),
    "title": field("person.title"),
    "university": field("person.university"),
    "views_on": field("person.views_on"),
    "weight": field("person.weight"),
    "worldview": field("person.worldview"),

    "alphabet": ",".join(field("text.alphabet")),
    "answer": field("text.answer"),
    "color": field("text.color"),
    "emoji": field("text.emoji"),
    "hex_color": field("text.hex_color"),
    "level": field("text.level"),
    "quote": field("text.quote"),
    "rgb_color": str(field("text.rgb_color")),
    "sentence": field("text.sentence"),
    "text": field("text.text"),
    "title": field("text.title"),
    "word": field("text.word"),
    "words": ','.join(field("text.words")),
    "desc": field("text.sentence"),
    "description": field("text.sentence"),

    "ean": field("code.ean"),
    "imei": field("code.imei"),
    "isbn": field("code.isbn"),
    "issn": field("code.issn"),
    "locale_code": field("code.locale_code"),
    "pin": field("code.pin"),

    "address": field("address.address"),
    "calling_code": field("address.calling_code"),
    "city": field("address.city"),
    "continent": field("address.continent"),
    "coordinates": ','.join(field("address.coordinates")),
    "country": field("address.country"),
    "country_code": field("address.country_code"),
    "country_emoji_flag": field("address.country_emoji_flag"),
    "federal_subject": field("address.federal_subject"),
    "isd_code": field("address.isd_code"),
    "latitude": field("address.latitude"),
    "longitude": field("address.longitude"),
    "postal_code": field("address.postal_code"),
    "prefecture": field("address.prefecture"),
    "province": field("address.province"),
    "region": field("address.region"),
    "state": field("address.state"),
    "street_name": field("address.street_name"),
    "street_number": field("address.street_number"),
    "street_suffix": field("address.street_suffix"),
    "zip_code": field("address.zip_code"),

    "bank": field("finance.bank"),
    "company": field("finance.company"),
    "company_type": field("finance.company_type"),
    "cryptocurrency_iso_code": field("finance.cryptocurrency_iso_code"),
    "cryptocurrency_symbol": field("finance.cryptocurrency_symbol"),
    "currency_iso_code": field("finance.currency_iso_code"),
    "currency_symbol": field("finance.currency_symbol"),
    "price": field("finance.price"),
    "price_in_btc": field("finance.price_in_btc"),
    "stock_exchange": field("finance.stock_exchange"),
    "stock_name": field("finance.stock_name"),
    "stock_ticker": field("finance.stock_ticker"),

    "dish": field("food.dish"),
    "drink": field("food.drink"),
    "fruit": field("food.fruit"),
    "spices": field("food.spices"),
    "dish": field("food.vegetable"),

    "hash": field("cryptographic.hash"),
    "mnemonic_phrase": field("cryptographic.mnemonic_phrase"),
    # "token_bytes": field("cryptographic.token_bytes"),
    "token_hex": field("cryptographic.token_hex"),
    "token_urlsafe": field("cryptographic.token_urlsafe"),
    "uuid": field("cryptographic.uuid"),

    "calver": field("development.calver"),
    "ility": field("development.ility"),
    "os": field("development.os"),
    "programming_language": field("development.programming_language"),
    "software_license": field("development.software_license"),
    "stage": field("development.stage"),
    "system_quality_attribute": field("development.system_quality_attribute"),
    "version": field("development.version"),

    "extension": field("file.extension"),
    "file_name": field("file.file_name"),
    "mime_type": field("file.mime_type"),
    "file_size": field("file.size"),

    "cpu": field("hardware.cpu"),
    "cpu_codename": field("hardware.cpu_codename"),
    "cpu_frequency": field("hardware.cpu_frequency"),
    "generation": field("hardware.generation"),
    "graphics": field("hardware.graphics"),
    "gpu": field("hardware.graphics"),
    "manufacturer": field("hardware.manufacturer"),
    "phone_model": field("hardware.phone_model"),
    "ram_size": field("hardware.ram_size"),
    "ram_type": field("hardware.ram_type"),
    "resolution": field("hardware.resolution"),
    "screen_size": field("hardware.screen_size"),
    "ssd_or_hdd": field("hardware.ssd_or_hdd"),

    "content_type": field("internet.content_type"),
    "dsn": field("internet.dsn"),
    "hostname": field("internet.hostname"),
    "http_method": field("internet.http_method"),
    "http_request_headers": json.dumps(field("internet.http_request_headers")),
    "http_response_headers": json.dumps(field("internet.http_response_headers")),
    "http_status_code": field("internet.http_status_code"),
    "http_status_message": field("internet.http_status_message"),
    "ip": field("internet.ip_v4"),
    "ip4": field("internet.ip_v4"),
    "ipv4": field("internet.ip_v4"),
    "ip_v4": field("internet.ip_v4"),
    "ip_v4_with_port": field("internet.ip_v4_with_port"),
    "ipv4_port": field("internet.ip_v4_with_port"),
    "ip6": field("internet.ip_v6"),
    "ipv6": field("internet.ip_v6"),
    "ip_v6": field("internet.ip_v6"),
    "mac": field("internet.mac_address"),
    "mac_address": field("internet.mac_address"),
    "path": field("internet.path"),
    "port": field("internet.port"),
    "dns": field("internet.public_dns"),
    "public_dns": field("internet.public_dns"),
    "query_parameters": json.dumps(field("internet.query_parameters")),
    "slug": field("internet.slug"),
    "stock_image_url": field("internet.stock_image_url"),
    "tld": field("internet.tld"),
    "top_domain": field("internet.top_level_domain"),
    "top_level_domain": field("internet.top_level_domain"),
    "uri": field("internet.uri"),
    "url": field("internet.url"),
    "user_agent": field("internet.user_agent"),

    "dev_dir": field("path.dev_dir"),
    "home": field("path.home"),
    "project_dir": field("path.project_dir"),
    "root": field("path.root"),
    "user_home": field("path.user"),
    "users_folder": field("path.users_folder"),

    "bitcoin_address": field("payment.bitcoin_address"),
    "cid": field("payment.cid"),
    "credit_card_expiration_date": field("payment.credit_card_expiration_date"),
    "credit_card_network": field("payment.credit_card_network"),
    "credit_card_number": field("payment.credit_card_number"),
    "credit_card_owner": json.dumps(field("payment.credit_card_owner")),
    "cvv": field("payment.cvv"),
    "ethereum_address": field("payment.ethereum_address"),
    "paypal": field("payment.paypal"),

    "airplane": field("transport.airplane"),
    "car": field("transport.car"),
    "car_manufacturer": field("transport.manufacturer"),
    "vehicle_registration_code": field("transport.vehicle_registration_code"),

    "dna_sequence": field("science.dna_sequence"),
    "measure_unit": field("science.measure_unit"),
    "metric_prefix": field("science.metric_prefix"),
    "rna_sequence": field("science.rna_sequence"),

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

schema = Schema(schema=schema_definition, iterations=3)


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

# 注意运行的PWD目录
import sys
sys.path.append(".")
sys.path.append("..")
from fake_data import mksql


if len(datas) > 0:
     sentence = mksql.mkcreate(datas[0], 'table2')
     print(sentence)

for data in datas:
    # print(data)
    # print(data.keys())
    # print(data.items())
    sentence = mksql.mkinsert(data, 'table2')
    print(sentence)

