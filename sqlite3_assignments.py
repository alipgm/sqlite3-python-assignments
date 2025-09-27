"""
SQLite3 Assignments - Complete Solution
A comprehensive Python script demonstrating SQLite3 database operations
Includes all 10 assignments with proper error handling and transactions
"""

import sqlite3
import shutil
import time
import os


def create_database():
    """
    Assignment 1.1: Create a new SQLite3 database named 'test.db'
    """
    # Remove existing database to start fresh
    if os.path.exists('test.db'):
        os.remove('test.db')
    
    conn = sqlite3.connect('test.db')
    conn.close()
    print("Database created and successfully connected.")


def create_table():
    """
    Assignment 1.2: Create employees table with columns: id, name, age, department
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            department TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Table 'employees' created successfully.")


def insert_employee(id, name, age, department):
    """
    Assignment 2.1: Insert a new employee into the employees table
    Uses parameterized queries to prevent SQL injection
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (id, name, age, department)
        VALUES (?, ?, ?, ?)
    ''', (id, name, age, department))
    conn.commit()
    conn.close()
    print(f"Employee {name} inserted successfully.")


def fetch_all_employees():
    """
    Assignment 3.1: Fetch and display all records from employees table
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    records = cursor.fetchall()
    conn.close()
    print("All employees:")
    for record in records:
        print(record)
    return records


def fetch_employees_by_department(department):
    """
    Assignment 3.2: Fetch employees from a specific department
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE department = ?', (department,))
    records = cursor.fetchall()
    conn.close()
    print(f"Employees in {department} department:")
    for record in records:
        print(record)


def update_employee_department(employee_id, new_department):
    """
    Assignment 4.1: Update employee department based on ID
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees
        SET department = ?
        WHERE id = ?
    ''', (new_department, employee_id))
    conn.commit()
    conn.close()
    print(f"Employee {employee_id} department updated to {new_department}.")


def delete_employee(employee_id):
    """
    Assignment 5.1: Delete an employee based on ID
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM employees
        WHERE id = ?
    ''', (employee_id,))
    conn.commit()
    conn.close()
    print(f"Employee {employee_id} deleted successfully.")


def fetch_employees_older_than(age):
    """
    Assignment 6.1: Fetch employees older than specified age
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE age > ?', (age,))
    records = cursor.fetchall()
    conn.close()
    print(f"Employees older than {age}:")
    for record in records:
        print(record)


