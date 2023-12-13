#This file is to create classes for data fetch in the database

#Library import
from Database import professors_database as pd
from Database import student_database_manager as sdm

#Class person this is a generalze class
class Person(object):
    def __init__(self, name, school_id) -> None:
        self._name = name
        self._id = school_id

    @property
    def name(self):
       return self._name

    @name.setter
    def name(self, name):
        self._name = name 

    @property
    def id(self):
       return self._id

    @id.setter
    def id(self, id):
        self._id = id 

    def __str__(self) -> str:
        return f"{self._name}"

class Professor(Person):
    def __init__(self, name, school_id) -> None:
        super().__init__(name, school_id)
        self._students = None

    def __delattr__(self, __name: str) -> None:
        pd.delete_professor(self.id)
        return super().__delattr__(__name)

    @property
    def students(self):
        return self._students
    
    @students.setter
    def students(self, students):

        #Variable declaration
        students_class = []

        for student in students:
            my_student = StudentClass(student["name"], student["student_id"], student["score"], student["profs"])
            students_class.append(my_student)

        self._students = students_class

    def get_students(self):
        prof_students = pd.update_professors_students(self.id)
        self.students = prof_students

    def sort_students(self) -> None:
        self.students.sort(key=lambda x : x.score)
        while True:
            n = 0
            for i in range(1, len(self.students)):
                if self.students[i - 1].score > self.students[i].score:
                    temp = self.students[i - 1]
                    self.students[i - 1] = self.students[i]
                    self.students[i] = temp
                    n += 1
            
            if n == 0 : break

        self.students.reverse()

    def __str__(self) -> str:
        return super().__str__()


class StudentClass(Person) :
    def __init__(self, name, school_id, score, prof_id) -> None:
        super().__init__(name, school_id)
        self._score = score
        self._prof_id = prof_id

    def __delattr__(self, __name: str, stu_id: str) -> None:
        sdm.delete_student(stu_id)
        return super().__delattr__(__name)

    @property
    def score(self):
       return self._score

    @score.setter
    def score(self, score: str):
        self._score = score 

    @property
    def prof_id(self):
       return self._prof_id

    @prof_id.setter
    def iprof_idd(self, prof_id: str):
        self._prof_id = prof_id 

    def to_jason(self):
        return {
            "name" : self.name,
            "student_id": self.id,
            "score" : self.score,
            "profs" : self.prof_id
        }

    def __str__(self) -> str:
        return super().__str__()