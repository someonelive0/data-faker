
Data-facker 

Data fro test data process.

require python-3.10 or higher


Database run the fake sql

Such as mysql:

docker cp fake_tables.sql mysql:/tmp/fake_tables.sql
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B fakedb  -e 'source /tmp/fake_tables.sql'
docker exec -ti mysql /usr/bin/mysql -uroot --password=<PASSWORD> -fr -B fakedb  -e 'show tables'



