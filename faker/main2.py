from mimesis import Generic
generic = Generic()
a=generic.person.username(mask="U_d", drange=(100, 1000))
print(a)

from mimesis import Field, Locale
field = Field(Locale.EN)
a=field("username", mask="U_d", key=str.lower, drange=(100, 1000))
print(a)


from mimesis import Fieldset, Locale
fieldset = Fieldset(locale=Locale.EN)
a=fieldset("name", key=str.lower, i=30)
print(a)

from faker import Faker

fake = Faker('zh_CN')
data_total = [
            {fake.name(), fake.job(), fake.company(), fake.phone_number(), fake.company_email(), fake.address(),
             fake.iso8601(tzinfo=None, end_datetime=None)} for x in range(2)] 
print('Faker', data_total)



from faker_schema.faker_schema import FakerSchema
import json
schema = {'employee_id': 'uuid4', 'employee_name': 'name', 'employee_address': 'address', 'email_address': 'email'}
faker = FakerSchema()
data = faker.generate_fake(schema, iterations=4)
print(json.dumps(data))
