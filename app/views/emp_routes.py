"""The module describes controllers in for department-related routes."""

from app.views import web
from app.service.services import EmployeeService as emp_servie

from datetime import date
from flask import render_template, url_for, request, flash, redirect, session


@web.route("/employees", defaults={'page': 1})
@web.route("/employees/<int:page>")
def employees(page):
    """Returns `employees.html` template for such url routes:
    `/employees` and `/employees/<page number>`

    :param page: page number to fetch service with pagination details
    :type page: int

    Supplies template with data obtained from service call
    :return: rendered `employees.html` template
    """

    emp_data = emp_servie.get_all(paginate=True, page=page, per_page=3)
    return render_template("employees.html", route_name="web.employees", emp_data=emp_data,
                           date_today=date.today(), title="List of all employees",
                           pagename="employee list")


@web.route("/employees/search", methods=["GET", "POST"])
def search():
    """Returns `employees.html` template for such url routes: `/employees/search`

    – page: page number to fetch service with pagination details. It is obtained from uri
    – session: apply session(cookies) to hold requested birth dates between pages

    On GET request:
    Obtains requested dates range (if provided) from session.
    Renders template with page specified for pagination
    On POST request:
    Supplies template with data, obtained from service call, with specified dates of birth

    :return: rendered `employees.html` template with entries, filtered by date, provided by service
    """
    page = request.args.get('page', 1, type=int)

    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        session["date"] = [start_date, end_date]

        filtered_result = emp_servie.search_by_date(paginate=True, page=page, per_page=2,
                                        start_date=start_date, end_date=end_date)

        return render_template("employees.html", route_name="web.search", emp_data=filtered_result,
                               date_today=date.today(), title="Search by birthday results",
                               pagename="employee list")


    elif session["date"]:
        start_date = session["date"][0]
        end_date = session["date"][1]
        filtered_result = emp_servie.search_by_date(paginate=True, page=page, per_page=2,
                                        start_date=start_date, end_date=end_date)

        return render_template("employees.html", route_name="web.search", emp_data=filtered_result,
                               date_today=date.today(), title="Search by birthday results",
                               pagename="employee list")


@web.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    """A route to call service and add department data. Redirects to `/employees` route

    On POST request validates form data and adds employee via service call.
    Flashes error message if validation fails.

    :return: redirect to the `/employees` route
    """
    validated = emp_servie.validate(request.form)
    if not isinstance(validated, dict):
        flash(f"Can't add this entry {validated}")
        return redirect(url_for("web.employees"))

    emp_servie.add_entry(validated)
    return redirect(url_for("web.employees"))


@web.route("/employees/edit", methods=["GET", "POST"])
def edit_employee():
    """A route to call service and edit employee data. Redirects to `/employees` route

   On POST request validates form data and edits employee's via service call.
   Flashes error message if validation fails. Flashes error message if service fails.

   :return: redirect to the `/employees` route
   """
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
    """A route to call service and deletes employee data. Redirects to `/employees` route

    – entry_id: fetches id from data provided by the user.
    Makes service call to delete employee on POST request.
    Flashes error message if deletion fails. Flashes success message if service succeeds.

    :return: redirect to the `/employees` route
    """
    entry_id = request.form["id"]
    result = emp_servie.delete_by_id(entry_id)

    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.employees"))
