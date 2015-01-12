#! /usr/bin/env python3
""" A simple python script that grades MC output from Scantron forms.

Takes 2 files as arguments. First, the grading key, a matrix with point values for each answer
deliminated by spaces, one row per question. Zeroes must be included. Second, the raw output from
IT. Correctly handles blank answers  ("."), but not forms. The Scantron key must be the first line
(for verification), usually with uniqueID 00000000.


"""
import sys, numpy as np
from operator import itemgetter

# Top and bottom cutoffs for analysis of answers, as fraction. IT uses 27% for some reason.
analysis_threshhold = 0.27

key_file = open(sys.argv[1])
answers_file = open(sys.argv[2])

# This function takes parameter answers (string in format "0213101230...") and returns the student
# solutions as an array, with "1" indicating the selection (for example, row [0,0,1,0,0] indicates
# an answer of c). This array yields the total when multiplied by the key and summed.
def generate_responses_array(answers):
    responses = []
    for qnum in range(len(answers)):
        response = [0 for n in range(5)]
        # Check if blank response.
        if answers[qnum] != ".":
            response[int(answers[qnum])] = 1
        responses.append(response)
    return np.array(responses)

title = input("Title for results: ")
output_file = open(input("Filename for output: "), "w")

# Load the key. Result is a numpy array.
key = np.loadtxt(key_file)
num_questions = len(key)

# Load the student info. Characters 0-7 in the input file are the student's uniqueID. Characters
# 10-? are the recorded answers. For student n, students[n][0] is the student's name, students[n][1]
# is the set of responses, as an array. Only collects the responses portion of the string (up to
# 10+num_questions), because the Scantron system can append extra characters.
students = []
for line in answers_file:
    students.append([line[0:8], generate_responses_array(line[10:10 + num_questions].replace("\n", ""))])

num_students = len(students[1:])
num_students_analysis = round(analysis_threshhold * num_students)

# Actually determines score for each student. Multiplies sets of responses by the key, then sums
# over whole array.
for stu_num in range(len(students)):
    students[stu_num].append((students[stu_num][1] * key).sum())

# Generates a new array, students_sorted, that is just sorted by grades. Des not include key
# (students[0])
students_sorted = sorted(students[1:], key=itemgetter(2), reverse=True)

# Determines number of each response, by question, for all students, and for the top and bottom
# students in the class. Values are given as fractions.
all_answers_frac = (sum(n[1] for n in students_sorted[:]) / num_students)
top_answers_frac = (sum(n[1] for n in students_sorted[:num_students_analysis]) / num_students_analysis)
bot_answers_frac = (sum(n[1] for n in students_sorted[-num_students_analysis:]) / num_students_analysis)

# List of all grades. Students only (key not included).
all_grades = [n[2] for n in students[1:]]

# The score for the Scantron key, as a check to make sure it was assessed properly.
max_score = students[0][2]
print("\nCheck: the Scantron key (uniqueID = {}) scores {:.2f}.\n".format(students[0][0], max_score))

# Dump everything into the output file.
output_file.write("{}\n".format(title))
output_file.write("{}\n\n".format("=" * len(title)))

# The overall averages, max, and min.
output_file.write("   Overall average: {:.2f} out of {:.2f} points ({:.2%})\n".
    format(np.mean(all_grades), max_score, np.mean(all_grades) / max_score))
output_file.write("Standard deviation: {:.2f}\n".format(np.std(all_grades)))
output_file.write("              High: {}\n".format(max(all_grades)))
output_file.write("               Low: {}\n".format(min(all_grades)))
output_file.write("\n")

# Breakdown by question. Includes both average score for the question, the overall performance, and
# the performance of the strongest and weakest students.
output_file.write("Average Scores by Question\n")
output_file.write("{}\n\n".format("-" * 26))

for n in range(num_questions):
    output_file.write("{:3}: {:.2f}         Key: ".format(n + 1, sum(all_answers_frac[n] * key[n])))
    for m in range(len(key[n])):
        if key[n][m] != 0:
            output_file.write("{:6.1f}  ".format(key[n][m]))
        else:
            output_file.write("    -   ")
    output_file.write("\n            Frequency:  ")
    for m in range(len(all_answers_frac[n])):
        output_file.write("{:5.1f}   ".format(all_answers_frac[n][m] * 100))
    output_file.write("(%)\n              Top {:2.0f}%:  ".format(analysis_threshhold * 100))
    for m in range(len(top_answers_frac[n])):
        output_file.write("{:5.1f}   ".format(top_answers_frac[n][m] * 100))
    output_file.write("\n              Bot {:2.0f}%:  ".format(analysis_threshhold * 100))
    for m in range(len(bot_answers_frac[n])):
        output_file.write("{:5.1f}   ".format(bot_answers_frac[n][m] * 100))
    output_file.write("\n\n")

# Actual student scores.
output_file.write("\nStudent Scores\n")
output_file.write("{}\n".format("-" * 14))
for student in students:
    output_file.write("{:8}\t{:.1f}\n".format(student[0], student[2]))