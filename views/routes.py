"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from flask import current_app, render_template, url_for, request, flash, redirect
from sqlalchemy import func


def routes(app, db, model):
    menu = {'Home': 'index', "Departments": "departments", "Employee": "employee", "Employees": "employees"}
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

        dept_salary = db.session.query(Department.name, func.avg(Employee.salary))\
                            .select_from(Department).join(Employee)\
                            .group_by(Department.name)\
                            .paginate(per_page=2, page=page_num, error_out=True)\

        # dept_salary = Department.query.\
        #                     join(Employee, Department.name == Employee.dept_name)\
        #                     .add_columns(func.avg(Employee.salary))\
        #                     .group_by(Department.name)\
        #                     .paginate(max_per_page=10)\

        return render_template("departments.html", column="name", dept_salary=dept_salary,
                               menu=menu, title="Departments",
                               pagename="departments", footer="link")


    @app.route("/department/<dept_name>")
    def department(dept_name):
        dept_details = model.Department.query.filter_by(name=dept_name).first_or_404().name
        return render_template("department.html", menu=menu,
                               body=dept_details.capitalize(),
                               title=dept_details.capitalize(),
                               footer="link")


    @app.route("/employees")
    def employees():
        row_names = model.Employee.__table__.columns.keys()
        person = model.Employee.query.all()
        emp_list = [i for i in person]

        return render_template("employees.html", row_names=row_names, emp_list=emp_list, menu=menu,
                               title="List of all employees", pagename="employee list", footer="link")

    @app.route("/employee", methods=["GET", "POST"])
    def employee():
        return render_template("employee.html", menu=menu, title="Employee",
                               pagename="Employee details", footer="link")

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("404.html", menu=menu, title="404 page not found", footer="link"), \
               404
