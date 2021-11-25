# Software Requirements Specification (SRS)

The file contains a description of a software system to be developed with all applicable use cases. The specification document includes forms mockups too.

## Project Requirements

Create a static mockup version of the application in HTML format with hardcoded data. It must include a minimum of 4 pages: 

- departments.html
- department.html 
- employees.html
- employee.html 

All pages have to include hyperlinks to simulate application use cases. Inside "documentation" folder create folder "html_prototype" and push static prototype there.

### Tech Stack
LAMP 
- Linux – Ubuntu 20.04;
- Apache2 – interact via Gunicorn WSGQ;
- MySQL – SQLAlchemy as ORM or DBAPI mysql-connector-python;
- Python – the app is based on based on Flask micro-framework.

*Apache2 – not required but I want to implement for a better software life-circle understanding*

*Also mysql-connector-python suggested as DBAPI, I’d like to test speed of mysqlclien or PyMySQL – as those are recommended by SQLAlchemy team*
 

### Project structure

department-app (a project / app directory)
|__ migrations (this package must include migration files to manage database schema changes )
|__ models (this package must include modules with Python classes describing DB models (for ORM only))
|__ service (this package must include modules with functions / classes to work with DB (CRUD operations))
|__ sql (this folder must include *.sql files to work with DB (for non-ORM only))
|__ rest (this package must include modules with RESTful service implementation)
|__ templates (this folder must include web app html templates)
|__ static (this folder must include static files (js, css, images, etc,))
|__ tests (this package must include modules with unit tests)
|__ views (this package must include modules with Web controllers / views)

+ setup.py
+ requirements.txt

## Project Scope
This is a simple web application for managing departments and employees. The web application uses aforementioned web service for storing data and reading from database. 

One is able to deploy the web application on Gunicorn using command line. All public functions / methods on all levels should include unit tests. Debug information should be displayed at the debugging level in the console and in a separate file. Classes and functions / methods must have docstrings comments. 

The README file contains a brief description of the project, instructions on how to build a project from the command line, how to start it, and at what addresses the Web service and the Web application will be available after launch.

The web application allows:
	1.	display a list of departments and the average salary (calculated automatically) for these departments
	2.	display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates
	3.	change (add / edit / delete) the above data


### DB
- Two tables: "department" and "employee"
- DB is populated with test data
- Departments table stores depts. names
- Employees table stores the following data: related department, employee name, date of birth, salary

	1.	Configure your application to connect to the required db.
	2.	If you chosen ORM technology to work with db (SQLAlchemy), you should create models and then generate migration scripts to manage database schema changes . You should use special Python modules or corresponding features of the chosen technology to generate migration scripts automatically or manually based on created modules.
### Web service

Create a web service (RESTful) for CRUD operations. One should be able to deploy the web service on Gunicorn using command line.

###### Check-list
- Web service has been deployed and runs on local instance
- Web service returns data stored in the database
- It is able to make rest calls from command line and other client tools
- Unit tests created
- Debug information is displayed at the debugging level in the console and in a separate file
- Classes and functions / methods have docstrings comments
- Gunicorn configured properly
- Create pull request(s) in GitHub.
- Travis-CI build was successfull after merging the pull request(s)


## CI/CD
	•	Project build configuration should include "pylint" plugin
	•	Use https://travis-ci.comfor building the project on github
	•	Set up and add https://coveralls.io

###### Check-list
Project has been successfully built with travis-ci
Code quality metrics can be calculated
Code coverage is available on coveralls.io
Create pull request(s) in GitHub.
Travis-CI build was successfull after merging the pull request(s)

All public functions / methods on all levels should include unit tests. Debug information should be displayed at the debugging level in the console and in a separate file. Classes and functions / methods must have docstrings comments.
black