|Travis Badge|

**Quickly and easily store data about your open source projects on
GitHub and various Package Managers.**

Announcements
=============

All updates to this project is documented in our
`CHANGELOG <https://github.com/sendgrid/open-source-library-data-collector/blob/master/CHANGELOG.md>`__.

Installation
============

Environment Variables
---------------------

First, get your free SendGrid account
`here <https://sendgrid.com/free?source=open-source-data-collector>`__.

Next, update your environment with your
`SENDGRID\_API\_KEY <https://app.sendgrid.com/settings/api_keys>`__.

Initial Setup
-------------

.. code:: bash

    echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
    echo "sendgrid.env" >> .gitignore
    source ./sendgrid.env

.. code:: bash

    git clone https://github.com/sendgrid/open-source-library-data-collector.git
    cd sendgrid-open-source-library-external-data
    virtualenv venv
    cp .env_sample .env

Update your settings in ``.env``

.. code:: bash

    mysql -u USERNAME -p -e "CREATE DATABASE IF NOT EXISTS open-source-library-data-collector";
    mysql -u USERNAME -p open-source-external-library-data < db/data_schema.sql
    cp config_sample.yml config.yml

Update the settings in ``config.yml``

.. code:: bash

    source venv/bin/activate
    pip install -r requirements.txt

Update the code in ``package_managers.py``. The functions
``update_package_manager_data`` and ``update_db`` was customized for our
particular needs. You will want to either subclass those functions in
your own application or modify it to suit your needs. We will remove
these customizations in a future release. `Here is the GitHub
issue <https://github.com/sendgrid/open-source-library-data-collector/issues/5>`__
for reference.

To run:

::

    source venv/bin/activate
    python app.py

Dependencies
------------

-  The SendGrid Service, starting at the `free
   level <https://sendgrid.com/free?source=open-source-data-collector>`__)
-  `virtualenv <https://pypi.python.org/pypi/virtualenv>`__
-  `mysql <https://www.mysql.com>`__

Heroku Deploy
=============

::

    heroku login
    heroku create
    heroku addons:create cleardb:ignite

Access the cleardb DB and create the tables in db/data\_schema.sql

::

    heroku config:add ENV=prod
    heroku config:add GITHUB_TOKEN=<<your_github_token>>
    heroku config:add SENDGRID_API_KEY=<<your_sendgrid_api_key>>
    heroku addons:create scheduler:standard

Configure the schedular addon in your Heroku dashboard to run
``python app.py`` at your desired frequency.

Test by running ``heroku run worker``

Roadmap
-------

If you are interested in the future direction of this project, please
take a look at our
`milestones <https://github.com/sendgrid/open-source-library-data-collector/milestones>`__.
We would love to hear your feedback.

How to Contribute
-----------------

We encourage contribution to our projects, please see our
`CONTRIBUTING <https://github.com/sendgrid/open-source-library-data-collector/blob/master/CONTRIBUTING.md>`__
guide for details.

Quick links:

-  [Feature
   Request](https://github.com/sendgrid/open-source-library-data-collector/blob/master/CONTRIBUTING.md#feature\_request
-  [Bug
   Reports](https://github.com/sendgrid/open-source-library-data-collector/blob/master/CONTRIBUTING.md#submit\_a\_bug\_report
-  [Sign the CLA to Create a Pull
   Request](https://github.com/sendgrid/open-source-library-data-collector/blob/master/CONTRIBUTING.md#cla
-  [Improvements to the
   Codebase](https://github.com/sendgrid/open-source-library-data-collector/blob/master/CONTRIBUTING.md#improvements\_to\_the\_codebase

About
=====

open-source-library-data-collector is guided and supported by the
SendGrid `Developer Experience Team <mailto:dx@sendgrid.com>`__.

open-source-library-data-collector is maintained and funded by SendGrid,
Inc. The names and logos for open-source-library-data-collector are
trademarks of SendGrid, Inc.

|SendGrid Logo|

.. |SendGrid Logo| image:: https://uiux.s3.amazonaws.com/2016-logos/email-logo%402x.png
   :target: https://www.sendgrid.com
.. |Travis Badge| image:: https://travis-ci.org/sendgrid/open-source-library-data-collector.svg?branch=master
   :target: https://travis-ci.org/sendgrid/open-source-library-data-collector
