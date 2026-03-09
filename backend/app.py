from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from datetime import datetime, timedelta
import re
import json
import numpy as np

# ================= APP CONFIG =================

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "jwt-secret"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)

CORS(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ================= MODELS =================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default="pending")

    face_encoding = db.Column(db.Text)


class Subject(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    year = db.Column(db.String(10))

    semester = db.Column(db.Integer)

    department = db.Column(db.String(50))


class TeacherSubject(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer)

    subject_id = db.Column(db.Integer)


class AttendanceSession(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer)

    subject_id = db.Column(db.Integer)

    year = db.Column(db.String(10))

    semester = db.Column(db.Integer)

    department = db.Column(db.String(50))

    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="active")


class AttendanceRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer)

    session_id = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ================= DATABASE INIT =================

with app.app_context():

    db.create_all()

    admin = User.query.filter_by(
        email="admin@eng.rizvi.edu.in"
    ).first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@eng.rizvi.edu.in",
            password="admin123",
            role="admin",
            status="approved"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created")


# ================= REGISTER =================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    email_pattern = r'^[a-zA-Z0-9._%+-]+@eng\.rizvi\.edu\.in$'

    if not re.match(email_pattern, data["email"]):

        return jsonify({"error": "Use college email"}), 400


    if User.query.filter_by(email=data["email"]).first():

        return jsonify({"error": "Email exists"}), 400


    user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        status="pending"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"})


# ================= LOGIN =================

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if user.status != "approved":
        return jsonify({"error": "Wait for admin approval"}), 403

    token = create_access_token(identity=user.id)

    return jsonify({
        "token": token,
        "id": user.id,
        "name": user.name,
        "role": user.role
    })


# ================= PENDING USERS =================

@app.route("/pending-users")
def pending_users():

    users = User.query.filter_by(status="pending").all()

    result = []

    for u in users:

        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        })

    return jsonify(result)


# ================= APPROVE USER =================

@app.route("/approve-user/<int:user_id>", methods=["POST"])
def approve_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.status = "approved"

    db.session.commit()

    return jsonify({"message": "User approved"})


# ================= GET TEACHERS =================

@app.route("/teachers")
def teachers():

    teachers = User.query.filter_by(
        role="teacher",
        status="approved"
    ).all()

    result = []

    for t in teachers:

        result.append({
            "id": t.id,
            "name": t.name
        })

    return jsonify(result)


# ================= INSERT SUBJECTS =================

