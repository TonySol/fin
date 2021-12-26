"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from app.views import web
from app.service.services import DepartmentService, EmployeeService

from flask import abort, render_template, url_for, request, flash, redirect
from datetime import date

menu = {"Home": "web.index", "Departments": "web.departments", "Employees": "web.employees"}
footer = "http://bengusta.com.ua"


@web.route("/")
@web.route("/index")
def index():
    return render_template("index.html",
                           menu=menu,
                           title="Search for employees in depts",
                           pagename="Homepage",
                           footer=footer)


@web.route("/departments", defaults={'page': 1})
@web.route("/departments/<int:page>")
def departments(page):
    dept_salary = DepartmentService.get_avg_salary(paginate=True, page=page)

    return render_template("departments.html",
                           route_name="web.departments",
                           dept_salary=dept_salary,
                           menu=menu, title="Departments",
                           pagename="departments", footer="link")


@web.route("/department/<dept_name>/", defaults={'page': 1})
@web.route("/department/<dept_name>/<int:page>")
def department(dept_name, page):
    page_name = DepartmentService.get_by_prime_key(dept_name)
    if not page_name:
        abort(404)

    dept_data = EmployeeService.get_all_by_filters(paginate=True, page=page, dept_name=dept_name)

    return render_template("department.html",
                           route_name="web.department",
                           menu=menu,
                           dept_name=dept_name,
                           dept_data=dept_data,
                           body=page_name.name.capitalize(),
                           title=page_name.name.capitalize(),
                           footer="link")


@web.route("/employees")
def employees():
    page = request.args.get("page", 1, type=int)
    emp_data = EmployeeService.get_all(paginate=True, page=page, per_page=3)

    return render_template("employees.html",
                           route_name="web.employees",
                           emp_data=emp_data,
                           date_today=date.today(),
                           menu=menu,
                           title="List of all employees",
                           pagename="employee list",
                           footer="link")


@web.route("/employees/search", methods=["GET", "POST"])
def search():
    page = request.args.get('page', 1, type=int)

    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)

    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        filtered_result = EmployeeService.search_by_date(
            paginate=True, page=page, per_page=2,
            start_date=start_date, end_date=end_date)

        return render_template("employees.html",
                               route_name="web.search",
                               start_date=start_date,
                               end_date=end_date,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               menu=menu,
                               title="List of all employees", pagename="employee list",
                               footer="link")

    elif start_date or end_date:
        filtered_result = EmployeeService.search_by_date(paginate=True, page=page, per_page=2,
                                                         start_date=start_date, end_date=end_date)

        return render_template("employees.html",
                               route_name="web.search",
                               start_date=start_date,
                               end_date=end_date,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               menu=menu,
                               title="List of all employees", pagename="employee list",
                               footer="link")


@web.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    form_data = request.form
    find_department = DepartmentService.get_by_prime_key(form_data["dept_name"])

    if not find_department:
        DepartmentService.add_entry(name=form_data["dept_name"])
    EmployeeService.add_entry(**form_data)

    return redirect(url_for("web.employees"))


@web.route("/employees/edit", methods=["GET", "POST"])
def edit_employee():
    form_data = request.form

    find_department = DepartmentService.get_by_prime_key(form_data["dept_name"])
    if not find_department:
        DepartmentService.add_entry(form_data["dept_name"])

    EmployeeService.edit_entry(form_data)
    return redirect(url_for("web.employees"))


@web.route("/employees/delete", methods=["GET", "POST"])
def delete_employee():
    entry_id = request.form["id"]
    result = EmployeeService.delete_by_prime_key(entry_id)

    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.employees"))


@web.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html", menu=menu, title="404 page not found", footer="link"), \
           404
