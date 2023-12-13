#This file will manage the database for students, it will be capable to create a student database and link it to a professors ID

#Library import
import csv
from Database import student_database_manager as sdm

# Define the CSV file path.
csv_file_name = "professors_data.csv"

# Function to create a new student record.
def create_proffesor(name, proffesor_id):

    #Variable declaration
    students = []

    #Saving the proffesor in the database
    with open(csv_file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, proffesor_id, students])

# Function to read and display all student records.
def read_professors():

    #Variable declaration
    profs = []

    with open(csv_file_name, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            name, prof_id, students = row
            profs.append([name, prof_id, list(students)])

    return profs

# Function to update a student record by student ID.
def update_professors_name(prof_id, new_name):
    data = []
    update_professors_students(prof_id)
    with open(csv_file_name, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == prof_id:
                row[0] = new_name
            data.append(row)
    
    with open(csv_file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

#Function to update Professors Students
def update_professors_students(prof_id):
    
    #Variable declaration
    data = []
    students = []
    all_students = sdm.read_students()

    for student in all_students:
        students.extend(
            student
            for professor in student["profs"]
            if str(professor) == prof_id
        )
    with open(csv_file_name, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == prof_id:
                row[2] = students
            data.append(row)

    with open(csv_file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return students

#Get proffesor name by its id
def get_name_by_id(proffesor_id):

    with open(csv_file_name, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            name, prof_id, students = row
            if prof_id == proffesor_id:
                return name

# Function to delete a student record by student ID.
def delete_professor(proffesor_id):
    data = []
    with open(csv_file_name, mode="r") as file:
        reader = csv.reader(file)
        data.extend(row for row in reader if row[1] != proffesor_id)
    with open(csv_file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

#Function to create a new proffessor
def create_prof():
    while True:
        print("\nCRUD Options:")
        print("1. Create student record")
        print("2. Read all student records")
        print("3. Update a professor's name")
        print("4. Delete student record")
        print("5. Quit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")

        print(choice)
        
        if choice == "1":
            name = input("Enter Professor name: ")
            student_id = input("Enter student ID: ")
            create_proffesor(name, student_id)
        elif choice == "2":
            print("\nAll Student Records:")
            print(csv_file_name)
            read_professors()
        elif choice == "3":
            student_id = input("Enter student ID to update: ")
            new_score = input("Enter new score: ")
            update_professors_name(student_id, new_score)
        elif choice == "4":
            student_id = input("Enter student ID to delete: ")
            delete_professor(student_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")
