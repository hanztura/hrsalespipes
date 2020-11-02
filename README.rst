HRSalesPipes
************

Overview
########
    
    HRSalesPipes is an open-source *business web application* that can be used to manage core operations of an **HR Recruitment Agency** (or whatever the name is of bussinesses that deliver similar services).

    Get free from using multiple separate spreadsheet(excel) files. Yes, HRSalesPipes *solves all the problem relating to managing our data* specially if our business is still using multiple spreadsheets.

    Produce real-time reports to make *well informed, better, smart, and on-time decisions*.

    With its Dashboard, we can *directly and conveniently know how our business is performing*. Even our employees will get to know how they are doing that might help them get motivated to perform better and achieve better results.

    *Improve the security* of our data by on-demand backups and secured transfer protocol(HTTPS).

    Related to improving the security are the different user permissions and that we can give to all sorts of user roles. This enable us to control which user can do this or that action(s).

    And we don't even have to worry about getting computer hardwares, location to place all this equipments, hiring another IT personnel to set-up and maintain a server because HRSalesPipes is built for the cloud.

    **Access our system anytime and anywhere**.

    For $0.00, yes Z-E-R-O f----ing dollar, we can already have this system live in production in less than 30 mins (not overstating here guys).

    Here are the core operations of our business that HRSalesPipes can manage:
        1. Sales Pipeline
        2. Job Board Management
        3. Candidates, Clients, and Supplier Management
        4. Commissions
        5. Reports

    Oh by the way, since HRSalesPipes is OPEN-SOURCE, ahemmm.... yeah we can entirely have this awesome tool for **FREE**.

    Not just that it is free, we can even sell this software and not even spending a penny or spend a single second of coding.

    Now if we think HRSalesPipes can do something for we and our business, then let us start talking about what is HRSalesPipes and how to use it.


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
    Manage our contacts here.

    Contacts includes Candidates, Clients, Suppliers, and Employees.

    All types of contacts can store basic information such as:
        a. Name
        b. Email Address
        c. Contact Numbers
        d. Location
           
    Candidates sub-module can store these extra information:
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
        r. Medical Fields (if medical related candidate).
        
    You can download a CV out of this canidate information using a template built with a docx document. And that is awesome.

    Clients have the following extra information:
        a. Initial Approach
        b. Meeting Arranged
        c. Agreement Terms
        d. Agreement Fee
        e. Refund Scheme
        f. Validity
        
    Suppliers and Employee are pretty much basic. But a user can be connected with a particular user account.

Jobs
****
    We can manage all of the Jobs our client needs here.
    
    These are the information that we can store in this module:
        a. Job Reference Number
        b. Date
        c. Status
        d. Client
        e. Positoin
        f. Location
        g. Potential Income
        h. Job Candidates (sub-module)
        i. Interviews (sub-module)
    
    Job Candidates is a sub-module of the Job module. In this sub-module we can manage all the prospect candidates for the specific Job record.
    
    A Job canidate may have the following information:
        a. Registration Date
        b. Status
        c. CV Source
        d. Date the cv was shared to the client
        e. Remarks
        f. Salary Offered
        g. Tentative date of joining
        h. Associate
        i. Consultant
    
    Interviews sub-module is where we can record all the interviews made with our job candidates.

Pipeline
********
    Pipelne module is where we manage our sales pipeline.

    As soon as a job candidate progresses to a status where it is set-up to automatically create a Pipeline record, then the system will automatically generate a pipeline record and compute the related amounts for us.

    A pipeline record can have the following information:
        a. Date
        b. Successful Date
        c. Job Candidate
        d. Recruitment Terms
        e. Recruitment Rate
        f. Base Amount
        g. Potential Income
        h. Status
        i. Invoice Date
        j. Invoice Number
        k. Invoice Amount
        l. VAT
    
    Once a Pipeline progresses into a 100%, then the system will automatically compute and generate commission records for us. These commission records can be edited at a later time.

Commissions
***********
    Here commissions are being managed.

    A Commission record may have the following information:
        a. Pipeline record
        b. Employee
        c. Rate used
        d. Amount of the commission
        e. If this record is paid
           
    What is amazing, is that we can set-up the commission rates. So the system adjusts itself according to our commssion schemes.

Reports
*******
    Here we can generate and export in PDF or Excel format business reports that we need.

    Here are the reports that are available:
        a. Pipeline Summary
        b. Jobs Summary
        c. Job to Pipeline Analysis
        d. Commissions Earned Summary
        e. Monthly Invoices Summary
           
    If a report is a missing, we can let the developer of HRSalesPipes know by sending him an email to hanz@xofytech.com. Or create a feature request on the project's official repository https://github.com/hanztura/hrsalespipes.


Dashboard
*********
    As soon as a user log's in to the system, they are redirected into the Dashboard.

    In Dashboard we can see directly the different statistics of our business through dashboard cards and graphs.

    These are some of Dashboard items:
        a. Active Jobs
        b. Succesful job placements this month
        c. Interviews Arranged
        d. CVs sent to clients\
        e. Income generated this month
        f. Income generated last month
        g. Successful job placements per industry
        h. Successful job placements per consultant this month
        i. Total Income generated per consultant this month
        j. Total Income generated per consultant last 12 months
        k. YTD Client Performance
           
System Administration
*********************
    In this module, we are able to manage all the system related data.

    It is very important to note to not share the admin page url to anyone that is not meant to know this information.

    Included here are:
        a. Admin Page Honeypot login attempts
        b. Authentication and Authorization
        c. Commission Rates
        d. CV Templates
        e. Employees
        f. Job Status
        g. Job Candidate Status
        h. Pipeline Status
        i. Interview Modes
        j. Locations
        k. Settings
        l. Users
        m. Visa Status
           
    This is where we control the permissions each users or group of users may have.

    Be extremely careful in giving a user an access to this module.


Technical Specifications
########################
    This part of this documents are meant for developers or anyone who is interested on how HRSalesPipes was built and developed.

    These are the main software technologies used in this project:
        a. `Python <http://www.python.org/>`_ - Python is a programming language that lets you work more quickly and integrate your systems more effectively.
        b. `Django <https://www.djangoproject.com/>`_- The Web framework for perfectionists with deadlines.
        c. `VueJS <https://vuejs.org/>`_ - The Progressive JavaScript Framework.
        d. `Vuetify <vuetifyjs.com//>`_ - Vue Material Design Component Framework.

    For the detailed list of the packages used by the project, see the requirements file on the config>>requirements directory of this project.

    Also, the author of HRSalesPipes recommend to deploy the app in Ubuntu - The leading operating system for PCs, IoT devices, servers and the cloud.


About the Author
################
    Lets talk a little about the author.

    Meet me, Hanz Tura.

    A self-taught programmer who is currently registered in the Philippines with the business name "X of Y Business and Services" and works us a full stack web developer mainly with Django and VueJS.

    Hanz is a passionate learner. 

    He found a great love for programming, specially with Python.

    Send him a message at `hanz@xofytech.com <mailto:hanz@xofytech.com/>`_!


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
        sudo apt-get install build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info libpq-dev

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

