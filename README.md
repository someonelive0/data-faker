
Data-facker 

Data fro test data process.

require python-3.10 or higher


Database run the fake sql

Such as mysql:

docker exec -ti mysql /bin/bash
docker cp fake_tables.sql mysql:/tmp
docker cp fake_tables_data.sql  mysql:/tmp
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'source /tmp/fake_tables.sql'
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'source /tmp/fake_tables_data.sql'
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B --default-character-set=utf8 fakedb  -e 'show tables'


