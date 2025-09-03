from tkinter import *
import csv

def show_data(e):
    employee = [row for row in data if row[0]==str(var.get())][0]
    j = 0
    for i in widgets:
        i[1].delete(0, END)
        i[1].insert(0, employee[j])
        j += 1

def update_handler():
    employee = [row for row in data if row[0] == str(widgets[0][1].get())]
    if not employee:
        return
    employee = employee[0]
    updated_employee = employee
    for i in range(len(widgets)):
        updated_employee[i] = widgets[i][1].get()
    data.remove(employee)
    data.append(updated_employee)
    print(data)

def save_changes():
    file_csv = open('Employees.csv', 'w', newline='')
    writer = csv.writer(file_csv)
    writer.writerow(headings, )
    writer.writerows(data)
    file_csv.close()

win = Tk()
win.geometry('400x300')

file_csv = open('Employees.csv', 'r')
reader = csv.reader(file_csv)

headings = next(reader)

widgets = []
data = []

for e in reader:
    data.append(e)

file_csv.close()

lbl = Label(win, text=headings[0], font=('Times New Roman', 10))
lbl.pack()

var = StringVar(value=data[0][0])
opt = OptionMenu(win, var, *[row[0] for row in data], command=show_data)
opt.pack()

for h in headings:
    widgets.append((Label(win, text=h, font=('Times New Roman', 15)),
                   Entry(win, width=20, font=('Times New Roman', 15))))
    widgets[-1][0].pack()
    widgets[-1][1].pack()

update = Button(win, text='update', command=update_handler)
update.pack()

save = Button(win, text='save changes', command=save_changes)
save.pack()

win.mainloop()