"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from app.views import web
from app.service.services import EmployeeService as emp_servie

from datetime import date
from flask import render_template, url_for, request, flash, redirect


@web.route("/employees")
def employees():
    page = request.args.get("page", 1, type=int)
    emp_data = emp_servie.get_all(paginate=True, page=page, per_page=3)

    return render_template("employees.html",
                           route_name="web.employees",
                           emp_data=emp_data,
                           date_today=date.today(),
                           title="List of all employees",
                           pagename="employee list")


@web.route("/employees/search", methods=["GET", "POST"])
def search():
    page = request.args.get('page', 1, type=int)

    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)

    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        filtered_result = emp_servie.search_by_date(paginate=True, page=page, per_page=2,
                                                        start_date=start_date, end_date=end_date)

        return render_template("employees.html",
                               route_name="web.search",
                               start_date=start_date,
                               end_date=end_date,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               title="List of all employees", pagename="employee list")

    elif start_date or end_date:
        filtered_result = emp_servie.search_by_date(paginate=True, page=page, per_page=2,
                                                         start_date=start_date, end_date=end_date)

        return render_template("employees.html",
                               route_name="web.search",
                               start_date=start_date,
                               end_date=end_date,
                               emp_data=filtered_result,
                               date_today=date.today(),
                               title="List of all employees", pagename="employee list")


@web.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    validated = emp_servie.validate(request.form)
    if not isinstance(validated, dict):
        flash(f"Can't add this entry {validated}")
        return redirect(url_for("web.employees"))

    emp_servie.add_entry(validated)
    return redirect(url_for("web.employees"))


@web.route("/employees/edit", methods=["GET", "POST"])
def edit_employee():
    validated = emp_servie.validate(request.form)
    if isinstance(validated, str):
        flash(f"Could not edit the entry: {validated}")
    else:
        result = emp_servie.edit_entry(validated)
        if not result:
            flash("Couldn't edit the entry: check if such employee exist.")
    return redirect(url_for("web.employees"))


@web.route("/employees/delete", methods=["GET", "POST"])
def delete_employee():
    entry_id = request.form["id"]
    result = emp_servie.delete_by_id(entry_id)

    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.employees"))
