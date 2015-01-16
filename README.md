# grade_mc: A partial-credit multiple-choice grader in Python

grade_mc is a simple Python 3 script for processing the output of machine-graded multiple choice exams. It allows per-item point values, enabling partial credit for some answers. It can handle multiple, scrambled forms.

The purpose and usage of the script has been discussed in a short series of [blog posts](http://blog.hartleygroup.org/2014/12/05/a-python-script-for-grading-partial-credit-multiple-choice-part-1/).

## Requirements

* Python 3
* [Numpy](http://www.numpy.org)

## Use

Run `python3 grade_mc.py` as usual (or just `grade_mc` if made executable). It will prompt for the file containing the answer key, the file containing the raw student responses, and (optionally) the file containing the scramble used for multiple forms (see below). Then prompts for the title for the results and (optionally) a file name for the output.

Samples of the required files are provided. The key is a plain text file of format:

```
0 0 4 0 0
4 0 0 0 0
0 2 0 2 4
```

where the columns left-to-right give the point values for each response A–E, one row per question (in the example above, the answer C to question 1 gets 4 points).

The raw output is also a plain text file of format:

```
000000000 21020331323103343144
adpxnkvx 204443403131302413422
aeaekfhv 121320333320114342142
apqaagpo 100310331221144233142
aqnioyxy 214423424331041213430
batmtdas 233443314141341300104
bmehvlxa 203423311343301430302

```

where the first 8 characters are a student's unique identifier, the first number is the form number, and the remaining numbers are the recorded responses with 0 = "A" and 4 = "E".

The scramble file is also plain text of format:

```
1   13
2   16
3   15
4   14
5   17
6   6
7   2
8   11
9   5
```

where the columns represent the analogous questions in each form (in the example, Q2 on form 1 is Q16 on form 2).
