"""The module describes controllers for department-related routes."""

from app.views import web

from app.service.services import DepartmentService as dept_service
from app.service.services import EmployeeService as emp_servie


from flask import abort, render_template, url_for, request, flash, redirect


@web.route("/departments", defaults={'page': 1})
@web.route("/departments/<int:page>")
def departments(page):
    """Returns `departments.html` template for such url routes:
    `/departments` and `/departments/<page number>`

    Supplies template with data obtained by service call
    :return: rendered `departments.html` template
    """
    dept_salary = dept_service.get_avg_salary(paginate=True, page=page)
    return render_template("departments.html",
                           route_name="web.departments",
                           dept_salary=dept_salary,
                           title="Departments")


@web.route("/department/<dept_name>/", defaults={'page': 1})
@web.route("/department/<dept_name>/<int:page>")
def department(dept_name, page):
    """Returns `department.html` template for such url routes:
    `/department/<dept_name>` and `/department/<dept_name>/<page number>`

    :param dept_name: the name of a requested department
    :type dept_name: str
    :param page: page number to fetch service with pagination details
    :type page: int


    Calls to service to search DB with `dept_name` parameter
    Supplies template with data obtained from service call

    :return: 404 if no department with `dept_name` parameter was found
    :return: rendered `department.html` template
    """
    dept_data = emp_servie.get_all_by_filters(paginate=True, page=page, dept_name=dept_name)
    if dept_data.total == 0:
        abort(404)

    return render_template("department.html",
                           route_name="web.department",
                           dept_name=dept_name,
                           dept_data=dept_data,
                           title=dept_name.capitalize())


@web.route("/department/add", methods=["GET", "POST"])
def add_department():
    """A route to call service and add department data. Redirects to `/departments` route

    On POST request validates form data and adds department via service call.
    Flashes error message if validation fails.

    :return: redirect to the `/departments` route
    """
    validated = dept_service.validate(request.form)
    if isinstance(validated, str):
        flash(f"Can't add this entry {validated}")
        return redirect(url_for("web.departments"))

    dept_service.add_entry(validated)
    return redirect(url_for("web.departments"))


@web.route("/department/edit", methods=["GET", "POST"])
def edit_department():
    """A route to call service and edit department data. Redirects to `/departments` route

    On POST request validates form data and edits department via service call.
    Flashes error message if validation fails. Flashes error message if service fails.

    :return: redirect to the `/departments` route
    """
    validated = dept_service.validate(request.form)
    if isinstance(validated, str):
        flash(f"Could not edit the entry: {validated}")
    else:
        result = dept_service.edit_entry(validated)
        if not result:
            flash(f"The department with {validated['id']} id does not exists.")
    return redirect(url_for("web.departments"))


@web.route("/department/delete", methods=["GET", "POST"])
def delete_department():
    """A route to call service and deletes department data. Redirects to `/departments` route

    – entry_id: fetches id from data provided by the user.
    Makes service call to delete department on POST request.
    Flashes error message if deletion fails. Flashes success message if service succeeds.

    :return: redirect to the `/departments` route
    """
    entry_id = request.form["id"]
    result = dept_service.delete_by_id(entry_id)
    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.departments"))
