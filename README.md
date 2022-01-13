[![Build Status](https://app.travis-ci.com/TonySol/fin.svg?branch=main)](https://app.travis-ci.com/TonySol/fin)

[![Coverage Status](https://coveralls.io/repos/github/TonySol/fin/badge.svg?branch=main)](https://coveralls.io/github/TonySol/fin?branch=main)

A simple two-page web app to hold department and employee entries linked between.
REST API included. All the common methods are supplied via API and Web.

How to build:

Configure MySQL database requires following values:

DB_USER,
DB_PASSWORD, 
DB_SERVER, 
DB_DATABASE,

For your convenience, set env variable: FLASK_APP='run.py' 

Run migration to set up db accordingly:
_flask db upgrade_

Run project in local env: _python -m flask run_
