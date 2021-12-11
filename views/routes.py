"""Here is a mini-constructor to create routes without Blueprints

We call this routes() from init.py and pass app as a parameter,
thus dealing with circular imports. Ha-ha!
"""

from flask import current_app, render_template, url_for, request, flash, redirect


def routes(app, db, model):
    menu = {'Home': 'index', "Departments": "departments", "Employee": "employee"}
    footer = "http://bengusta.com.ua"

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template("index.html", menu=menu,
                               title="Search for employees in depts",
                               pagename="Homepage",
                               footer=footer)

    @app.route("/departments")
    def departments():
        dept = model.Department.query.all()
        dept_list = [i.name for i in dept]
        return render_template("departments.html", column="name", dept_list=dept_list, menu=menu,
                               title="Departments", pagename="departments", footer="link")

    @app.route("/department/<dept>")
    def department(dept):
        dept_name = model.Department.query.filter_by(name=dept).first_or_404().name
        return render_template("department.html", menu=menu,
                               body=dept_name.capitalize(),
                               title=dept_name.capitalize(),
                               footer="link")


    @app.route("/employees")
    def employees():
        row_names = model.Employee.__table__.columns.keys()

        person = model.Employee.query.all()
        emp_list = [i.name for i in person]
        # for row in person:
        #     new_list = []
        #     for i in row_names:
        #         entry = row.i
        #         new_list.append(entry)
        #     emp_list.append(new_list)

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
