from faker import Faker
from faker_schema.faker_schema import FakerSchema
from faker_web import WebProvider


fake = Faker()
fake.add_provider(WebProvider)

faker = FakerSchema(faker=fake)
headers_schema = {'Content-Type': 'content_type', 'Server': 'server_token'}
fake_headers = faker.generate_fake(headers_schema)
print(fake_headers)
# {'Content-Type': 'application/json', 'Server': 'Apache/2.0.51 (Ubuntu)'}