@app.route("/insert-subjects")
def insert_subjects():

    subjects = [

        # ================= FE SEM 1 =================
        ("Engineering Mathematics I", "FE", 1, "ALL"),
        ("Engineering Physics I", "FE", 1, "ALL"),
        ("Engineering Chemistry I", "FE", 1, "ALL"),
        ("Engineering Mechanics", "FE", 1, "ALL"),
        ("Basic Electrical Engineering", "FE", 1, "ALL"),
        ("Engineering Graphics", "FE", 1, "ALL"),
        ("Programming in C", "FE", 1, "ALL"),
        ("Communication Skills", "FE", 1, "ALL"),

        # ================= FE SEM 2 =================
        ("Engineering Mathematics II", "FE", 2, "ALL"),
        ("Engineering Physics II", "FE", 2, "ALL"),
        ("Engineering Chemistry II", "FE", 2, "ALL"),
        ("Engineering Mechanics II", "FE", 2, "ALL"),
        ("Basic Electronics", "FE", 2, "ALL"),
        ("Environmental Engineering", "FE", 2, "ALL"),
        ("Python Programming", "FE", 2, "ALL"),
        ("Workshop Practice", "FE", 2, "ALL"),


        # ================= SE COMPUTER =================
        ("Discrete Mathematics", "SE", 3, "Computer"),
        ("Data Structures", "SE", 3, "Computer"),
        ("Digital Logic Design", "SE", 3, "Computer"),
        ("Computer Graphics", "SE", 3, "Computer"),

        ("Analysis of Algorithms", "SE", 4, "Computer"),
        ("Operating Systems", "SE", 4, "Computer"),
        ("Database Management Systems", "SE", 4, "Computer"),
        ("Microprocessors", "SE", 4, "Computer"),


        # ================= SE AIDS =================
        ("Statistics", "SE", 3, "AIDS"),
        ("Python Programming", "SE", 3, "AIDS"),
        ("Data Structures", "SE", 3, "AIDS"),
        ("Linear Algebra", "SE", 3, "AIDS"),

        ("Machine Learning", "SE", 4, "AIDS"),
        ("Database Systems", "SE", 4, "AIDS"),
        ("AI Fundamentals", "SE", 4, "AIDS"),
        ("Probability", "SE", 4, "AIDS"),


        # ================= SE MECHANICAL =================
        ("Thermodynamics", "SE", 3, "Mechanical"),
        ("Fluid Mechanics", "SE", 3, "Mechanical"),
        ("Manufacturing Process", "SE", 3, "Mechanical"),
        ("Machine Drawing", "SE", 3, "Mechanical"),

        ("Heat Transfer", "SE", 4, "Mechanical"),
        ("Kinematics", "SE", 4, "Mechanical"),
        ("Material Science", "SE", 4, "Mechanical"),
        ("Dynamics", "SE", 4, "Mechanical"),


        # ================= SE CIVIL =================
        ("Structural Analysis", "SE", 3, "Civil"),
        ("Geotechnical Engineering", "SE", 3, "Civil"),
        ("Surveying", "SE", 3, "Civil"),
        ("Fluid Mechanics", "SE", 3, "Civil"),

        ("Concrete Technology", "SE", 4, "Civil"),
        ("Transportation Engineering", "SE", 4, "Civil"),
        ("Environmental Engineering", "SE", 4, "Civil"),
        ("Hydrology", "SE", 4, "Civil"),


        # ================= SE ELECTRICAL =================
        ("Circuit Theory", "SE", 3, "Electrical"),
        ("Electrical Machines I", "SE", 3, "Electrical"),
        ("Electromagnetics", "SE", 3, "Electrical"),
        ("Network Analysis", "SE", 3, "Electrical"),

        ("Electrical Machines II", "SE", 4, "Electrical"),
        ("Control Systems", "SE", 4, "Electrical"),
        ("Power Systems", "SE", 4, "Electrical"),
        ("Measurements", "SE", 4, "Electrical"),


        # ================= TE COMPUTER =================
        ("Theory of Computation", "TE", 5, "Computer"),
        ("Computer Networks", "TE", 5, "Computer"),
        ("Web Development", "TE", 5, "Computer"),
        ("Software Engineering", "TE", 5, "Computer"),

        ("Compiler Design", "TE", 6, "Computer"),
        ("Distributed Systems", "TE", 6, "Computer"),
        ("Machine Learning", "TE", 6, "Computer"),
        ("Cloud Computing", "TE", 6, "Computer"),


        # ================= BE COMPUTER =================
        ("Artificial Intelligence", "BE", 7, "Computer"),
        ("Big Data", "BE", 7, "Computer"),
        ("Cyber Security", "BE", 7, "Computer"),
        ("Blockchain", "BE", 7, "Computer"),

        ("Deep Learning", "BE", 8, "Computer"),
        ("Data Science", "BE", 8, "Computer"),
        ("IoT", "BE", 8, "Computer"),
        ("Project", "BE", 8, "Computer"),
    ]


    inserted = 0

    for name, year, sem, dept in subjects:

        exists = Subject.query.filter_by(
            name=name,
            year=year,
            semester=sem,
            department=dept
        ).first()

        if not exists:

            db.session.add(
                Subject(
                    name=name,
                    year=year,
                    semester=sem,
                    department=dept
                )
            )

            inserted += 1

    db.session.commit()

    return {
        "message": "Subjects inserted",
        "count": inserted
    }


# ================= SUBJECT FILTER =================

@app.route("/subjects-filter")
def subjects_filter():

    year = request.args.get("year")

    semester = request.args.get("semester")

    department = request.args.get("department")

    subjects = Subject.query.filter(
        Subject.year == year,
        Subject.semester == int(semester),
        (Subject.department == department) |
        (Subject.department == "ALL")
    ).all()

    result = []

    for s in subjects:

        result.append({
            "id": s.id,
            "name": s.name
        })

    return jsonify(result)


# ================= ASSIGN SUBJECT =================

@app.route("/assign-subject", methods=["POST"])
def assign_subject():

    data = request.json

    exists = TeacherSubject.query.filter_by(
        teacher_id=data["teacher_id"],
        subject_id=data["subject_id"]
    ).first()

    if exists:
        return jsonify({"message": "Already assigned"})

    db.session.add(
        TeacherSubject(
            teacher_id=data["teacher_id"],
            subject_id=data["subject_id"]
        )
    )

    db.session.commit()

    return jsonify({"message": "Subject assigned"})


