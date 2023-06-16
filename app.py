from flask import Flask,jsonify,request, abort
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost:5433/Employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee_management(db.Model):
    __tablename__ = 'Employee_management'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db. Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    emailId = db.Column(db.String(100), nullable = False)

def __repr__(self):
        return "<Employee_management %r>" % self.first_name

if __name__ == '__main__':
  app.run(debug=True)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
        return jsonify({"message":"Welcome to my site"})


# Endpoint for creating a record
#  http://127.0.0.1:5000/employees
#{ "firstName"="hi", "lastName"="bye", emailId="aa@gmail.com" }
@app.route('/employee', methods = ['POST'])
def create_employee():
    employee_data = request.json

    firstName = employee_data['firstName']
    lastName = employee_data['lastName']
    
    emailId = employee_data['emailId']
    try:
        valid = validate_email(emailId)
        emailId = valid.email
    except:
        return jsonify({"success": False,"response":"Invalid email address"})


    employee = Employee_management(firstName =firstName , lastName = lastName, emailId = emailId )
    db.session.add(employee)
    db.session.commit()
    return jsonify({"success": True,"response":"Employee added"})
# Endpoint for geting a record
#  http://127.0.0.1:5000/getemployees
@app.route('/getemployees', methods = ['GET'])
def getemployees():
     all_employees = []
     employees = Employee_management.query.all()
     for employee in employees:
          results = {
                    "employee_id":employee.id,
                    "firstName":employee.firstName,
                    "lastName":employee.lastName,
                    "emailId":employee.emailId, }
          all_employees.append(results)

     return jsonify(
            {
                "success": True,
                "employees": all_employees,
                "total_employees": len(employees),
            }
        )
# Endpoint for updating a record
#  http://127.0.0.1:5000/employees/1
@app.route("/employee/<int:employee_id>", methods = ["PATCH"])
def update_employee(employee_id):
    employee = Employee_management.query.get(employee_id)
    firstName = request.json['firstName']
    emailId = request.json['emailId']

    if employee is None:
        abort(404)
    else:
        employee.firstName = firstName
        employee.emailId = emailId
        db.session.add(employee)
        db.session.commit()
        return jsonify({"success": True, "response": "Employee Details updated"})
    

    
# Endpoint for deleting a record
#  http://127.0.0.1:5000/employees/1
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
      employee = Employee_management.query.get(employee_id)
      if employee is None:
           abort(404)
      else:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"success": True, "response": "Employee Details deleted"})
    