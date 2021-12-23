"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from app.views import web
from app import db
from app.models import Employee
from app.service.services import DepartmentService, EmployeeService

from flask import render_template, url_for, request, flash, redirect
from sqlalchemy import func
from datetime import date


menu = {"Home": "web.index", "Departments": "web.departments", "Employee": "web.employee",
        "Employees": "web.employees"}
footer = "http://bengusta.com.ua"



@web.route("/")
@web.route("/index")
def index():
    return render_template("index.html",
                           menu=menu,
                           title="Search for employees in depts",
                           pagename="Homepage",
                           footer=footer)

@web.route("/departments", defaults={'page_num': 1})
@web.route("/departments/<int:page_num>")
def departments(page_num):

    dept_salary = DepartmentService.get_avg_salary()\
        .paginate(per_page=2, page=page_num, error_out=True)

    return render_template("departments.html",
                           route_name="web.departments",
                           dept_salary=dept_salary,
                           menu=menu, title="Departments",
                           pagename="departments", footer="link")

@web.route("/department/<dept_name>/", defaults={'page_num': 1})
@web.route("/department/<dept_name>/<int:page_num>")
def department(dept_name, page_num):
    if_exists = DepartmentService.get_all().get_or_404(dept_name)
    page_name = if_exists.name
    dept_data = db.session.query \
                (Employee.name, Employee.surname, Employee.date_of_bidth, Employee.salary) \
                .select_from(Employee).filter_by(dept_name=dept_name) \
                .paginate(per_page=2, page=page_num, error_out=True) \

    return render_template("department.html",
                           route_name="web.department",
                           menu=menu,
                           dept_name=dept_name,
                           dept_data=dept_data,
                           body=page_name.capitalize(),
                           title=page_name.capitalize(),
                           footer="link")


@web.route("/employees")
def employees():
    page_num = request.args.get("page_num", 1, type=int)
    column_names = Employee.__table__.columns.keys()[1:]

    emp_data = db.session\
                .query(Employee)\
                .order_by(Employee.dept_name)\
                .paginate(per_page=2, page=page_num, error_out=True)

    return render_template("employees.html",
                           route_name="web.employees",
                           column_names=column_names,
                           emp_data=emp_data,
                           date_today=date.today(),
                           menu=menu,
                           title="List of all employees",
                           pagename="employee list",
                           footer="link")


@web.route("/employees/search", methods=["GET", "POST"])
def search():
    page_num = request.args.get('page_num', 1, type=int)
    column_names = Employee.__table__.columns.keys()[1:]

    birthday_start = request.args.get("birthday_start", type=str)
    birthday_finish = request.args.get("birthday_finish", type=str)

    if request.method == "POST":
        birthday_start = request.form["birthday_start"]
        birthday_finish = request.form["birthday_finish"]

        filtered_result = db.session \
            .query(Employee) \
            .filter(Employee.date_of_bidth >= birthday_start) \
            .filter(Employee.date_of_bidth <= birthday_finish) \
            .order_by(Employee.dept_name) \
            .paginate(per_page=2, page=page_num, error_out=True)

        return render_template("employees.html",
                               route_name="web.search",
                               column_names=column_names,
                               birthday_start=birthday_start,
                               birthday_finish=birthday_finish,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               menu=menu,
                               title="List of all employees", pagename="employee list",
                               footer="link")

    elif birthday_start or birthday_finish:
        filtered_result = db.session \
            .query(Employee) \
            .filter(Employee.date_of_bidth >= birthday_start) \
            .filter(Employee.date_of_bidth <= birthday_finish) \
            .order_by(Employee.dept_name) \
            .paginate(per_page=2, page=page_num, error_out=True)

        return render_template("employees.html",
                               route_name="web.search",
                               column_names=column_names,
                               birthday_start=birthday_start,
                               birthday_finish=birthday_finish,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               menu=menu,
                               title="List of all employees", pagename="employee list",
                               footer="link")


@web.route("/employees/edit", methods=["GET", "POST"])
def edit_employee():
    data_from_form = request.form

    find_department = DepartmentService.get_by_name(data_from_form["dept_name"])
    if not find_department:
        DepartmentService.add_dept(data_from_form["dept_name"])

    EmployeeService.edit_emp(data_from_form["id"], data_from_form)
    return redirect(url_for("web.employees"))

@web.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    data_from_form = request.form
    find_department = DepartmentService.get_by_name(data_from_form["dept_name"])

    if not find_department:
        DepartmentService.add_dept(data_from_form["dept_name"])
    EmployeeService.add_emp(**data_from_form)

    return redirect(url_for("web.employees"))


@web.route("/employees/delete", methods=["GET", "POST"])
def delete_employee():
    delete_id = request.form["id"]
    result = db.session.query(Employee).filter_by(id=delete_id).delete()
    db.session.commit()

    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.employees"))


@web.route("/employee", methods=["POST"])
def employee():
    return render_template("employee.html", menu=menu, title="Employee",
                           pagename="Employee details", footer="link")

@web.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html", menu=menu, title="404 page not found", footer="link"), \
           404
