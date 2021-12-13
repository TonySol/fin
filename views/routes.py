"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from flask import current_app, render_template, url_for, request, flash, redirect
from sqlalchemy import func


def routes(app, db, model):
    menu = {'Home': 'index', "Departments": "departments", "Employee": "employee",
            "Employees": "employees"}
    footer = "http://bengusta.com.ua"

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html", menu=menu,
                               title="Search for employees in depts",
                               pagename="Homepage",
                               footer=footer)

    @app.route("/departments", defaults={'page_num': 1})
    @app.route("/departments/page/<int:page_num>")
    def departments(page_num):
        Department = model.Department
        Employee = model.Employee

        dept_salary = db.session.query(Department.name, func.avg(Employee.salary)) \
            .select_from(Department).join(Employee) \
            .group_by(Department.name) \
            .paginate(per_page=2, page=page_num, error_out=True) \

        return render_template("departments.html", route_name="departments",
                               dept_salary=dept_salary,
                               menu=menu, title="Departments",
                               pagename="departments", footer="link")

    @app.route("/department/<dept_name>/", defaults={'page_num': 1})
    @app.route("/department/<dept_name>/page/<int:page_num>")
    def department(dept_name, page_num):
        Department = model.Department
        Employee = model.Employee

        dept_name_db = Department.query.filter_by(name=dept_name).first_or_404().name
        dept_data = db.session.query \
                    (Employee.name, Employee.surname, Employee.date_of_bidth, Employee.salary) \
                    .select_from(Employee).filter_by(dept_name=dept_name) \
                    .paginate(per_page=2, page=page_num, error_out=True) \

        return render_template("department.html", route_name="department",
                               menu=menu, dept_name=dept_name,
                               dept_data=dept_data,
                               body=dept_name_db.capitalize(),
                               title=dept_name_db.capitalize(),
                               footer="link")

    @app.route("/employees", defaults={'page_num': 1})
    @app.route("/employees/page/<int:page_num>")
    def employees(page_num):
        column_names = model.Employee.__table__.columns.keys()
        emp_data = model.Employee.query.paginate(per_page=2, page=page_num, error_out=True)

        return render_template("employees.html", route_name="employees",
                               column_names=column_names,
                               emp_data=emp_data,
                               menu=menu,
                               title="List of all employees", pagename="employee list",
                               footer="link")

    @app.route("/employee", methods=["GET", "POST"])
    def employee():
        return render_template("employee.html", menu=menu, title="Employee",
                               pagename="Employee details", footer="link")

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("404.html", menu=menu, title="404 page not found", footer="link"), \
               404
