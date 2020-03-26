HRSalesPipes
************

Overview
########
    
    HRSalesPipes is an open-source *business web application* that can be used to manage core operations of an **HR Recruitment Agency** (or whatever the name is of bussinesses that deliver similar services).

    Get free from using multiple separate spreadsheet(excel) files. Yes, HRSalesPipes solves all the problem relating to managing your data specially if your business is still using multiple spreadsheets.

    Produce real-time reports to make well informed, better, smart, and on-time decisions.

    With its Dashboard, you can directly and conveniently know how your business is performing. Even your employees will get to know how they are doing that might help them get motivated to perform better and achieve better results.

    Improve the security of your data by on-demand backups and secured transfer protocol(HTTPS).

    And you don't even have to worry about getting computer hardwares, location to place all this equipments, hiring another IT personnel to set-up and maintain a server because HRSalesPipes is built for the cloud.

    **Access your system anytime and anywhere**.

    For $0.00, yes Z-E-R-O f----ing dollar, you can already have this system live in production in less than 30 mins (not overstating here guys).

    Here are the core operations of your business that HRSalesPipes can manage:
        1. Sales Pipeline
        2. Job Board Management
        3. Candidates, Clients, and Supplier Management
        4. Commissions
        5. Reports

    Oh by the way, since HRSalesPipes is OPEN-SOURCE, ahemmm.... yeah you can entirely have this awesome tool for **FREE**.

    Not just that it is free, you can even sell this software and not even spending a penny or spend a single second of coding.

    Now if you think HRSalesPipes can do something for you and your business, then let us start talking about what is HRSalesPipes and how to use it.


Modules
#######
    1. Contacts
    2. Jobs
    3. Pipeline
    4. Commissions
    5. Reports
    6. Dashboard
    7. System Administration
       
Contacts
********
    Manage your contacts here.

    Contacts includes Candidates, Clients, Suppliers, and Employees.

    All types of contacts can store basic information such as:
        a. Name
        b. Email Address
        c. Contact Numbers
        d. Location
           
    Candidates sub-module can store these extra information:
        Personal Details
        a. Language spoken
        b. Civil Status
        c. Gender
        d. Dependents
        e. Educational Attainment
        f. Date of Birth
        g. Current/Previous Position
        h. Current/Previous Company
        i. Current/Previous Salary and Benefits
        j. Motivation for leaving
        k. Expected Salary and Benefits
        l. Visa Status
        m. Availability for Interview
        n. Notice Period
        o. Candidate Owner
        p. CV Template
        q. Notes/Remarks

Jobs
****

Pipeline
********

Commissions
***********


Deployment
##########

    For reference on how to setup the server, see link below. Though this guide is created by DigitalOcean, but it can be applied to any server setup.

        https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#configure-nginx-to-proxy-pass-to-gunicorn

Server Specifications:
**********************

    Ubuntu 16 or 18
    Postgresql
    Gunicorn
    Python3.6
    Django2.2

Install Project Requirements
****************************

    Weasy requirement
        sudo apt-get install build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

    With or without Python virtual environment install the Django project requirements:
        pip install -r config/requirements/base.txt
        pip install -r config/requirements/producttion.txt


Set-up Postgresql Database
**************************

    Sample setup only. Please change database name, password, and user accordingly.

    CREATE DATABASE database_name;
    CREATE USER your_username WITH PASSWORD 'your_password';
    ALTER ROLE your_username SET client_encoding TO 'utf8';
    ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
    ALTER ROLE your_username SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE database_name TO your_username;            

Set-up Gunicorn
***************

    [Unit]
    Description=HRSalesPipes Daemon
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/home/path-to/hrsalespipes
    Environment=HRSALESPIPES_ALLOWED_HOST=ipaddres.or.domain.com,another.domain.com HRSALESPIPES_DATABASE_NAME=database_name HRSALESPIPES_DATABASE_USER=your_username "HRSALESPIPES_DATABASE_PASSWORD=your_password" "HRSALESPIPES_SECRET_KEY=your_secret_key"
    ExecStart=/home/path-to/envs/hrsalespipes/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/path-to/hrsalespipes/hrsalespipes.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

