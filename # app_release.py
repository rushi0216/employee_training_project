import sqlite3
from datetime import datetime
import atexit

conn = sqlite3.connect("EmployeeTraining.db", timeout=10)
cursor = conn.cursor()
atexit.register(lambda: conn.close())
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables found:", cursor.fetchall())

def schedule_training():
    while True:
        training_id = input("Enter a unique Training ID: ")
        cursor.execute("SELECT 1 FROM Training WHERE Training_ID = ?", (training_id,))
        if cursor.fetchone():
            print(" Error: Training ID already exists. Please enter a new one.")
        else:
            break

    title = input("Enter Training Title: ")

    while True:
        scheduled_date = input("Enter Scheduled Date (MM-DD-YYYY): ")
        try:
            scheduled_dt = datetime.strptime(scheduled_date, "%m-%d-%Y").date()
            if scheduled_dt < datetime.today().date():
                print(" Scheduled date cannot be in the past.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use MM-DD-YYYY.")

    while True:
        start_time = input("Enter Start Time (e.g., 10:00 AM): ")
        end_time = input("Enter End Time (e.g., 12:00 PM): ")
        try:
            start_dt = datetime.strptime(start_time, "%I:%M %p")
            end_dt = datetime.strptime(end_time, "%I:%M %p")
            if end_dt <= start_dt:
                print(" End Time must be after Start Time.")
            else:
                break
        except ValueError:
            print(" Invalid time format. Please use format like '10:00 AM'.")

    duration = input("Enter Duration (e.g., 2 hours): ")

    try:
        cursor.execute("""
            INSERT INTO Training (Training_ID, Title, Scheduled_Date, Start_Time, End_Time, Duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (training_id, title, scheduled_date, start_time, end_time, duration))
        conn.commit()
        print(" Training scheduled successfully.")
    except Exception as e:
        print(f" Unexpected error: {e}")
def record_attendance():
    attendance_id = input("Enter a unique Attendance ID: ")
    employee_id = input("Enter Employee ID: ")
    training_id = input("Enter Training ID: ")
    status = input("Enter Attendance Status (Present/Absent/In Progress): ")

    cursor.execute("SELECT 1 FROM Employee WHERE Employee_ID = ?", (employee_id,))
    if not cursor.fetchone():
        print(" Error: Employee ID does not exist.")
        return

    cursor.execute("SELECT 1 FROM Training WHERE Training_ID = ?", (training_id,))
    if not cursor.fetchone():
        print(" Error: Training ID does not exist.")
        return

    try:
        cursor.execute("""
            INSERT INTO Attendance (Attendance_ID, Employee_ID, Training_ID, Completion_Status)
            VALUES (?, ?, ?, ?)
        """, (attendance_id, employee_id, training_id, status))
        conn.commit()
        print(" Attendance recorded.")
    except sqlite3.IntegrityError:
        print(" Error: Attendance ID already exists.")
    except Exception as e:
        print(f" Error: {e}")
def complete_training():
    employee_id = input("Enter Employee ID: ")
    training_id = input("Enter Training ID: ")

    cursor.execute("""
        UPDATE Attendance
        SET Completion_Status = 'Completed'
        WHERE Employee_ID = ? AND Training_ID = ?
    """, (employee_id, training_id))
    conn.commit()
    print(" Training marked as completed.")

def generate_report():
    print("\n Completed Trainings:")
    cursor.execute("""
        SELECT e.FirstName || ' ' || e.LastName AS FullName, t.Title
        FROM Attendance a
        JOIN Employee e ON a.Employee_ID = e.Employee_ID
        JOIN Training t ON a.Training_ID = t.Training_ID
        WHERE LOWER(a.Completion_Status) = 'completed'
    """)
    completed = cursor.fetchall()
    if completed:
        for name, title in completed:
            print(f"{name} completed '{title}'")
    else:
        print("No trainings completed yet.")

    print("\nPending Trainings (Present / Absent / In Progress):")
    cursor.execute("""
        SELECT e.FirstName || ' ' || e.LastName AS FullName, t.Title, a.Completion_Status
        FROM Attendance a
        JOIN Employee e ON a.Employee_ID = e.Employee_ID
        JOIN Training t ON a.Training_ID = t.Training_ID
        WHERE LOWER(a.Completion_Status) IN ('present', 'absent', 'in progress')
    """)
    pending = cursor.fetchall()
    if pending:
        for name, title, status in pending:
            print(f"{name} has '{title}' marked as {status}")
    else:
        print("No pending trainings.")
def main_menu():
    while True:
        print("\n--- Employee Training Management System ---")
        print("1. Schedule a Training Session")
        print("2. Record Employee Attendance")
        print("3. Mark Training as Completed")
        print("4. Generate Training Report")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            schedule_training()
        elif choice == '2':
            record_attendance()
        elif choice == '3':
            complete_training()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print(" Invalid option. Try again.")
if __name__ == "__main__":
    main_menu()
    conn.close()
