from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data['name'], course=data['course'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"})

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []
    
    for student in students:
        output.append({
            "id": student.id,
            "name": student.name,
            "course": student.course
        })
    
    return jsonify(output)

# Update student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    
    if not student:
        return jsonify({"message": "Student not found"})
    
    data = request.json
    student.name = data.get('name', student.name)
    student.course = data.get('course', student.course)
    
    db.session.commit()
    
    return jsonify({"message": "Student updated successfully"})

# Delete student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    
    if not student:
        return jsonify({"message": "Student not found"})
    
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({"message": "Student deleted successfully"})

# Attendance Model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    date = db.Column(db.String(20))
    status = db.Column(db.String(10))

    # Mark attendance
@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    
    attendance = Attendance(
        student_id=data['student_id'],
        date=data['date'],
        status=data['status']
    )
    
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify({"message": "Attendance marked"})

@app.route('/attendance', methods=['GET'])
def get_attendance():
    records = Attendance.query.all()
    
    output = []
    
    for record in records:
        output.append({
            "id": record.id,
            "student_id": record.student_id,
            "date": record.date,
            "status": record.status
        })
    
    return jsonify(output)

@app.route('/createdb')
def create_db():
    db.create_all()
    return "Database created!"

if __name__ == "__main__":
    app.run(debug=True)