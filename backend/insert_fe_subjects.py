from app import db, Subject, app

with app.app_context():

    # FE Semester 1 Subjects
    fe_sem1 = [
        "Engineering Mathematics I",
        "Engineering Physics I",
        "Engineering Chemistry I",
        "Basic Electrical Engineering",
        "Basic Electronics Engineering",
        "Engineering Mechanics",
        "Engineering Graphics",
        "Professional Communication & Ethics"
    ]

    # FE Semester 2 Subjects
    fe_sem2 = [
        "Engineering Mathematics II",
        "Engineering Physics II",
        "Engineering Chemistry II",
        "Programming for Problem Solving",
        "Basic Mechanical Engineering",
        "Environmental Studies",
        "Workshop Practice",
        "Engineering Drawing"
    ]

    # Insert Semester 1
    for subject_name in fe_sem1:

        subject = Subject(
            name=subject_name,
            year="FE",
            semester=1,
            department="ALL"
        )

        db.session.add(subject)

    # Insert Semester 2
    for subject_name in fe_sem2:

        subject = Subject(
            name=subject_name,
            year="FE",
            semester=2,
            department="ALL"
        )

        db.session.add(subject)

    db.session.commit()

    print("FE Semester 1 and Semester 2 subjects inserted successfully!")
