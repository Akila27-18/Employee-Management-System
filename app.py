
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Employee
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    department_filter = request.args.get('department')
    if department_filter:
        employees = Employee.query.filter_by(department=department_filter).all()
    else:
        employees = Employee.query.all()
    departments = db.session.query(Employee.department).distinct()
    return render_template('index.html', employees=employees, departments=departments)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        salary = request.form['salary']
        new_employee = Employee(name=name, position=position, department=department, salary=float(salary))
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.position = request.form['position']
        employee.department = request.form['department']
        employee.salary = float(request.form['salary'])
        db.session.commit()
        flash('Employee updated successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
