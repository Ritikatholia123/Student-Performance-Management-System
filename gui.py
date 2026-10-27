import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# =========================================================
# DATABASE CONNECTION
# =========================================================

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ritika@12",
        database="student_db"
    )

except mysql.connector.Error as error:
    connection = None
    print("Database Error:", error)


# =========================================================
# DATABASE CHECK
# =========================================================

def check_database():
    if connection is None or not connection.is_connected():
        messagebox.showerror(
            "Database Error",
            "MySQL database is not connected.\nPlease start MySQL Server."
        )
        return False

    return True


# =========================================================
# ADD STUDENT
# =========================================================

def open_add_student():

    if not check_database():
        return

    window = tk.Toplevel(root)
    window.title("Add Student")
    window.geometry("500x550")
    window.resizable(False, False)

    tk.Label(
        window,
        text="ADD NEW STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Student Name").pack()
    name_entry = tk.Entry(window, width=40)
    name_entry.pack(pady=7)

    tk.Label(window, text="Age").pack()
    age_entry = tk.Entry(window, width=40)
    age_entry.pack(pady=7)

    tk.Label(window, text="Course").pack()
    course_entry = tk.Entry(window, width=40)
    course_entry.pack(pady=7)

    tk.Label(window, text="Marks").pack()
    marks_entry = tk.Entry(window, width=40)
    marks_entry.pack(pady=7)

    tk.Label(window, text="Email").pack()
    email_entry = tk.Entry(window, width=40)
    email_entry.pack(pady=7)

    def save_student():

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        course = course_entry.get().strip()
        marks = marks_entry.get().strip()
        email = email_entry.get().strip()

        if not name or not age or not course or not marks or not email:
            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields."
            )
            return

        try:
            age = int(age)
            marks = float(marks)

            if marks < 0 or marks > 100:
                messagebox.showwarning(
                    "Invalid Marks",
                    "Marks must be between 0 and 100."
                )
                return

            cursor = connection.cursor()

            query = """
            INSERT INTO students
            (name, age, course, marks, email)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                name,
                age,
                course,
                marks,
                email
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            window.destroy()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Age and Marks must be numbers."
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        window,
        text="SAVE STUDENT",
        width=20,
        height=2,
        command=save_student
    ).pack(pady=30)


# =========================================================
# VIEW ALL STUDENTS
# =========================================================

def view_students():

    if not check_database():
        return

    window = tk.Toplevel(root)
    window.title("All Students")
    window.geometry("950x500")

    tk.Label(
        window,
        text="ALL STUDENTS",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    columns = (
        "ID",
        "Name",
        "Age",
        "Course",
        "Marks",
        "Email"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=140)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students ORDER BY student_id"
        )

        students = cursor.fetchall()

        for student in students:
            table.insert(
                "",
                tk.END,
                values=student
            )

        cursor.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    if not check_database():
        return

    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("850x500")

    tk.Label(
        window,
        text="SEARCH STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    tk.Label(
        window,
        text="Enter Student ID, Name or Course"
    ).pack()

    search_entry = tk.Entry(
        window,
        width=40
    )

    search_entry.pack(pady=10)

    columns = (
        "ID",
        "Name",
        "Age",
        "Course",
        "Marks",
        "Email"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=120)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    def search():

        for item in table.get_children():
            table.delete(item)

        value = search_entry.get().strip()

        if not value:
            messagebox.showwarning(
                "Search",
                "Please enter something to search."
            )
            return

        try:

            cursor = connection.cursor()

            student_id = value if value.isdigit() else -1
            search_text = "%" + value + "%"

            query = """
            SELECT * FROM students
            WHERE student_id = %s
            OR name LIKE %s
            OR course LIKE %s
            """

            cursor.execute(
                query,
                (
                    student_id,
                    search_text,
                    search_text
                )
            )

            students = cursor.fetchall()

            if not students:

                messagebox.showinfo(
                    "Result",
                    "Student not found."
                )

            else:

                for student in students:
                    table.insert(
                        "",
                        tk.END,
                        values=student
                    )

            cursor.close()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        window,
        text="SEARCH",
        width=15,
        command=search
    ).pack(pady=5)


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():

    if not check_database():
        return

    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("500x550")

    tk.Label(
        window,
        text="UPDATE STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Student ID"
    ).pack()

    id_entry = tk.Entry(
        window,
        width=35
    )

    id_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Course"
    ).pack()

    course_entry = tk.Entry(
        window,
        width=35
    )

    course_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Marks"
    ).pack()

    marks_entry = tk.Entry(
        window,
        width=35
    )

    marks_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Email"
    ).pack()

    email_entry = tk.Entry(
        window,
        width=35
    )

    email_entry.pack(pady=5)

    tk.Label(
        window,
        text="Enter the new values for all three fields."
    ).pack(pady=10)

    def update():

        student_id = id_entry.get().strip()
        course = course_entry.get().strip()
        marks = marks_entry.get().strip()
        email = email_entry.get().strip()

        if not student_id or not course or not marks or not email:

            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields."
            )

            return

        try:

            student_id = int(student_id)
            marks = float(marks)

            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM students WHERE student_id = %s",
                (student_id,)
            )

            student = cursor.fetchone()

            if student is None:

                messagebox.showerror(
                    "Not Found",
                    "Student ID not found."
                )

                cursor.close()
                return

            query = """
            UPDATE students
            SET course = %s,
                marks = %s,
                email = %s
            WHERE student_id = %s
            """

            cursor.execute(
                query,
                (
                    course,
                    marks,
                    email,
                    student_id
                )
            )

            connection.commit()

            cursor.close()

            messagebox.showinfo(
                "Success",
                "Student updated successfully!"
            )

            window.destroy()

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Student ID and Marks must be numbers."
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        window,
        text="UPDATE STUDENT",
        width=20,
        height=2,
        command=update
    ).pack(pady=30)


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    if not check_database():
        return

    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("450x300")

    tk.Label(
        window,
        text="DELETE STUDENT",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Student ID"
    ).pack()

    id_entry = tk.Entry(
        window,
        width=30
    )

    id_entry.pack(pady=10)

    def delete():

        try:

            student_id = int(
                id_entry.get()
            )

            cursor = connection.cursor()

            cursor.execute(
                "SELECT name FROM students WHERE student_id = %s",
                (student_id,)
            )

            student = cursor.fetchone()

            if student is None:

                messagebox.showerror(
                    "Not Found",
                    "Student not found."
                )

                cursor.close()
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete {student[0]}?"
            )

            if confirm:

                cursor.execute(
                    "DELETE FROM students WHERE student_id = %s",
                    (student_id,)
                )

                connection.commit()

                messagebox.showinfo(
                    "Success",
                    "Student deleted successfully!"
                )

                window.destroy()

            cursor.close()

        except ValueError:

            messagebox.showerror(
                "Invalid ID",
                "Please enter a valid Student ID."
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        window,
        text="DELETE",
        width=20,
        height=2,
        command=delete
    ).pack(pady=20)


# =========================================================
# PERFORMANCE REPORT
# =========================================================

def performance_report():

    if not check_database():
        return

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            COUNT(*),
            AVG(marks),
            MAX(marks),
            MIN(marks),
            SUM(CASE WHEN marks >= 40 THEN 1 ELSE 0 END),
            SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END)
        FROM students
        """

        cursor.execute(query)

        report = cursor.fetchone()

        cursor.close()

        if report[0] == 0:

            messagebox.showinfo(
                "Performance Report",
                "No student records found."
            )

            return

        window = tk.Toplevel(root)

        window.title(
            "Performance Report"
        )

        window.geometry(
            "600x500"
        )

        tk.Label(
            window,
            text="STUDENT PERFORMANCE REPORT",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        tk.Label(
            window,
            text=f"Total Students : {report[0]}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            window,
            text=f"Average Marks : {float(report[1]):.2f}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            window,
            text=f"Highest Marks : {report[2]}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            window,
            text=f"Lowest Marks : {report[3]}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            window,
            text=f"Passed Students : {report[4]}",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            window,
            text=f"Failed Students : {report[5]}",
            font=("Arial", 14)
        ).pack(pady=10)

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Student Performance Management System"
)

