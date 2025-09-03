import csv
import re

f = open('data.csv', 'r')  # Open a file for reading
csv_reader = csv.reader(f)  # Create a CSV reader object

pat1 = re.compile(r'/(\d+)/(\w+)')
pat2 = re.compile(r'CF(\d+)-D2-(\w+)')

problem_list = []

for row in csv_reader:
    finding = re.finditer(pat1, row[0])
    for match in finding:
        problem_list.append(match.group(1)+match.group(2))
    finding = re.finditer(pat2, row[0])
    for match in finding:
        problem_list.append(match.group(1) + match.group(2))

for p in problem_list:
    print(p)

# print(len(problem_list))

f.close()  # Close the file after reading