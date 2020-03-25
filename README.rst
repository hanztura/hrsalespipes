HRSalesPipes
************

Deployment
##########

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#configure-nginx-to-proxy-pass-to-gunicorn

Server Specifications:
    Ubuntu 16 or 18
    Postgresql
    Gunicorn
    Python3.6
    Django2.2

Set-up Postgresql Database
    CREATE DATABASE hrsalespipes;
    CREATE USER hrsalespipes WITH PASSWORD 'hrsalespipes';
    ALTER ROLE hrsalespipes SET client_encoding TO 'utf8';
    ALTER ROLE hrsalespipes SET default_transaction_isolation TO 'read committed';
    ALTER ROLE hrsalespipes SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE hrsalespipes TO hrsalespipes;            

Set-up Gunicorn
    [Unit]
    Description=HRSalesPipes Daemon
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/home/path-to/hrsalespipes
    Environment=HRSALESPIPES_ALLOWED_HOST=ip_address_or_domain_name HRSALESPIPES_DATABASE_NAME=database_name HRSALESPIPES_DATABASE_USER=your_username "HRSALESPIPES_DATABASE_PASSWORD=your_password" "HRSALESPIPES_SECRET_KEY=your_secret_key"
    ExecStart=/home/path-to/envs/hrsalespipes/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/path-to/hrsalespipes/hrsalespipes.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

Install
    Weasy requirement
    sudo apt-get install build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