root.geometry(
    "900x600"
)

root.resizable(
    False,
    False
)


# =========================================================
# HEADER
# =========================================================

heading = tk.Label(
    root,
    text="STUDENT PERFORMANCE MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold")
)

heading.pack(
    pady=30
)

subtitle = tk.Label(
    root,
    text="Student Management Dashboard",
    font=("Arial", 14)
)

subtitle.pack(
    pady=5
)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=40
)


# =========================================================
# BUTTONS
# =========================================================

add_btn = tk.Button(
    button_frame,
    text="➕ Add Student",
    width=22,
    height=2,
    command=open_add_student
)

add_btn.grid(
    row=0,
    column=0,
    padx=20,
    pady=15
)


view_btn = tk.Button(
    button_frame,
    text="👥 View Students",
    width=22,
    height=2,
    command=view_students
)

view_btn.grid(
    row=0,
    column=1,
    padx=20,
    pady=15
)


search_btn = tk.Button(
    button_frame,
    text="🔍 Search Student",
    width=22,
    height=2,
    command=search_student
)

search_btn.grid(
    row=1,
    column=0,
    padx=20,
    pady=15
)


update_btn = tk.Button(
    button_frame,
    text="✏ Update Student",
    width=22,
    height=2,
    command=update_student
)

update_btn.grid(
    row=1,
    column=1,
    padx=20,
    pady=15
)


delete_btn = tk.Button(
    button_frame,
    text="🗑 Delete Student",
    width=22,
    height=2,
    command=delete_student
)

delete_btn.grid(
    row=2,
    column=0,
    padx=20,
    pady=15
)


report_btn = tk.Button(
    button_frame,
    text="📊 Performance Report",
    width=22,
    height=2,
    command=performance_report
)

report_btn.grid(
    row=2,
    column=1,
    padx=20,
    pady=15
)


exit_btn = tk.Button(
    root,
    text="EXIT",
    width=22,
    height=2,
    command=root.destroy
)

exit_btn.pack(
    pady=15
)


# =========================================================
# DATABASE STATUS
# =========================================================

if connection is not None and connection.is_connected():

    status_text = "● Database Connected"

else:

    status_text = "● Database Not Connected"


status_label = tk.Label(
    root,
    text=status_text,
    font=("Arial", 10)
)

status_label.pack(
    pady=10
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()


# =========================================================
# CLOSE DATABASE CONNECTION
# =========================================================

if connection is not None and connection.is_connected():
    connection.close()