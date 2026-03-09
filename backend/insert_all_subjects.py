from app import db, Subject, app

with app.app_context():

    subjects = [

    # ================= FE SEM 1 =================

    ("Engineering Mathematics I", "FE", 1, "ALL"),
    ("Engineering Physics I", "FE", 1, "ALL"),
    ("Engineering Chemistry I", "FE", 1, "ALL"),
    ("Basic Electrical Engineering", "FE", 1, "ALL"),
    ("Basic Electronics Engineering", "FE", 1, "ALL"),
    ("Engineering Mechanics", "FE", 1, "ALL"),
    ("Engineering Graphics", "FE", 1, "ALL"),
    ("Professional Communication & Ethics", "FE", 1, "ALL"),

    # ================= FE SEM 2 =================

    ("Engineering Mathematics II", "FE", 2, "ALL"),
    ("Engineering Physics II", "FE", 2, "ALL"),
    ("Engineering Chemistry II", "FE", 2, "ALL"),
    ("Programming for Problem Solving", "FE", 2, "ALL"),
    ("Basic Mechanical Engineering", "FE", 2, "ALL"),
    ("Environmental Studies", "FE", 2, "ALL"),
    ("Workshop Practice", "FE", 2, "ALL"),
    ("Engineering Drawing", "FE", 2, "ALL"),


    # ================= SE COMPUTER SEM 3 =================

    ("Data Structures", "SE", 3, "Computer"),
    ("Discrete Mathematics", "SE", 3, "Computer"),
    ("Digital Logic Design", "SE", 3, "Computer"),
    ("Computer Organization", "SE", 3, "Computer"),
    ("Database Management Systems", "SE", 3, "Computer"),
    ("Python Programming", "SE", 3, "Computer"),

    # ================= SE COMPUTER SEM 4 =================

    ("Analysis of Algorithms", "SE", 4, "Computer"),
    ("Operating Systems", "SE", 4, "Computer"),
    ("Computer Networks", "SE", 4, "Computer"),
    ("Microprocessors", "SE", 4, "Computer"),
    ("Software Engineering", "SE", 4, "Computer"),
    ("Web Development", "SE", 4, "Computer"),


    # ================= SE AIDS =================

    ("Data Structures", "SE", 3, "AIDS"),
    ("Statistics for Data Science", "SE", 3, "AIDS"),
    ("Machine Learning Basics", "SE", 4, "AIDS"),
    ("Data Visualization", "SE", 4, "AIDS"),


    # ================= SE MECHANICAL =================

    ("Engineering Mathematics III", "SE", 3, "Mechanical"),
    ("Thermodynamics", "SE", 3, "Mechanical"),
    ("Strength of Materials", "SE", 3, "Mechanical"),
    ("Theory of Machines", "SE", 4, "Mechanical"),
    ("Manufacturing Processes", "SE", 4, "Mechanical"),


    # ================= SE CIVIL =================

    ("Structural Engineering", "SE", 3, "Civil"),
    ("Surveying", "SE", 3, "Civil"),
    ("Concrete Technology", "SE", 4, "Civil"),
    ("Geotechnical Engineering", "SE", 4, "Civil"),


    # ================= SE ELECTRICAL =================

    ("Electrical Machines I", "SE", 3, "Electrical"),
    ("Network Theory", "SE", 3, "Electrical"),
    ("Power Electronics", "SE", 4, "Electrical"),
    ("Control Systems", "SE", 4, "Electrical"),


    # ================= TE COMPUTER =================

    ("Theory of Computation", "TE", 5, "Computer"),
    ("Database Management Systems Advanced", "TE", 5, "Computer"),
    ("Artificial Intelligence", "TE", 5, "Computer"),
    ("System Programming", "TE", 6, "Computer"),
    ("Cloud Computing", "TE", 6, "Computer"),


    # ================= TE AIDS =================

    ("Machine Learning", "TE", 5, "AIDS"),
    ("Deep Learning", "TE", 5, "AIDS"),
    ("Natural Language Processing", "TE", 6, "AIDS"),
    ("Computer Vision", "TE", 6, "AIDS"),


    # ================= TE MECHANICAL =================

    ("Heat Transfer", "TE", 5, "Mechanical"),
    ("CAD CAM", "TE", 5, "Mechanical"),
    ("Robotics", "TE", 6, "Mechanical"),
    ("Automobile Engineering", "TE", 6, "Mechanical"),


    # ================= TE CIVIL =================

    ("Structural Design", "TE", 5, "Civil"),
    ("Environmental Engineering", "TE", 5, "Civil"),
    ("Transportation Engineering", "TE", 6, "Civil"),
    ("Earthquake Engineering", "TE", 6, "Civil"),


    # ================= TE ELECTRICAL =================

    ("Power System II", "TE", 5, "Electrical"),
    ("Electrical Drives", "TE", 5, "Electrical"),
    ("Switchgear Protection", "TE", 6, "Electrical"),
    ("Renewable Energy Systems", "TE", 6, "Electrical"),


    # ================= BE COMPUTER =================

    ("Distributed Systems", "BE", 7, "Computer"),
    ("Blockchain Technology", "BE", 7, "Computer"),
    ("Machine Learning Advanced", "BE", 8, "Computer"),
    ("Internet of Things", "BE", 8, "Computer"),


    # ================= BE AIDS =================

    ("AI Systems", "BE", 7, "AIDS"),
    ("Deep Learning Advanced", "BE", 7, "AIDS"),
    ("AI Applications", "BE", 8, "AIDS"),
    ("Major Project", "BE", 8, "AIDS"),


    # ================= BE MECHANICAL =================

    ("Advanced Machine Design", "BE", 7, "Mechanical"),
    ("Automation Systems", "BE", 8, "Mechanical"),


    # ================= BE CIVIL =================

    ("Advanced Structural Design", "BE", 7, "Civil"),
    ("Infrastructure Engineering", "BE", 8, "Civil"),


    # ================= BE ELECTRICAL =================

    ("Advanced Power Systems", "BE", 7, "Electrical"),
    ("Power System Protection", "BE", 8, "Electrical"),

    ]


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


    db.session.commit()

    print("All subjects inserted successfully!")