def fetch_employees_name_starts_with(letter):
    """
    Assignment 6.2: Fetch employees whose names start with specific letter
    Uses LIKE operator with wildcard %
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', (letter + '%',))
    records = cursor.fetchall()
    conn.close()
    print(f"Employees whose names start with '{letter}':")
    for record in records:
        print(record)


def insert_multiple_employees(employees):
    """
    Assignment 7.1: Insert multiple employees in a single transaction
    If any insertion fails, all changes are rolled back
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.executemany('''
            INSERT INTO employees (id, name, age, department)
            VALUES (?, ?, ?, ?)
        ''', employees)
        conn.commit()
        print("All employees inserted successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print("Error occurred, transaction rolled back.")
        print(f"Error: {e}")
    finally:
        conn.close()


def update_multiple_employees_ages(updates):
    """
    Assignment 7.2: Update age of multiple employees in a single transaction
    If any update fails, all changes are rolled back
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.executemany('''
            UPDATE employees
            SET age = ?
            WHERE id = ?
        ''', updates)
        conn.commit()
        print("All employee ages updated successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print("Error occurred, transaction rolled back.")
        print(f"Error: {e}")
    finally:
        conn.close()


def create_departments_table():
    """
    Assignment 8.1: Create departments table with id and name columns
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("Table 'departments' created successfully.")


def add_department_foreign_key():
    """
    Assignment 8.2: Modify employees table to include foreign key reference
    Fixed: Execute each SQL statement separately
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    try:
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if the foreign key column already exists
        cursor.execute("PRAGMA table_info(employees)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'department_id' not in columns:
            # Create a new table with the foreign key
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees_new (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    department TEXT,
                    department_id INTEGER,
                    FOREIGN KEY(department_id) REFERENCES departments(id)
                )
            ''')
            
            # Copy data from old table to new table
            cursor.execute('''
                INSERT INTO employees_new (id, name, age, department)
                SELECT id, name, age, department FROM employees
            ''')
            
            # Drop the old table
            cursor.execute('DROP TABLE IF EXISTS employees')
            
            # Rename new table to employees
            cursor.execute('ALTER TABLE employees_new RENAME TO employees')
            
            print("Table 'employees' modified successfully with foreign key.")
        else:
            print("Foreign key column already exists.")
            
        conn.commit()
        
    except sqlite3.Error as e:
        conn.rollback()
        print("Error occurred while modifying table:")
        print(f"Error: {e}")
    finally:
        conn.close()


def insert_department_and_employee(department_id, department_name, employee_id, name, age, department):
    """
    Assignment 8.3: Insert data into both tables with referential integrity
    Uses transaction to ensure both operations succeed or fail together
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    try:
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Insert department
        cursor.execute('''
            INSERT OR IGNORE INTO departments (id, name)
            VALUES (?, ?)
        ''', (department_id, department_name))
        
        # Insert employee with foreign key reference
        cursor.execute('''
            INSERT INTO employees (id, name, age, department, department_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (employee_id, name, age, department, department_id))
        
        conn.commit()
        print("Department and employee inserted successfully.")
        
    except sqlite3.Error as e:
        conn.rollback()
        print("Error occurred, transaction rolled back.")
        print(f"Error: {e}")
    finally:
        conn.close()


def create_index_on_name():
    """
    Assignment 9.1: Create index on name column for performance optimization
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON employees(name)')
    conn.commit()
    conn.close()
    print("Index on 'name' column created successfully.")


def fetch_employees_name_starts_with_performance(letter):
    """
    Assignment 9.2: Fetch employees with name starting with letter and measure performance
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', (letter + '%',))
    records = cursor.fetchall()
    end_time = time.time()
    conn.close()
    print(f"Time taken: {end_time - start_time:.6f} seconds")
    print(f"Employees whose names start with '{letter}':")
    for record in records:
        print(record)


def backup_database():
    """
    Assignment 10.1: Backup database to backup.db file
    """
    if os.path.exists('test.db'):
        shutil.copy('test.db', 'backup.db')
        print("Database backed up successfully.")
    else:
        print("Database file not found.")


def restore_database():
    """
    Assignment 10.2: Restore database from backup.db file
    """
    if os.path.exists('backup.db'):
        shutil.copy('backup.db', 'test.db')
        print("Database restored successfully.")
    else:
        print("Backup file not found.")


def main():
    """
    Main function to demonstrate all assignments
    """
    print("=== SQLite3 Assignments Demo ===\n")
    
    try:
        # Assignment 1
        print("1. Creating database and table...")
        create_database()
        create_table()
        
        # Assignment 2
        print("\n2. Inserting employees...")
        employees_data = [
            (1, 'Alice', 30, 'HR'),
            (2, 'Bob', 25, 'Engineering'),
            (3, 'Charlie', 28, 'Sales'),
            (4, 'David', 35, 'Marketing'),
            (5, 'Eve', 22, 'HR')
        ]
        
        for emp in employees_data:
            insert_employee(*emp)
        
        # Assignment 3
        print("\n3. Querying data...")
        fetch_all_employees()
        fetch_employees_by_department('HR')
        
        # Assignment 4
        print("\n4. Updating data...")
        update_employee_department(1, 'Finance')
        update_employee_department(2, 'Research')
        fetch_all_employees()
        
        # Assignment 5
        print("\n5. Deleting data...")
        delete_employee(4)
        fetch_all_employees()
        
        # Assignment 6
        print("\n6. Advanced queries...")
        fetch_employees_older_than(25)
        fetch_employees_name_starts_with('A')
        
        # Assignment 7
        print("\n7. Transaction handling...")
        new_employees = [
            (6, 'Frank', 40, 'Finance'),
            (7, 'Grace', 29, 'Engineering')
        ]
        insert_multiple_employees(new_employees)
        
        age_updates = [
            (32, 1),
            (26, 2)
        ]
        update_multiple_employees_ages(age_updates)
        fetch_all_employees()
        
        # Assignment 8
        print("\n8. Creating relationships...")
        create_departments_table()
        add_department_foreign_key()
        
        # Insert sample department data first
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('INSERT OR IGNORE INTO departments (id, name) VALUES (1, "Finance")')
        cursor.execute('INSERT OR IGNORE INTO departments (id, name) VALUES (2, "HR")')
        conn.commit()
        conn.close()
        
        insert_department_and_employee(1, 'Finance', 10, 'Zara', 28, 'Finance')
        fetch_all_employees()
        
        # Assignment 9
        print("\n9. Indexing and optimization...")
        create_index_on_name()
        fetch_employees_name_starts_with_performance('A')
        
        # Assignment 10
        print("\n10. Backup and restore...")
        backup_database()
        restore_database()
        
        print("\n=== All assignments completed successfully! ===")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()