# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`grade_mc` is a partial-credit multiple-choice exam grader in Python. It supports per-item point values, multiple scrambled exam forms, and optional individualized student output.

## Installation and Running

```bash
# Install in development mode
pip install -e .

# Run as installed CLI tool
grade_mc <key_file> <raw_file> <title> [-s <scramble_file>] [-o]

# Run directly as a module (without installing)
python3 -m grade_mc <key_file> <raw_file> <title> [-s <scramble_file>] [-o]
```

## Manual Testing with Sample Files

There is no automated test suite. Validate changes by running against the samples and comparing output:

```bash
# Multiple forms (with scramble file)
grade_mc samples/test_key.txt samples/test_raw_key.txt "Test - With Key" -s samples/test_scr.txt

# Single form (no scramble)
grade_mc samples/test_key.txt samples/test_raw_nokey.txt "Test - No Key"
```

Expected outputs are in `samples/test_output_key.txt` and `samples/test_output_nokey.txt`.

## Architecture

All logic lives in a single file: `grade_mc/grade_mc.py`. The `__init__.py` just re-exports everything from it.

### Key File Formats

- **Key file** (`test_key.txt`): One row per question, 5 space-separated point values representing partial credit for answers A–E.
- **Raw responses file** (`test_raw_key.txt` / `test_raw_nokey.txt`): Each line is an 8-character student ID + 1-character form number (or space) + answers as letters A–E (or `.` for blank).
- **Scramble file** (`test_scr.txt`): Maps question numbers between forms. Each row is a question; columns are forms. Used to reorder student responses so all forms grade against the same key.

### Core Functions

- **`generate_responses_array(answers)`** — Converts a string of letter answers into a one-hot numpy array (shape: `num_questions × NUM_ANSWERS`).
- **`descramble(responses, formnum, scramble)`** — Reorders a student's response array using the scramble map so it aligns with the master key.
- **`convert_response_to_letter(response)`** — Converts a one-hot row back to a letter (`A`–`E`) or `.` for blank.
- **`main(key_file_name, answers_file_name, title, scramble_file_name=None)`** — Loads all files, grades all students, computes statistics (overall, per-question, top/bottom 27% analysis), and returns `(overall_output_text, {student_id: individual_output})`.
- **`process_grades()`** — CLI entry point (registered as `grade_mc` console script). Parses args, calls `main()`, writes output file(s).

### Data Flow

1. Key file → numpy array (questions × 5) of point values
2. Raw file → per-student: ID, form number, response array
3. Optional descramble using scramble file
4. Score = dot product of response array with key array, summed across questions
5. Output: overall stats + per-question frequency analysis + student score list; optionally per-student response sheets
