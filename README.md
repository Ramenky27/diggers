##CMS for urban exploration blog engine
###Setup

Install PostgreSQL and Python3.

Import existing DB backup
```
psql -U diggers < dump.sql
```

Or prepare new db with psql:
```
create database diggers;
create user diggers with encrypted password 'securepass';
grant all privileges on database diggers to diggers;
alter database diggers OWNER TO diggers;
exit
```

Create virtual env and install packages:
```
sudo apt install python3.8-venv
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

Run project:
```
cd website
gunicorn website.wsgi
```

Now it run on port 8000