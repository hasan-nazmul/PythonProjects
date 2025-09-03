import student, pickle

students =  [
                student.Student(10, 'John', 'cs'),
                student.Student(20, 'Jack', 'ee'),
                student.Student(30, 'Khan', 'me')
            ]

with open('student.data', 'wb') as file:
    for s in students:
        pickle.dump(s, file)
