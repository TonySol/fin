"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from flask import current_app, render_template, url_for, request, flash, redirect
from sqlalchemy import func
from datetime import date


def routes(app, db, model):
    menu = {'Home': 'index', "Departments": "departments", "Employee": "employee",
            "Employees": "employees"}
    footer = "http://bengusta.com.ua"

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html",
                               menu=menu,
                               title="Search for employees in depts",
                               pagename="Homepage",
                               footer=footer)

    @app.route("/departments", defaults={'page_num': 1})
    @app.route("/departments/<int:page_num>")
    def departments(page_num):
        Department = model.Department
        Employee = model.Employee

        dept_salary = db.session.query(Department.name, func.avg(Employee.salary)) \
            .select_from(Department).join(Employee) \
            .group_by(Department.name) \
            .paginate(per_page=2, page=page_num, error_out=True) \

        return render_template("departments.html",
                               route_name="departments",
                               dept_salary=dept_salary,
                               menu=menu, title="Departments",
                               pagename="departments", footer="link")

    @app.route("/department/<dept_name>/", defaults={'page_num': 1})
    @app.route("/department/<dept_name>/<int:page_num>")
    def department(dept_name, page_num):
        Department = model.Department
        Employee = model.Employee

        dept_name_db = Department.query.filter_by(name=dept_name).first_or_404().name
        dept_data = db.session.query \
                    (Employee.name, Employee.surname, Employee.date_of_bidth, Employee.salary) \
                    .select_from(Employee).filter_by(dept_name=dept_name) \
                    .paginate(per_page=2, page=page_num, error_out=True) \

        return render_template("department.html",
                               route_name="department",
                               menu=menu,
                               dept_name=dept_name,
                               dept_data=dept_data,
                               body=dept_name_db.capitalize(),
                               title=dept_name_db.capitalize(),
                               footer="link")


    @app.route("/employees")
    def employees():
        page_num = request.args.get('page_num', 1, type=int)

        column_names = model.Employee.__table__.columns.keys()[1:]
        emp_data = db.session\
                    .query(model.Employee)\
                    .order_by(model.Employee.dept_name)\
                    .paginate(per_page=2, page=page_num, error_out=True)

        return render_template("employees.html",
                               route_name="employees",
                               column_names=column_names,
                               emp_data=emp_data,
                               date_today = date.today(),
                               menu=menu,
                               title="List of all employees",
                               pagename="employee list",
                               footer="link")


    @app.route("/employees/search", methods=["GET", "POST"])
    def search():
        page_num = request.args.get('page_num', 1, type=int)
        column_names = model.Employee.__table__.columns.keys()[1:]

        birthday_start = request.args.get('birthday_start', type=str)
        birthday_finish = request.args.get('birthday_finish', type=str)

        if request.method == 'POST':
            birthday_start = request.form["birthday_start"]
            birthday_finish = request.form["birthday_finish"]

            filtered_result = db.session \
                .query(model.Employee) \
                .filter(model.Employee.date_of_bidth >= birthday_start) \
                .filter(model.Employee.date_of_bidth <= birthday_finish) \
                .order_by(model.Employee.dept_name) \
                .paginate(per_page=2, page=page_num, error_out=True)
            print(birthday_start, birthday_finish)
            return render_template("employees.html",
                                   route_name="search",
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
                .query(model.Employee) \
                .filter(model.Employee.date_of_bidth >= birthday_start) \
                .filter(model.Employee.date_of_bidth <= birthday_finish) \
                .order_by(model.Employee.dept_name) \
                .paginate(per_page=2, page=page_num, error_out=True)

            return render_template("employees.html",
                                   route_name="search",
                                   column_names=column_names,
                                   birthday_start=birthday_start,
                                   birthday_finish=birthday_finish,
                                   emp_data=filtered_result,
                                   date_today=date.today(),
                                   menu=menu,
                                   title="List of all employees", pagename="employee list",
                                   footer="link")


    @app.route("/employees/add", methods=["GET", "POST"])
    def edit_employee():
        add_data = request.form.getlist()
        # db.session.add(Employee(name="Tony", surname="Sol", date_of_bidth="1995-02-02", salary=5000, dept_name="Julius"))
        #     *[i for i in add_data]
        return redirect(url_for("employees"))


    @app.route("/employees/delete", methods=["GET", "POST"])
    def delete_employee():
        delete_id = request.form["id"]

        result = db.session.query(model.Employee).filter_by(id=delete_id).delete()
        db.session.commit()

        if result > 0:
            flash('Entry has been deleted.', "success")
        else:
            flash('Could not delete the entry', "fail")

        return redirect(url_for("employees"))


    @app.route("/employee", methods=["POST"])
    def employee():
        return render_template("employee.html", menu=menu, title="Employee",
                               pagename="Employee details", footer="link")

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("404.html", menu=menu, title="404 page not found", footer="link"), \
               404
