import os
import stat
from .cpp_runner import run_cpp
from subprocess import run, CompletedProcess


def test_cpp(file: str, data_in: list, data_out: list) -> list:
    status = run(['g++', file], capture_output=True)  # Compile file

    if status.returncode == 1:
        print(status.stderr.decode())
        return False

    else:
        correctness = True
        correct_counter = 0

        tests_number = len(data_in)
        tests_results = []
        for i, question, answer in zip(range(1, tests_number + 1), data_in, data_out):
            program_out = run_cpp(question)

            test_correctness = (answer == program_out)
            correctness *= test_correctness
            correct_counter += test_correctness

            tests_results.append([i, test_correctness, question, answer, program_out])

        return [correctness, f'passed {correct_counter}/{tests_number} tests', tests_results]


if __name__ == "__main__":
    print(test_cpp('main.cpp', ['1 2', '2 2', '3 3', '4 1'], ['6', '8', '12', '10']))
