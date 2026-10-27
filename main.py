import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritika@12",
        database="student_db"
    )

    if connection.is_connected():
        print("✅ Database connected successfully!")

except mysql.connector.Error as error:
    print("❌ Database connection failed!")
    print("Error:", error)

# Student function
def add_student():
    try:
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        course = input("Enter course: ")
        marks = float(input("Enter marks: "))
        email = input("Enter email: ")

        cursor = connection.cursor()

        query = """
        INSERT INTO students (name,age,course,marks,email)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (name,age,course,marks,email)

        cursor.execute(query,values)
        connection.commit()

        print("✅ Student added successfully!")

    except ValueError:
        print("❌Please enter valid age and marks.")

    except mysql.connector.Error as Error:
        print("❌Error",error)

def view_students():
    cursor = connection.cursor()

    query = "SELECT * FROM students"
    cursor.execute(query)

    students = cursor.fetchall()

    if len(students) == 0:
        print("❌ No students found!")
    else:
        print("\n===== ALL STUDENTS =====")

        for student in students:
            print("------------------------------")
            print("Student ID :", student[0])
            print("Name       :", student[1])
            print("Age        :", student[2])
            print("Course     :", student[3])
            print("Marks      :", student[4])
            print("Email      :", student[5])
    
def search_student():
    search = input("Enter Student ID, Name or Course: ")

    cursor = connection.cursor()

    query = """
    SELECT * FROM students
    WHERE student_id = %s
       OR name LIKE %s
       OR course LIKE %s
    """

    student_id = search if search.isdigit() else -1
    search_text = "%" + search + "%"

    values = (student_id, search_text, search_text)

    cursor.execute(query, values)
    students = cursor.fetchall()

    if len(students) == 0:
        print("❌ Student not found!")
    else:
        print("\n===== SEARCH RESULTS =====")

        for student in students:
            print("------------------------------")
            print("Student ID :", student[0])
            print("Name       :", student[1])
            print("Age        :", student[2])
            print("Course     :", student[3])
            print("Marks      :", student[4])
            print("Email      :", student[5])

def update_student():
    try:
        student_id = int(input("Enter Student ID to update: "))

        cursor = connection.cursor()

        # Check student exists
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if student is None:
            print("❌ Student not found!")
            return

        print("\nStudent Found:", student[1])

        print("\nWhat do you want to update?")
        print("1. Marks")
        print("2. Email")
        print("3. Course")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_marks = float(input("Enter new marks: "))

            query = "UPDATE students SET marks = %s WHERE student_id = %s"
            cursor.execute(query, (new_marks, student_id))

        elif choice == "2":
            new_email = input("Enter new email: ")

            query = "UPDATE students SET email = %s WHERE student_id = %s"
            cursor.execute(query, (new_email, student_id))

        elif choice == "3":
            new_course = input("Enter new course: ")

            query = "UPDATE students SET course = %s WHERE student_id = %s"
            cursor.execute(query, (new_course, student_id))

        else:
            print("❌ Invalid choice!")
            return

        connection.commit()
        print("✅ Student updated successfully!")

    except ValueError:
        print("❌ Please enter a valid Student ID or marks.")
def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))

        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if student is None:
            print("❌ Student not found!")
            return

        print("Student Found:", student[1])

        confirm = input("Are you sure you want to delete? (yes/no): ")

        if confirm.lower() == "yes":
            query = "DELETE FROM students WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            connection.commit()

            print("✅ Student deleted successfully!")
        else:
            print("❌ Delete cancelled!")

    except ValueError:
        print("❌ Please enter a valid Student ID.")

def performance_report():
    cursor = connection.cursor()

    query = """
    SELECT
        AVG(marks),
        MAX(marks),
        MIN(marks),
        SUM(CASE WHEN marks >= 40 THEN 1 ELSE 0 END),
        SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END)
    FROM students
    """

    cursor.execute(query)
    report = cursor.fetchone()

    if report[0] is None:
        print("❌ No student records found!")
    else:
        print("\n===== PERFORMANCE REPORT =====")
        print("Average Marks :", round(float(report[0]), 2))
        print("Highest Marks :", report[1])
        print("Lowest Marks  :", report[2])
        print("Pass Students :", report[3])
        print("Fail Students :", report[4])
#main menu
while True:
    print("\n===== STUDENT PERFORMANCE MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Performance Report")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        performance_report()

    elif choice == "7":
        print("Thank you!")
        break

    else:
        print("❌ Invalid choice!")