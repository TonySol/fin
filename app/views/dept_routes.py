from app.views import web

from app.service.services import DepartmentService as dept_service
from app.service.services import EmployeeService as emp_servie


from flask import abort, render_template, url_for, request, flash, redirect


@web.route("/departments", defaults={'page': 1})
@web.route("/departments/<int:page>")
def departments(page):
    dept_salary = dept_service.get_avg_salary(paginate=True, page=page)
    return render_template("departments.html",
                           route_name="web.departments",
                           dept_salary=dept_salary,
                           title="Departments")


@web.route("/department/<dept_name>/", defaults={'page': 1})
@web.route("/department/<dept_name>/<int:page>")
def department(dept_name, page):

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
    validated = dept_service.validate(request.form)
    if not isinstance(validated, dict):
        flash(f"Can't add this entry {validated}")
        return redirect(url_for("web.departments"))

    dept_service.add_entry(validated)
    return redirect(url_for("web.departments"))


@web.route("/department/edit", methods=["GET", "POST"])
def edit_department():
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
    result = dept_service.delete_by_id(request.form["id"])
    if result > 0:
        flash("Entry has been deleted.", "success")
    else:
        flash("Could not delete the entry", "fail")
    return redirect(url_for("web.departments"))
