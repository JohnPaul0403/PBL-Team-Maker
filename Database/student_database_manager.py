#This file will manage the database for students, it will be capable to create a student database and link it to a professors ID

#Library import
import csv

# Define the CSV file path.
csv_file = "student_data.csv"

# Function to create a new student record.
def create_student(name, student_id, score, prof_id):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, student_id, score, prof_id])

# Function to read and display all student records.
def read_students():

    #Variable declaration
    students = []

    #Accesing to the database to seach for all students
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            name, student_id, score, prof_id = row
            students.append(
                {
                    "name" : name,
                    "student_id": student_id,
                    "score" : score,
                    "profs" : eval(prof_id)
                }
            )
    
    return students

# Function to update a student record by student ID.
def update_student(student_id, new_score):
    data = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == student_id:
                row[2] = new_score
            data.append(row)
    
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Function to delete a student record by student ID.
def delete_student(student_id):
    data = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != student_id:
                data.append(row)
    
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Example usage:
def create_data_student() :
    while True:
        print("\nCRUD Options:")
        print("1. Create student record")
        print("2. Read all student records")
        print("3. Update student record")
        print("4. Delete student record")
        print("5. Quit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == "1":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            score = input("Enter student score: ")
            prof_id = input("Enter the proffesors ID: ")
            create_student(name, student_id, score, prof_id.split(", "))
        elif choice == "2":
            print("\nAll Student Records:")
            read_students()
        elif choice == "3":
            student_id = input("Enter student ID to update: ")
            new_score = input("Enter new score: ")
            update_student(student_id, new_score)
        elif choice == "4":
            student_id = input("Enter student ID to delete: ")
            delete_student(student_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")
