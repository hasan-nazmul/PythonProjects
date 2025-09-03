import student, pickle

with open('student.data', 'rb') as f:
    for i in range(3):
        s = pickle.load(f)
        s.display()
        print('-'*15)