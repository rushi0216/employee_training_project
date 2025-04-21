import sqlite3

def create_database():
    # Connect to SQLite database (will be created if it doesn't exist)
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()

    # Create Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            Employee_ID INTEGER PRIMARY KEY,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT UNIQUE,
            Department TEXT
        )
    ''')

    # Create Training table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Training (
            Training_ID INTEGER PRIMARY KEY,
            Title TEXT NOT NULL,
            Scheduled_Date TEXT,
            Start_Time TEXT,
            End_Time TEXT,
            Duration TEXT
        )
    ''')

    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            Attendance_ID INTEGER PRIMARY KEY,
            Employee_ID INTEGER,
            Training_ID INTEGER,
            Completion_Status TEXT,
            Completion_Date TEXT,
            FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
            FOREIGN KEY (Training_ID) REFERENCES Training(Training_ID)
        )
    ''')

    # Save and close
    conn.commit()
    conn.close()
    print("✅ Database and tables created successfully!")

if __name__ == "__main__":
    create_database()

import sqlite3

def create_and_populate_database():
    # Connect to database
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()

    # Create Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            Employee_ID INTEGER PRIMARY KEY,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Department TEXT,
            Email TEXT UNIQUE
        )
    ''')

    # Create Training table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Training (
            Training_ID INTEGER PRIMARY KEY,
            Title TEXT NOT NULL,
            Scheduled_Date TEXT,
            Start_Time TEXT,
            End_Time TEXT,
            Duration TEXT
        )
    ''')

    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            Attendance_ID INTEGER PRIMARY KEY,
            Employee_ID INTEGER,
            Training_ID INTEGER,
            Completion_Status TEXT,
            Completion_Date TEXT,
            FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
            FOREIGN KEY (Training_ID) REFERENCES Training(Training_ID)
        )
    ''')

    # Insert dummy Employee records
    employees = [
        (1, 'Aron', 'Warner', 'awarner@gmail.com', 'IT'),
    (2, 'John', 'Brooks', 'jbrooks@gmail.com', 'Sales'),
    (3, 'Sam', 'Kelly', 'skelly@gmail.com', 'Finance'),
    (4, 'Kai', 'Moore', 'kmoore@gmail.com', 'IT'),
    (5, 'Damon', 'Torrance', 'dtorrance@gmail.com', 'Sales'),
    (6, 'Julie', 'West', 'jwest@gmail.com', 'Testing'),
    (7, 'Tatiana', 'Edwins', 'tedwins@gmail.com', 'Finance'),
    (8, 'Jones', 'Coery', 'jcoery@gmail.com', 'IT'),
    (9, 'Jack', 'Thomson', 'jthomson@gmail.com', 'Sales'),
    (10, 'Jona', 'Powell', 'jpowell@gmail.com', 'Testing')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Employee VALUES (?, ?, ?, ?, ?)', employees)

    # Insert dummy Training records
    trainings = [
        (101, 'Data Analytics', '04-09-2024', '2:00PM', '4:00PM', '2hrs'),
        (102, 'Cyber Security', '04-05-2024', '12:00PM', '3:00PM', '3hrs'),
        (103, 'Agile Development', '04-08-2024', '11:00AM', '1:00PM', '2hrs'),
        (104, 'Data Analytics', '05-25-2024', '3:00PM', '5:00PM', '2hrs'),
        (105, 'Communication Skills', '04-20-2024', '2:00PM', '5:00PM', '3hrs'),
        (106, 'Cuber Security', '05-11-2024', '8:00AM', '12:00PM', '4hrs'),
        (107, 'Quality Control', '06-13-2024', '9:00AM', '12:00PM', '3hrs'),
        (108, 'Agile Development', '05-15-2024', '2:00PM', '5:00PM', '3hrs'),
        (109, 'Sales Masterclass', '05-27-2024', '6:00PM', '9:00PM', '3hrs'),
        (110, 'Quality Control', '04-24-2024', '3:00PM', '7:00PM', '4hrs')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Training VALUES (?, ?, ?, ?, ?, ?)', trainings)

    # Insert dummy Attendance records
    attendance = [
        (1, 1, 101, 'Completed', '04-09-2024'),
        (2, 5, 105, 'Completed', '04-20-2024'),
        (3, 3, 107, 'In Progress', None),
        (4, 10, 106, 'Completed', '05-11-2024'),
        (5, 9, 105, 'In Progress', None),
        (6, 2, 102, 'Completed', '04-05-2024'),
        (7, 4, 104, 'In Progress', None),
        (8, 7, 103, 'Completed', '04-08-2024'),
        (9, 6, 108, 'In Progress', None),
        (10, 8, 110, 'Completed', '04-24-2024')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Attendance VALUES (?, ?, ?, ?, ?)', attendance)

    # Save and close
    conn.commit()
    conn.close()
    print("Database created and populated successfully!")

# Run the function
if __name__ == '__main__':
    create_and_populate_database()

# --- EMPLOYEE CRUD OPERATIONS ---

def add_employee(employee_id, first_name, last_name, email, department):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Employee (Employee_ID, FirstName, LastName, Email, Department)
        VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, first_name, last_name, email, department))
    conn.commit()
    conn.close()
    print("✅ New employee added.")

def read_employees():
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

def update_employee(employee_id, new_email, new_department):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Employee
        SET Email = ?, Department = ?
        WHERE Employee_ID = ?
    ''', (new_email, new_department, employee_id))
    conn.commit()
    conn.close()
    print("✅ Employee updated.")

def delete_employee(employee_id):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employee WHERE Employee_ID = ?", (employee_id,))
    conn.commit()
    conn.close()
    print("🗑️ Employee deleted.")


# --- ATTENDANCE CRUD OPERATIONS ---

def add_attendance(attendance_id, employee_id, training_id, status, date):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Attendance (Attendance_ID, Employee_ID, Training_ID, Completion_Status, Completion_Date)
        VALUES (?, ?, ?, ?, ?)
    ''', (attendance_id, employee_id, training_id, status, date))
    conn.commit()
    conn.close()
    print("✅ New attendance added.")

def read_attendance():
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Attendance")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

def update_attendance(attendance_id, new_status, new_date):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Attendance
        SET Completion_Status = ?, Completion_Date = ?
        WHERE Attendance_ID = ?
    ''', (new_status, new_date, attendance_id))
    conn.commit()
    conn.close()
    print("✅ Attendance record updated.")

def delete_attendance(attendance_id):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Attendance WHERE Attendance_ID = ?", (attendance_id,))
    conn.commit()
    conn.close()
    print("🗑️ Attendance record deleted.")


# --- TRAINING CRUD OPERATIONS ---

def add_training(training_id, title, date, start_time, end_time, duration):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Training (Training_ID, Title, Scheduled_Date, Start_Time, End_Time, Duration)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (training_id, title, date, start_time, end_time, duration))
    conn.commit()
    conn.close()
    print("✅ New training added.")

def read_trainings():
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Training")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

def update_training(training_id, new_title, new_duration):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Training
        SET Title = ?, Duration = ?
        WHERE Training_ID = ?
    ''', (new_title, new_duration, training_id))
    conn.commit()
    conn.close()
    print("✅ Training updated.")

def delete_training(training_id):
    conn = sqlite3.connect('EmployeeTraining.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Training WHERE Training_ID = ?", (training_id,))
    conn.commit()
    conn.close()
    print("🗑️ Training deleted.")