# ================= GET TEACHER SUBJECTS =================

@app.route("/teacher-subjects/<int:teacher_id>")
def teacher_subjects(teacher_id):

    assignments = TeacherSubject.query.filter_by(
        teacher_id=teacher_id
    ).all()

    result = []

    for a in assignments:

        subject = Subject.query.get(a.subject_id)

        if subject:
            result.append({
                "id": subject.id,
                "name": subject.name,
                "year": subject.year,
                "semester": subject.semester,
                "department": subject.department
            })

    return jsonify(result)

# ================= START SESSION =================

@app.route("/start-session", methods=["POST"])
def start_session():

    AttendanceSession.query.filter_by(
        status="active"
    ).update({"status": "ended"})

    data = request.json

    session = AttendanceSession(
        teacher_id=data["teacher_id"],
        subject_id=data["subject_id"],
        year=data["year"],
        semester=data["semester"],
        department=data["department"],
        status="active"
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({"message": "Session started"})


# ================= REGISTER FACE =================

@app.route("/register-face", methods=["POST"])
def register_face():

    data = request.json

    user = User.query.get(data["user_id"])

    if not user:
        return jsonify({"message": "User not found"})

    user.face_encoding = data["encoding"]

    db.session.commit()

    return jsonify({"message": "Face registered"})


# ================= MARK ATTENDANCE =================

@app.route("/mark-attendance", methods=["POST"])
def mark_attendance():

    student_id = request.json["student_id"]

    session = AttendanceSession.query.filter_by(
        status="active"
    ).first()

    if not session:
        return jsonify({"message": "No active session"})

    exists = AttendanceRecord.query.filter_by(
        student_id=student_id,
        session_id=session.id
    ).first()

    if exists:
        return jsonify({"message": "Already marked"})

    db.session.add(
        AttendanceRecord(
            student_id=student_id,
            session_id=session.id
        )
    )

    db.session.commit()

    return jsonify({"message": "Attendance marked"})


# ================= STUDENT ATTENDANCE =================

@app.route("/student-attendance/<int:student_id>")
def student_attendance(student_id):

    records = AttendanceRecord.query.filter_by(
        student_id=student_id
    ).all()

    result = []

    for r in records:

        session = AttendanceSession.query.get(r.session_id)

        subject = Subject.query.get(session.subject_id)

        result.append({
            "subject": subject.name,
            "date": session.start_time.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(result)

@app.route("/debug-users")
def debug_users():

    users = User.query.all()

    result = []

    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "face_registered": True if u.face_encoding else False
        })

    return jsonify(result)





@app.route("/match-face", methods=["POST"])
def match_face():

    try:

        data = request.json

        if not data or "encoding" not in data:
            return jsonify({
                "success": False,
                "message": "No encoding received"
            }), 400


        incoming_encoding = np.array(
            json.loads(data["encoding"])
        )


        users = User.query.filter(
            User.face_encoding != None
        ).all()


        for user in users:

            try:

                saved_encoding = np.array(
                    json.loads(user.face_encoding)
                )

                distance = np.linalg.norm(
                    saved_encoding - incoming_encoding
                )

                if distance < 0.6:

                    session = AttendanceSession.query.filter_by(
                        status="active"
                    ).first()

                    if not session:
                        return jsonify({
                            "success": False,
                            "message": "No active session"
                        })


                    # prevent duplicate attendance
                    exists = AttendanceRecord.query.filter_by(
                        student_id=user.id,
                        session_id=session.id
                    ).first()

                    if exists:
                        return jsonify({
                            "success": True,
                            "name": user.name,
                            "message": "Already marked"
                        })


                    record = AttendanceRecord(
                        student_id=user.id,
                        session_id=session.id
                    )

                    db.session.add(record)
                    db.session.commit()


                    return jsonify({
                        "success": True,
                        "name": user.name
                    })

            except Exception as inner_error:
                print("Encoding error:", inner_error)
                continue


        return jsonify({
            "success": False,
            "message": "Face not recognized"
        })


    except Exception as e:

        print("MATCH FACE ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500
    
# ================= RUN =================

if __name__ == "__main__":

    app.run(debug=True)