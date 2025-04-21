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
